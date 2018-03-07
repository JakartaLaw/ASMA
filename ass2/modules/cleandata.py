import pandas as pd
import numpy as np
from datetime import datetime


class CleanData(object):

    @staticmethod
    def get_index():

        data = pd.read_csv('data_and_factors.csv', sep=';', decimal=',',
                           header=None, usecols=[0, 1, 2, 3, 4, 5])
        data.columns = ['date', 'MKT', 'SMB', 'HML', 'WML', 'Tbillrate']
        #data.set_index('date', inplace=True)

        return data

    @classmethod
    def get_data(cls, csv_name):
        index = cls.get_index()

        data = pd.read_csv(csv_name, sep=';', decimal=',',
                           header=None)

        #data.set_index(index, inplace=True)
        return data


#data = CleanData.get_data('bmit.csv')
data = CleanData.get_index()
data.head()
pd.to_datetime(str(data['date']), format='%Y%m')
