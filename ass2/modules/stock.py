import pandas as pd
import numpy as np
from modules.cleandata import CleanData
import matplotlib.pyplot as plt


# %%


class Stock(object):

    def __init__(self):

        self.bmit = CleanData.get_data('bmit.csv')
        self.iait = CleanData.get_data('iait.csv')
        self.rit = CleanData.get_data('rit.csv')
        self.momit = CleanData.get_data('momit.csv')
        self.kpi_list = ['bmit', 'iait', 'rit', 'momit']

    def create_stock(self, n_stock):

        bmit, iait, rit, momit = self.bmit[n_stock], self.iait[n_stock], self.rit[n_stock], self.momit[n_stock]

        stock = pd.concat([bmit, iait, rit, momit], axis=1)
        stock.columns = self.kpi_list

        return stock

    def all_stocks(self):
        """Depreciated"""

        list_of_cols = list(self.bmit.columns)
        stocks = dict()

        for i in list_of_cols:
            stocks[i] = self.create_stock(i)

        self.stocks = stocks
        return stocks

    def return_df(self, kpi):
        """
        Parameters:
        ===========
        kpi (string)

        Returns:
        ========
        df_kpi : pandas dataframe with desired kpi
        """

        assert kpi in self.kpi_list, "kpi i should be one of {}".format(self.kpi_list)

        # grim implementation
        if kpi == 'bmit':
            return self.bmit
        if kpi == 'rit':
            return self.rit
        if kpi == 'momit':
            return self.momit
        if kpi == 'iait':
            return self.iait

    def portfolio_dummy(self, kpi, ascending=True):

        # grim implementation

        df_kpi = self.return_df(kpi)

        df_rank = df_kpi.rank(axis=1, pct=True, ascending=ascending)
        df_rank[(df_rank <= 0.8)] = np.nan

        df_dummy = df_rank
        df_dummy[(df_dummy > -1)] = 1
        return df_dummy

    def portfolio(self, kpi, ascending_performance=True, return_dummy=False):
        """
        Parameters:
        ===========
        kpi : (string)
        ascending_performance : (Boolean)
        return_dummy : (boolean) --> whether or not to return the dataframe with dummy variables

        Returns
        =======
        df_rit * df_dummy, (df_dummy) --> if df_dummy==True
        """

        df_rit = self.return_df('rit')
        df_dummy = self.portfolio_dummy(kpi, ascending_performance)
        if return_dummy is False:
            return df_rit * df_dummy
        if return_dummy is True:
            return df_rit * df_dummy, df_dummy
