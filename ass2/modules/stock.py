import pandas as pd
import numpy as np
from modules.cleandata import CleanData
import matplotlib.pyplot as plt


# %%


class Stock(object):

    """
    Initiates a stock object:

    """

    def __init__(self):

        bmit = CleanData.get_data('bmit.csv')
        iait = CleanData.get_data('iait.csv')
        rit = CleanData.get_data('rit.csv')
        momit = CleanData.get_data('momit.csv')
        industry_momit = CleanData.get_data('industry_momit.csv', doc_type='Industry')
        industry_bmit = CleanData.get_data('industry_bmit.csv', doc_type='Industry')
        factors = CleanData.get_data('data_and_factors.csv', doc_type='Factors')

        data = {'bmit': bmit, 'iait': iait, 'rit': rit, 'momit': momit,
                'industry_momit': industry_momit, 'industry_bmit': industry_bmit, 'factors': factors}

        self.data = data

    def __repr__(self):

        data_names = [key for key in self.data]
        return str(data_names)

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
        """
        Standardizes data with mean zero, and std. dev 1
        """
        std_df = df.std(axis=1)
        mean_df = df.mean(axis=1)
        return df.add(-mean_df, axis=0).mul((1 / std_df), axis=0)  # standardized data

    @staticmethod
    def add_dfs(df1, df2, add_or_minus='add'):
        """
        Can add two dataframes together
        """

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
        """
        adds dataframe to dictionary containing all dataframes
        """
        self.data[df_name] = df

    def composite_data(self, df1, df2, standardize=True):
        """
        Function that takes two dataframes, and make a composite portfolio
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

    @staticmethod
    def empty_df(df):
        """
        Creates and empty dataframe, based on the dimensions of the input dataframe
        """

        index, cols, shape = df.index, df.columns, df.shape
        array_nan = np.empty(shape).fill(np.nan)
        df_nan = pd.DataFrame(array_nan, index=index, columns=cols)
        return df_nan

    @staticmethod
    def industry_adjustment(df_industry, df_benchmark, industry):

        df_industry[(df_industry != industry)] = np.nan
        df_industry[(df_industry == industry)] = 1
        return df_industry.mul(df_benchmark, axis=0)

    def industry_adjusted_data(self, industry):
        """
        Industry adjust data and adds it to the dictionary containing all dataframes
        """

        assert industry in ['bmit', 'momit'], "industry must be either 'bmit' or 'momit'"

        df_industry = self.data[industry]
        df_iait = self.data['iait']
        df_benchmark = self.data['industry_{}'.format(industry)]
        industry_list = df_benchmark.columns
        df_name = "adjusted_{}".format(industry)

        df_merge = self.empty_df(df_industry)

        for i in industry_list:

            df_industry_temp = pd.DataFrame(df_iait, copy=True)
            df_temp = self.industry_adjustment(df_industry_temp, df_benchmark[i], industry=i)
            df_merge = self.add_dfs(df_merge, df_temp, add_or_minus='add')

        df_industry_adjusted = self.add_dfs(df_industry, df_merge, add_or_minus='minus')
        self.add_data(df_name, df_industry_adjusted)

    def industry_dummy(self, kpi, ascending=True):
        """
        Creates dummy for a given industry
        """

        kpi_data = "industry_{}".format(kpi)
        industry = self.return_df(kpi_data)

        df_rank = industry.rank(axis=1, ascending=ascending)
        df_rank[(df_rank > 3)] = np.nan
        df_rank[(df_rank > -1)] = 1

        return df_rank

    def portfolio_dummy(self, kpi, ascending=True, pct=True):
        """
        Function that returns a dummy = 1 for given observations, that have an
        good enough rank
        """

        df_kpi = self.return_df(kpi)

        df_rank = df_kpi.rank(axis=1, pct=pct, ascending=ascending)
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
