# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 22:46:42 2018

@author: misakawa
"""

import numpy as np
from scipy import stats
import matplotlib as mpl
mpl.rcParams['font.sans-serif']=['FangSong']
import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
import pandas as pd
from sympy import init_printing, Matrix, latex
np.set_printoptions(suppress=True)
init_printing()


def standard_scale(x):
    x = x - np.mean(x)
    if all(x == 0):
        return np.zeros(x.shape)
    return x/np.linalg.norm(x)

class StatsEnv:
    def __init__(self, 
                 data: pd.DataFrame, 
                 target: str,
                 t=0.05,
                 use_bias = True,
                 report_filters=('x', 'y', 'e', 'C', 't', 'target')):
        if use_bias:
            data['beta0'] = np.ones(data.shape[0])
            
        self.data = data
        self.target = target
        self.t = t
        self.report_filters = report_filters 
        n , p = data.shape    
        
        p -= 1
        
        x =  data.loc[:, data.columns != target].values
        y = data[target].values
        coef, _, *_ = np.linalg.lstsq(x, y)
        
        
        C = np.linalg.inv(np.dot(x.T, x)) # c_ij matrix       
        
        e = y - np.dot(x, coef) 
        
        SSE = sum(np.square(e))
        
        stderr = sqrt(SSE/(n-p))
        
        SST = sum(np.square(y - np.mean(y)))
        
        R2 = 1 - SSE/SST 
        
        print(coef / np.sqrt(C.diagonal())*stderr)
        
        t_pair = np.array(list(zip(*stats.t.interval(
                                   t, 
                                   n, 
                                   coef, 
                                   np.sqrt(C.diagonal())*stderr))))
        
        checked_pass = [inf < beta < sup for (inf, sup), beta in zip(t_pair, coef)]
        r = np.dot(data.T, data)  # 相关系数
        self.stats_result = dict(
                coef = pd.DataFrame([data.columns[1:], coef]).T,
                equ = self.target + 
                        ' = ' + 
                        ' + '.join([f'{c}*{1 if name =="beta0" else name}' 
                                  for c, name in zip(coef.round(3), data.columns[1:])]),
                C = C,
                e = e,
                r = r,
                stderr = stderr,
                SST = SST,
                SSE = SSE,
                R2 = R2,
                t_pair = t_pair,
                checked_pass = checked_pass)
    
    def plot(self, dims: np.ndarray=1):
        """
        画图
        """
        
        if isinstance(dims, int):
        
            plt.figure()
            plt.title('dim'+str(dims))
            sns.regplot(self.data.iloc[:, dims], self.data.iloc[:, 0])
        
        else:
            
            for dim in dims:
                plt.figure()
                plt.title('dim'+str(dim))
                sns.regplot(self.data.iloc[:, dim], self.data.iloc[:, 0])
                
        plt.show()
        
    def __str__(self, filters=('x', 'y', 'e', 'C', 't', 'target')):
        """report
        """
       
            
        return '\n'.join((f"{k}:\n {v}"  for k, v in self.stats_result.items() if k not in filters))
    
    
    def __repr__(self):
        return str(self)
    
    @property
    def report_use_latex(self):
        """使用LaTex格式化报告
        """
        try:
            from IPython.display import display_latex, Math
        except ModuleNotFoundError:
            return self.__str__()
        
        for k, v in self.stats_result.items():
            if k not in self.report_filters:
                print(k)
                if isinstance(v, np.ndarray):
                    display_latex(Math(latex(Matrix(v))))
                else:
                    print(v)        
                print()
        return "repr"
    
    @property
    def report(self):
        """无LaTex公式显示的报告
        """
        print(self.__str__())
        
    @property
    def to_standard(self):
        """标准化后的回归
        """
        return StatsEnv(self.data.loc[:, self.data.columns!='beta0'].apply(standard_scale), 
                        use_bias=False, # 继承当前数据是否使用bias的状态
                        target=self.target,
                        t=self.t)
    
df = pd.read_csv('2-14.csv', encoding='gbk')
s = StatsEnv(df, target='y', t=0.05)
