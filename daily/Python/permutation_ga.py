# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 01:07:03 2017

@author: thautwarm
"""


import numpy as np
from random import random

gen_chromosome = np.random.permutation  # initialize a piece of chromosome. 

# initialize a group of chromosomes, in other words, it's a population.
gen_population = lambda popu_size: lambda chromo_size:\
             np.vectorize(gen_chromosome, signature='()->(m)')(np.repeat(chromo_size, popu_size))



def genetic_algorithm_by_group(population, fit_func, mutate_rate=0.3, crossover_rate=0.2):
    popu_size, chromo_size = population.shape
    
    half = popu_size//2
    left = popu_size - half
    best = population[0]
    
    @np.vectorize
    def mutate(chromo_idx):
        chromo = population[chromo_idx]
        test_if_change = np.random.random((chromo_size, ))
        last = None
        for i in range(chromo_size):
            """
            循环似乎不可避免 because of none reference of immutable datas in CPython.
            """
            if mutate_rate > test_if_change[i]:
                if last is None:
                    last = i
                else:
                    chromo[last], chromo[i] = chromo[i], chromo[last]
    
    @np.vectorize
    def crossover(popu_idx):
        """inner crossover.
        """
        if crossover_rate>random():
            head = int(random()*chromo_size)
            this = population[popu_idx]
            a  = this[:head].copy()
            b  = this[head:].copy()
            for idx, e in enumerate(a):
                this[idx] = e
            idx = len(a)
            for tdx, e in enumerate(b):
                this[idx+tdx] = e 
        
    def natural_selection():
        nonlocal population, best
        mutate(np.arange(popu_size))
        crossover(np.arange(popu_size))
        population = population[np.argsort(np.vectorize(fit_func, signature='(m)->()')(population))]
        population[half:] = gen_population(left)(chromo_size)
        if fit_func(best) > fit_func(population[0]):
            best = population[0].copy()
            
    def evolution(iterations=100):
        for i in range(iterations):
            natural_selection()
            print(fit_func(best))
        return best
    return evolution


#
#
#fit = lambda x: x[0]>x[1]>x[2]>x[3]>x[4]
#evolution = genetic_algorithm_by_group(gen_population(100)(5), fit)
#maybe_best = evolution(1000)
#print(maybe_best)
#

X = [34, 56, 27, 44, 4, 10, 55, 14, 28, 12, 16, 68, 24, 29,49, 51, 45, 78, 82, 32, 95, 53, 
     7, 64, 88, 23, 87, 34, 71, 98]
print(len(X))


Y = [57, 64, 82, 94, 18, 64, 69, 30, 54, 70, 40, 46, 82, 38, 15, 26, 31, 56,
     33, 11, 8,  46, 94, 62, 52, 61, 76, 58, 41, 69]
print(len(Y))

Points = list(zip(X, Y))
from math import sqrt
get_dim_am = lambda i: lambda x,y: x[i]-y[i]
def dist(f, t):
    return sqrt(get_dim_am(0)(f, t)**2 + get_dim_am(1)(f, t)**2)
def gen_dist_for_permutation(permutation):
    _P = [Points[i] for i in permutation]
    return sum([dist(f, t) for f,t in zip(_P, _P[1:]+[_P[0]])])

popu = gen_population(1000)(30)
evolution = genetic_algorithm_by_group(popu, gen_dist_for_permutation, )
maybe_best = evolution(1000)
print(gen_dist_for_permutation(maybe_best))

# array([24, 20, 18, 21, 25,  8,  7,  0,  3,  1,  6, 19, 16, 15, 14, 28,  2,
#        4, 13, 12,  5,  9, 22, 10, 27, 23, 26, 17, 29, 11])

