ignored = 15
import concurrent.futures
import numpy.random as rnd
import numpy as np
from numpy import vectorize
from copy import deepcopy
from numba import autojit
import sys
def forI(i, p_c, prob_interval):
        if master_influ_prob[i] > p_c:
            master = deepcopy(seqs[master_indices[i]])
            crossover(master, seqs[I[i]], prob_interval)
            seqs[I[i]+1] = master            
rev = {1:0, 0:1}
@autojit
def generate(length):
    return rnd.randint(0, 2,size=(length,))

@autojit
def mutate(seq, p_m):
    for i in range(len(seq)):
        seq[i] = rev[seq[i]]
        
@autojit
def crossover(seq1, seq2, prob_interval):
    
    idx  = int(np.random.random()/prob_interval)
    temp = np.zeros((idx,)).astype(np.int)
    for i in range(idx):
        temp[i] = seq1[i]
        seq1[i] = seq2[i]
        seq2[i] = temp[i]
        
def return_score(seq, fscore, fchange):
    seq.setflags(write= True)
    fchange(seq)
    return fscore(seq)
def evolution(fitness, p_c, p_m, prob_interval ,stats, range_indices):
    global master_influ_prob, master_indices, I, seqs
    fchange    = lambda seq : mutate(seq, p_m)
    fit        = lambda seq : return_score(seq, fitness, fchange)
    def select(i, seqs):
        return fit(seqs[i]) if i>ignored else fitness(seqs[i])
    scores = vectorize(select, signature='(),(m,n)->()', otypes=[np.float])(range_indices,seqs)
    indices= np.argsort(scores)[::-1]
    seqs   = np.take(seqs, indices, axis = 0)
    ignore = np.float(0)
    final_eval = False
    for idx, score_idx in enumerate(indices):
        score  = scores[score_idx] 
        ignore += score
        if ignore > ignored:
            if idx == ignored:
                final_eval = True
            I = list(range(idx, len(seqs)-1 , 2))
            master_indices    = rnd.randint(0, idx if idx else 1, size = (len(I),) )
            master_influ_prob = rnd.random(size = (len(I),) )
            
            for i, seq_idx in enumerate(I):
                if master_influ_prob[i] > p_c:
                    master = deepcopy(seqs[master_indices[i]])
                    crossover(master, seqs[seq_idx], prob_interval)
                    seqs[seq_idx+1] = master
#            with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
#                for i in range(len(I)):
#                    executor.submit(forI, i, p_c, prob_interval)
            for i in range(idx):
                for j in range(stats.shape[0]):
                    stats[j][seqs[i][j]]+=1
            break
    return final_eval, scores[indices[0]]        

def run(fitness, length, p_c = 0.5, p_m = 0.06, iterations=100):
    global ignored, seqs
    stats = np.zeros((length, 2))
    prob_interval = 1.0/length
    popu_size     = 1000        # the max size of population
    range_indices = np.arange(popu_size)
    seqs = vectorize(generate, signature='()->(m)')(np.repeat(length, popu_size))
    range_indices = np.arange(len(seqs))
    final_eval = False
    for i in range(iterations):
        final_eval, max_score = evolution(fitness, p_c, p_m, prob_interval, stats, range_indices)
        if max_score == 1.0:
            try:
                ignored = tmp_glob
            except:pass
            return ''.join(map(str, seqs[0]))
        elif final_eval:
            try:
                tmp_glob
            except:
                tmp_glob = ignored
            ignored *= 2
            stats = (stats/2).astype(np.int)
    print(max_score)
    res1 = list(map(lambda x: 0 if x[0]>x[1] else 1 , stats))
    res2 = seqs[0]
    try:
        ignored = tmp_glob
    except:pass
    res = res1 if fitness(res1) > fitness(res2) else res2
    return ''.join(map(str, res))

def fit1(seq):
    odd   = False
    score = 0
    for i in seq:
        score += i if odd else -i
        odd = not odd
    return score


    
def makeFitBySeq(seq1):
    def fit2(seq):
       return sum([1 for i,j in zip(seq, seq1) if i==j])
    return fit2
if __name__ == '__main__':
    print(run(eval(sys.argv[1]), int(sys.argv[2]), 0.3, 0.3))

# print(run(fit1, 20, 0.5, 0.3))
# target = [1,0,1,1,1,0,0,0,1,1,1,1,1,0,0,0,1,1,0,0]
# fit2 = makeFitBySeq(target)
# print(run(fit2, len(target), 0.3, 0.3))

    
