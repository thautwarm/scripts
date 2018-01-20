# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 22:46:42 2018

@author: misakawa
"""

import numpy as np
from scipy import stats
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus']=False
import matplotlib.pyplot as plt
from pipe_fn import and_then

import seaborn as sns
from math import sqrt
import pandas as pd
from sympy import Matrix, latex
from numbers import Number
from collections import Iterable

np.set_printoptions(suppress=True)
#init_printing()


def standard_scale(x):
    x = x - np.mean(x)
    if all(x == 0):
        return np.zeros(x.shape)
    return x / np.linalg.norm(x)

class ReadonlyDict:
    def __init__(self, _context):
        self._context = _context
    def __getattr__(self, k):
        return self._context[k]


class StatsEnv:
    def __init__(self,
                 data: pd.DataFrame,
                 target: str,
                 t=0.05,
                 use_bias=True,
                 digit=3,
                 standard_recovery = None,
                 report_filters=('x', 'y', 'e', 'C', 't', 'target', 'data', 'use_bias', 'digit')):
        if data.columns[0] != target:
            data = data.loc[:, [target, *[column for column in data.columns if column != target]]]
        if use_bias:
            data['beta0'] = np.ones(data.shape[0])

        self.use_bias = use_bias
        self.digit = digit
        self.data = data
        self.standard_recovery = standard_recovery
        self.target = target
        self.t = t
        self.report_filters = report_filters
        
        n, p = data.shape

        p -= 1

        x = data.loc[:, data.columns != target].values
        y = data[target].values
        coef, _, *_ = np.linalg.lstsq(x, y)

        C = np.linalg.inv(np.dot(x.T, x))  # c_ij matrix

        e = y - np.dot(x, coef)

        SSE = sum(np.square(e))

        stderr = sqrt(SSE / (n - p))

        mean_y = np.mean(y)
        SST = sum(np.square(y - mean_y))
        
        SSR = SST - SSE
        R2 = SSR / SST
        
        coef_stderrs = (np.sqrt(C.diagonal()) * stderr)
        
        t_stats = coef / coef_stderrs
        f_stats = (SSR/(p-1))/(SSE/(n-p))
        
        t_bound = stats.t.cdf(t_stats, n - p -1)
        f_bound = stats.f.cdf(f_stats, p, n - p - 1)
        
        
        interval = list(zip(*map(lambda _: _.round(digit), 
                                 stats.t.interval(t, n - p, coef, coef_stderrs))))

        equ_checked_pass = f_bound > 1 - t
        coef_checked_pass = t_bound > 1 - t
        
        r = np.dot(data.T, data)  # 相关系数
        self.stats_result = dict(     
            # 初始化配置
            data=data,
            use_bias=use_bias,
            target=target,
            t=t,
            digit=digit,
            
            # 统计结果
            coef=coef,
            C=C,
            e=e,
            r=r,
            t_stats=t_stats,
            f_stats=f_stats,
            t_bound=t_bound,
            f_bound=f_bound,
            stderr=stderr,
            SST=SST,
            SSE=SSE,
            R2=R2,
            interval=interval,
            coef_checked_pass=coef_checked_pass,
            equ_checked_pass=equ_checked_pass)
        self.context = ReadonlyDict(self.stats_result)

    
    @property
    def context_format(self):
        def format_df(x, columns=None):
            m, n = x.shape
            x.columns = columns if columns else ['']*n
            x.index = ['']*m
            return x
        context = self.context
        digit = context.digit
        return dict(     
                coef=format_df(pd.DataFrame([context.data.columns[1:], context.coef]).T, ['coef for', 'value']),
                equ=context.target +
                ' = ' +
                ' + '.join([f'{c}*{1 if name =="beta0" else name}'
                            for c, name in zip(context.coef.round(digit), 
                                               context.data.columns[1:])]),
    
                C=context.C.round(digit),
                e=context.e.round(digit),
                r=context.r.round(digit),
                t_stats=context.t_stats.round(digit),
                t_bound=context.t_bound.round(digit),
                f_stats=context.f_stats.round(digit),
                f_bound=context.f_bound.round(digit),
                stderr=round(context.stderr, digit),
                SST=round(context.SST, digit),
                SSE=round(context.SSE, digit),
                R2=round(context.R2, digit),
                
                equ_checked_pass = context.equ_checked_pass,
                interval=format_df(pd.DataFrame([context.data.columns[1:], context.interval]).T, ['coef for', '(inf, sup)']),
                coef_checked_pass=format_df(pd.DataFrame([context.data.columns[1:], context.coef_checked_pass]).T, ['coef for', 'is_passed']))

    def plot(self, dims: np.ndarray = 1, residual=True, regression=True):
        """
        画图
        """
        
        if isinstance(dims, int):

            plt.figure()
            plt.title('dim' + str(dims))
            x, y = self.data.iloc[:, dims], self.data.iloc[:, 0]
            if regression:
                sns.regplot(x, y, label='x-y')
            if residual:
                sns.residplot(x, y, label='x-residual')
            plt.legend()

        else:

            for dim in dims:
                plt.figure()
                plt.title('dim' + str(dim))
                x, y = self.data.iloc[:, dim], self.data.iloc[:, 0]
                if regression:
                    sns.regplot(x, y, label='x-y')
                if residual:
                    sns.residplot(x, y, label='x-residual')
                plt.legend()

        plt.show()
    
    def predict(self, samples, confidence: float=False):
        if isinstance(samples, Number):
            samples = np.array((samples,))
        elif isinstance(samples, Iterable) and not isinstance(samples, np.ndarray):
            samples = np.array(tuple(samples))
        else:
            raise TypeError(f'Invalid type `{samples.__class__}`')
        
        
        if self.standard_recovery is not None:
            scale = True
        else:
            scale = False
        
        if scale:
            mean, norm = self.standard_recovery
            samples = (samples - mean)/norm
            


        coef = self.stats_result['coef']
        
        def _pred(x):
            if self.use_bias:
                return np.dot(x, coef[:-1]) + coef[-1]
            else:
                return np.dot(x, coef)
        
        if samples.ndim is 1:
            prediction = _pred(samples)

        else:
            prediction = np.vectorize(_pred)(samples)
        
        if scale:
            prediction = prediction*norm + mean
                    
        if confidence is not False:
            return prediction, stats.norm.interval(1-confidence, prediction, self.context.stderr)
        return prediction
            

    def __str__(self):
        """report
        """
        return '\n\n'.join((f"{k}:\n\n {v}" for k, v in self.context_format.items() if k not in self.report_filters))

    def __repr__(self):
        return str(self)

    @property
    def report_use_latex(self):
        """使用LaTex格式化报告
        """
        try:
            from IPython.display import display_latex, Math
            from sympy import init_printing
            init_printing()
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
        context = self.context
        data = context.data.loc[:, context.data.columns != 'beta0']
        return StatsEnv(data.agg(standard_scale),
                        standard_recovery=(
                                (lambda _: (
                                        lambda mean, df: (
                                                mean, np.linalg.norm(df-mean, axis=0))
                                        )(_.mean(0), _)))(data.values),
                        use_bias=False,  # 继承当前数据是否使用bias的状态
                        target=context.target,
                        t=context.t)

    def normal_probability_plot(self, by: str):
        this = getattr(self.context, by)
        
        plt.subplot(311)
        
        plt.title(by+'分布直方图')
        sns.distplot(this)
    
        plt.subplot(313)
        stats.probplot(this, plot=plt)
        
        

df = pd.read_csv('happiness.csv', encoding='gbk')
cols = df.dtypes.map(lambda x: issubclass(x.type, np.floating))
cols = (df.columns!='Standard Error') & cols
COL1 = ['Economy (GDP per Capita)', 'Health (Life Expectancy)']
df = df.loc[:, COL1]
s = StatsEnv(df, target='Health (Life Expectancy)', t=0.05, digit=8)
#print(s)
#coef_checked_pass = s.stats_result['coef_checked_pass']
#df = df[[df.columns[0], *df.columns[1:][coef_checked_pass]]]
#s = StatsEnv(df, target='货运总量', t=0.05, digit=5)
print(s)
print()
#s.to_standard.report_use_latex
#print(s.to_standard)
# s.plot([1, 2, 3])
# print(s.to_standard)

# sns.distplot(s.context.e)
# stats.probplot(s.context.e, plot=plt)


