import pandas as pd
import numpy as np


import pandas as pd
import numpy as np
from modules.cleandata import CleanData
import matplotlib.pyplot as plt


# %%


class IndustryRotation(object):

    def __init__(self):

        bmit = CleanData.get_data('bmit.csv')
        iait = CleanData.get_data('iait.csv')
        rit = CleanData.get_data('rit.csv')
        momit = CleanData.get_data('momit.csv')
        industry_momit = CleanData.get_data('industry_momit.csv', doc_type='Industry')
        industry_bmit = CleanData.get_data('industry_bmit.csv', doc_type='Industry')
        industry_rit = CleanData.get_data('industry_rit.csv', doc_type='Industry')
        factors = CleanData.get_data('data_and_factors.csv', doc_type='Factors')

        data = {'bmit': bmit, 'iait': iait, 'rit': rit, 'momit': momit,
                'industry_momit': industry_momit, 'industry_bmit': industry_bmit, 'factors': factors, 'industry_rit': industry_rit}

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

    def portfolio_dummy(self, kpi, ascending=True):

        kpi = 'industry_{}'.format(kpi)
        industry = self.return_df(kpi)

        df_rank = industry.rank(axis=1, ascending=ascending)
        df_rank[(df_rank > 3)] = np.nan
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

        df_rit = self.return_df('industry_rit')

        if highlow is 'high':
            df_dummy = self.portfolio_dummy(kpi, False)
        elif highlow is 'low':
            df_dummy = self.portfolio_dummy(kpi, True)
        elif highlow is 'highlow':
            dummy_high = self.portfolio_dummy(kpi, False)
            dummy_low = self.portfolio_dummy(kpi, True)
            df_dummy = self.add_dfs(dummy_high, dummy_low, add_or_minus='minus')
        else:
            raise Exception("highlow must be either: 'high', 'low', 'highlow'")

        if return_dummy is False:
            return df_rit * df_dummy
        if return_dummy is True:
            return df_rit * df_dummy, df_dummy
