import pandas as pd
import numpy as np
from modules.utils import to_latex_table


class Performance(object):

    # avg-return
    # geo-mean
    # std_dev
    # sharpe
    # t_stat

    def __init__(self, portfolio_returns, frequency, dummy=None):
        self.portfolio_returns = portfolio_returns
        self.frequency = frequency
        self.dummy = dummy

    @staticmethod
    def avg_return(series, frequency):
        return np.mean(series * frequency)

    @staticmethod
    def std_dev(series, frequency):
        return np.sqrt(np.var(series) * frequency)

    @classmethod
    def sharp_ratio(cls, series, frequency):
        ER = cls.avg_return(series, frequency)
        STD = cls.std_dev(series, frequency)
        return ER / STD

    @staticmethod
    def t_statistic(series, frequency):

        beta = np.mean(series) * frequency
        sigma = np.std(series) * np.sqrt(frequency)
        sqrt_n = np.sqrt(len(series))

        sigma_beta = sigma / sqrt_n

        return beta / sigma_beta

    @staticmethod
    def geo_return(series, frequency):
        product_array = np.array([i + 1 for i in series])
        return np.prod(product_array)**(frequency / len(series)) - 1

    @staticmethod
    def average_number_of_months(dummy):
        if dummy is None:
            return None
        else:
            return np.mean(dummy.count(axis=0))

    def get_performance(self, name):
        avg_ret = self.avg_return(self.portfolio_returns, self.frequency)
        std_dev = self.std_dev(self.portfolio_returns, self.frequency)
        sharp_ratio = self.sharp_ratio(self.portfolio_returns, self.frequency)
        t_stat = self.t_statistic(self.portfolio_returns, self.frequency)
        geo_ret = self.geo_return(self.portfolio_returns, self.frequency)
        count_months = self.average_number_of_months(self.dummy)

        if count_months is None:
            performance = pd.DataFrame(
                {'avg return': avg_ret, 'std. deviation': std_dev, 'sharpe ratio': sharp_ratio, 't-stat': t_stat})
        else:
            performance = pd.DataFrame(
                {'avg return': avg_ret, 'std. deviation': std_dev, 'sharpe ratio': sharp_ratio, 't-stat': t_stat, 'avg months for stock': count_months})

        performance['index_name'] = name
        performance.set_index(['index_name'], inplace=True)
        self.performance = performance
        return self.performance

    def performance_to_latex(self, file_name, decimals=3):
        to_latex_table(file_name, self.performance, directory=None,
                       index=True, nr_decimals=decimals)


class CollectPerformance(object):

    def __init__(self, performance_list):
        self.performance_list = performance_list

    def __call__(self):
        self.performance_concat()
        return self.performance

    def performance_concat(self):
        self.performance = pd.concat(self.performance_list)

    def performance_to_latex(self, file_name, decimals=3):
        to_latex_table(file_name, self.performance, directory=None,
                       index=True, nr_decimals=decimals)
