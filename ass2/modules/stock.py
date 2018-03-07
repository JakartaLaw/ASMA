import pandas as pd
import numpy as np
from modules.cleandata import CleanData


class Stock(object):

    def __init__(self):

        self.bmit = CleanData.get_data('bmit.csv')
        self.iait = CleanData.get_data('iait.csv')
        self.rit = CleanData.get_data('rit.csv')
        self.momit = CleanData.get_data('momit.csv')

    def create_stock(self, n_stock):

        bmit, iait, rit, momit = self.bmit[n_stock], self.iait[n_stock], self.rit[n_stock], self.momit[n_stock]

        stock = pd.concat([bmit, iait, rit, momit], axis=1)
        stock.columns = ['bmit', 'iait', 'rit', 'momit']

        return stock

    def all_stocks(self):

        list_of_cols = list(self.bmit.columns)
        stocks = dict()

        for i in list_of_cols:
            stocks[i] = self.create_stock(i)

        self.stocks = stocks
        return stocks

    @staticmethod
    def get_stock(stocks, stock, time, kpi=None):

        if kpi is None:
            s = stocks[stock]
            return s.loc[s.index[time]]
        else:
            s = stocks[stock]
            return s[kpi].loc[s.index[time]]

    @classmethod
    def rank_stock_at_t(cls, stocks, time, kpi):

        list_stocks = [stock for stock in stocks]
        list_kpi = np.array([cls.get_stock(stocks, stock, time, kpi) for stock in stocks])

        return list_kpi

    def rank_stocks(self, kpi):
        stocks = self.stocks


test = Stock()
stocks = test.all_stocks()


s = stocks[9]

# %%
print(s.head())

test2 = Stock.rank_stock_at_t(stocks, 4, 'bmit')

test.bmit
