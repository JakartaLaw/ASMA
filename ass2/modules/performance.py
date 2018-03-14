import pandas as pd
import numpy as np
from modules.utils import to_latex_table


class Performance(object):

    # avg-return
    # geo-mean
    # std_dev
    # sharpe
    # t_stat

    def __init__(self, portfolio_returns, frequency, dummy=None, sum_of_weights=1):
        self.portfolio_returns = portfolio_returns
        self.frequency = frequency
        self.dummy = dummy
        self.sum_of_weights = sum_of_weights

    @staticmethod
    def avg_return(series, frequency, sum_of_weights=1):
        """
        Returns the arithmetic mean
        """
        return np.mean(series * frequency) * sum_of_weights

    @staticmethod
    def std_dev(series, frequency, sum_of_weights=1):
        return np.sqrt(np.var(series) * frequency) * sum_of_weights

    @classmethod
    def sharpe_ratio(cls, series, frequency, sum_of_weights=1):
        ER = cls.avg_return(series, frequency, sum_of_weights)
        STD = cls.std_dev(series, frequency, sum_of_weights)
        return ER / STD

    @classmethod
    def t_statistic(cls, series, frequency):

        beta = cls.avg_return(series, frequency)
        sigma = cls.std_dev(series, frequency)
        sqrt_n = np.sqrt(len(series))

        sigma_beta = sigma / sqrt_n

        return beta / sigma_beta

    @staticmethod
    def geo_return(series, frequency):
        product_array = np.array([i + 1 for i in series])
        return np.prod(product_array)**(frequency / len(series)) - 1

    @staticmethod
    def average_number_of_months(dummy):
        """
        Returns the average number of months a stock is in a given portfolio
        """
        if dummy is None:
            return None
        else:
            return np.mean(dummy.count(axis=0))

    def get_performance(self, name):
        """
        Function made for nice print-out options
        """
        avg_ret = self.avg_return(self.portfolio_returns, self.frequency, self.sum_of_weights)
        std_dev = self.std_dev(self.portfolio_returns, self.frequency, self.sum_of_weights)
        sharpe_ratio = self.sharpe_ratio(
            self.portfolio_returns, self.frequency, self.sum_of_weights)
        t_stat = self.t_statistic(self.portfolio_returns, self.frequency)
        geo_ret = self.geo_return(self.portfolio_returns, self.frequency)
        count_months = self.average_number_of_months(self.dummy)

        if count_months is None:
            performance = pd.DataFrame(
                {'avg return': avg_ret, 'std. deviation': std_dev, 'sharpe ratio': sharpe_ratio, 't-stat': t_stat})
        else:
            performance = pd.DataFrame(
                {'avg return': avg_ret, 'std. deviation': std_dev, 'sharpe ratio': sharpe_ratio, 't-stat': t_stat, 'avg months for stock': count_months})

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
