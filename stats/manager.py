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

import seaborn as sns
from math import sqrt
import pandas as pd
from sympy import init_printing, Matrix, latex

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
                 t=0.025,
                 use_bias=True,
                 digit=3,
                 report_filters=('x', 'y', 'e', 'C', 't', 'target', 'data', 'use_bias', 'digit')):
        if data.columns[0] != target:
            data = data.loc[:, [target, *[column for column in data.columns if column != target]]]
        if use_bias:
            data['beta0'] = np.ones(data.shape[0])

        self.use_bias = use_bias
        self.digit = digit
        self.data = data
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

        SST = sum(np.square(y - np.mean(y)))

        R2 = 1 - SSE / SST
        coef_stderrs = (np.sqrt(C.diagonal()) * stderr)
        t_stats = coef / coef_stderrs
        t_bound = stats.t.cdf(t_stats, n - p)
        
        interval = list(zip(*map(lambda _: _.round(digit), 
                                 stats.t.interval(t, n - p, coef, coef_stderrs))))

        checked_pass = t_bound > 1 - t
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
            t_bound=t_bound,
            stderr=stderr,
            SST=SST,
            SSE=SSE,
            R2=R2,
            interval=interval,
            checked_pass=checked_pass)
        self.context = ReadonlyDict(self.stats_result)

    
    @property
    def context_format(self):
        def format_df(x, columns=None):
            m, n = x.shape
            x.columns = columns if columns else ['']*n
            x.index = ['']*m
            return x
        context = self.context
        return dict(     
                coef=format_df(pd.DataFrame([context.data.columns[1:], context.coef]).T, ['coef for', 'value']),
                equ=context.target +
                ' = ' +
                ' + '.join([f'{c}*{1 if name =="beta0" else name}'
                            for c, name in zip(context.coef.round(context.digit), 
                                               context.data.columns[1:])]),
    
                C=context.C.round(context.digit),
                e=context.e.round(context.digit),
                r=context.r.round(context.digit),
                t_stats=context.t_stats.round(context.digit),
                t_bound=context.t_bound.round(context.digit),
                stderr=round(context.stderr, context.digit),
                SST=round(context.SST, context.digit),
                SSE=round(context.SSE, context.digit),
                R2=round(context.R2, context.digit),
                
                interval=format_df(pd.DataFrame([context.data.columns[1:], context.interval]).T, ['coef for', '(inf, sup)']),
                checked_pass=format_df(pd.DataFrame([context.data.columns[1:], context.checked_pass]).T, ['coef for', 'is_passed']))

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
    
    def predict(self, samples):
        
        coef = self.stats_result['coef']
        
        def _pred(x):
            if self.use_bias:
                return np.dot(x, coef[:-1]) + coef[-1]
            else:
                return np.dot(x, coef)
        
        if samples.ndim is 1:
            return _pred(samples)
        else:
            return np.vectorize(_pred)(samples)
            

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
        return StatsEnv(context.data.loc[:, context.data.columns != 'beta0'].apply(standard_scale),
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
        
        

df = pd.read_csv('2-16.csv', encoding='gbk')
s = StatsEnv(df, target='y', t=0.025, digit=5)
print(s)
print()
print(s.to_standard.stats_result['r'])
#print(s.to_standard)
# s.plot([1, 2, 3])
# print(s.to_standard)

# sns.distplot(s.context.e)
# stats.probplot(s.context.e, plot=plt)


