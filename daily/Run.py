#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 23:32:23 2017

@author: misakawa
"""

import sys
import numpy as np

def main(size:str, f:str, learnRate = 0.5, iters = 5):
    learnRate = float(0.5)
    iters     = int(iters)
    size      = int(size)

    bases     = np.random.random(size = (size, )) * (2 * np.pi)
    R         = np.arange(0, 1, 0.05)

    Y = np.sin(bases)
    X = np.cos(bases)
    
    indices  = np.random.permutation(size)
    datas    = np.array(list(zip(X,Y)))[indices]
    datas    = np.vstack([r*datas for r in R])
    
    function = lambda y, x : eval(f)
    targets  = np.array([np.sign(function(y,x)) for x,y in datas])
    
    Weights  = np.random.rand(1, 2)
    Bias     = np.random.random()
    
#    net      = Perceptron(2, learnRate)
    for i in range(iters):
        for data, target in zip(datas, targets):
#            net.Renew(data, target) 
            if (np.dot(Weights, data)+Bias)*target <= 0: 
                Weights += learnRate * target * data
                Bias    += learnRate * target
                
    outputs = np.sign(np.dot(Weights, np.atleast_2d(datas).T)+Bias)
#    outputs = [np.sign(Weights*data) for data, in datas]
    from matplotlib import pyplot as plt
    plt.subplot(211)
    plt.scatter(datas[:,0], datas[:, 1], c = targets)
    plt.subplot(212)
    plt.scatter(datas[:,0], datas[:, 1], c = outputs )
    plt.show()

if __name__ == '__main__':
	args = sys.argv[1:]
	main(*args)