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



def genetic_algorithm_by_group(population, fit_func, mutate_rate=0.3, crossover_rate=0.1):
    popu_size, chromo_size = population.shape
    
    half = popu_size//2
    left = popu_size - half
    
    @np.vectorize
    def mutate(chromo_idx):
        chromo = population[chromo_idx]
        test_if_change = np.random.random((chromo_size, ))
        last = None
        for i in range(chromo_size):
            if mutate_rate > test_if_change[i]:
                if last is None:
                    last = i
                else:
                    chromo[last], chromo[i] = chromo[i], chromo[last]
                    last = None
    
    @np.vectorize
    def crossover(popu_idx):
        """inner crossover.
        """
        if crossover_rate>random():
            head = int(random()*chromo_size)
            this = population[popu_idx]
            this.__init__(this[:head]+this[:head])                    
        
    def natural_selection():
        nonlocal population
        mutate(np.arange(popu_size))
        crossover(np.arange(popu_size))
        population = population[np.argsort(np.vectorize(fit_func, signature='(m)->()')(population))[::-1]]
        population[half:] = gen_population(left)(chromo_size)
            
    def evolution(iterations=100):
        for i in range(iterations):
            print(f'iteration-{i+1}')
            natural_selection()
        return population[0]
    return evolution




fit = lambda x: x[0]>x[1]>x[2]>x[3]>x[4]
evolution = genetic_algorithm_by_group(gen_population(100)(5), fit)
maybe_best = evolution()
print(maybe_best)
# array([4, 3, 2, 1, 0])
