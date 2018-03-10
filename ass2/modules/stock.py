import pandas as pd
import numpy as np
from modules.cleandata import CleanData
import matplotlib.pyplot as plt

%matplotlib inline

# %%


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
        """Depreciated"""

        list_of_cols = list(self.bmit.columns)
        stocks = dict()

        for i in list_of_cols:
            stocks[i] = self.create_stock(i)

        self.stocks = stocks
        return stocks

    def portfolio(Self, kpi):


test = Stock()
stocks


# %%

# %%
StockPicker.rank_stocks(stocks, 'bmit').head()

# %%
a = pd.Series([1, 2, 3])
b = pd.Series([2, 3, 4])

pd.DataFrame(data=[a, b])
