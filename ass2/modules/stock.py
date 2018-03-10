import pandas as pd
import numpy as np
from modules.cleandata import CleanData
import matplotlib.pyplot as plt


# %%


class Stock(object):

    def __init__(self):

        bmit = CleanData.get_data('bmit.csv')
        iait = CleanData.get_data('iait.csv')
        rit = CleanData.get_data('rit.csv')
        momit = CleanData.get_data('momit.csv')

        data = {'bmit': bmit, 'iait': iait, 'rit': rit, 'momit': momit}
        self.data = data

    def return_df(self, kpi):
        """
        Parameters:
        ===========
        kpi (string)

        Returns:
        ========
        df_kpi : pandas dataframe with desired kpi
        """

        kpi_list = [key for key in self.data]
        assert kpi in kpi_list, "kpi i should be one of {}".format(kpi_list)

        return self.data[kpi]

    @staticmethod
    def standardize_data(df):
        std_df = df.std(axis=1)
        mean_df = df.mean(axis=1)
        return df.add(-mean_df, axis=0).mul((1 / std_df), axis=0)  # standardized data

    @staticmethod
    def add_dfs(df1, df2, add_or_minus='add'):

        if add_or_minus == 'add':
            df = pd.DataFrame(df1.fillna(0) + df2.fillna(0))
            df[(df == 0)] = np.nan
        elif add_or_minus == 'minus':
            df = pd.DataFrame(df1.fillna(0) - df2.fillna(0))
            df[(df == 0)] = np.nan
        else:
            raise Exception("add_or_minus should be either 'add' or 'minus' ")

        return df

    def add_data(self, df_name, df):
        self.data[df_name] = df

    def composite_data(self, df1, df2, standardize=True):
        """ add data to self.data

        Parameters
        ==========
        df1 : string (from data)
        df2 : string (from data)
        """

        df_name = "{}_{}".format(df1, df2)
        df1_data = self.return_df(df1)
        df2_data = self.return_df(df2)

        if standardize is True:
            df1_standard = self.standardize_data(df1_data)
            df2_standard = self.standardize_data(df2_data)
            added_dfs = self.add_dfs(df1_standard, df2_standard)
            self.add_data(df_name, added_dfs)

        elif standardize is False:
            added_dfs = self.add_dfs(df1_data, df2_data)
            self.add_data(df_name, added_dfs)

        else:
            raise Exception("standardize must be either True or False")

    def industry_adjusted_data(self, industry):

        assert industry in ['bmit', 'momit'], "industry must be either 'bmit' or 'momit'"

        df_industry = df['iait']
        df_benchmark = df['industry_{}'.format(industry)]
        for i in industry:
            df_temp = df_industry
            df_temp[(df_temp != i)] = np.nan
            df_temp[(df_temp == i)] = 1

    def portfolio_dummy(self, kpi, ascending=True):

        df_kpi = self.return_df(kpi)

        df_rank = df_kpi.rank(axis=1, pct=True, ascending=ascending)
        df_rank[(df_rank < 0.8)] = np.nan
        df_rank[(df_rank > -1)] = 1

        return df_rank

    def portfolio(self, kpi, highlow='high', return_dummy=False):
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

        if highlow is 'high':
            df_dummy = self.portfolio_dummy(kpi, True)
        elif highlow is 'low':
            df_dummy = self.portfolio_dummy(kpi, False)
        elif highlow is 'highlow':
            dummy_high = self.portfolio_dummy(kpi, True)
            dummy_low = self.portfolio_dummy(kpi, False)
            df_dummy = self.add_dfs(dummy_high, dummy_low, add_or_minus='minus')
        else:
            raise Exception("highlow must be either: 'high', 'low', 'highlow'")

        if return_dummy is False:
            return df_rit * df_dummy
        if return_dummy is True:
            return df_rit * df_dummy, df_dummy
