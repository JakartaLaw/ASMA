import pandas as pd
import numpy as np
#from modules.utils import to_latex_table


class Performance(object):

    # avg-return
    # geo-mean
    # std_dev
    # sharpe
    # t_stat

    def __init__(self, portfolio_returns, frequency, risk_free_rate):
        self.portfolio_returns
        self.frequency
        self.risk_free_rate

    @staticmethod
    def avg_return(series, frequency):
        return np.mean(series * frequency)

    @staticmethod
    def std_dev(series, frequency):
        return np.sqrt(np.var(VolatilityTimingPortfolio) * frequency)

    @classmethod
    def sharp_ratio(cls, series, frequency, risk_free_rate):
        ER = cls.avg_return(series, frequency)
        STD = cls.avg_return(series, frequency)
        return (ER - np.mean(risk_free_rate)) / STD

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

    def get_performance(self):
        avg_ret = self.avg_return(self.series, self.frequency)
        std_dev = self.std_dev(self.series, self.frequency)
        t_stat = self.t_statistic(self.series, self.frequency)
        geo_ret = self.geo_return(self.series, self.frequency)

        self.performance = pd.DataFrame({'avg return': avg_ret, 'std. deviation': std_dev})
        return self.performance

    def performance_to_latex(self, file_name):
        #to_latex_table(file_name, self.performance, directory=None, index=False, nr_decimals=2)
        pass
