from scipy import stats
from modules.performance import Performance
from modules.cleandata import CleanData
import numpy as np
import pandas as pd


class P_regress(object):
    
    def __init__(self):
       pass
    
    @staticmethod
    def combine_dicts(first_dict, last_dict):
         z = {**first_dict, **last_dict}
         return z
    
    @staticmethod
    def data_setup(data, data_type='x', lag_len=12):
        data_list = []
        if data_type == 'y':
            for i in range(lag_len, len(data)):  
                a = Performance.geo_return(data.iloc[i-lag_len:i, 0], 12)
                data_list.append(a)
        if data_type == 'x':
            for i in range (lag_len, len(data)):
                a = data.iloc[i-lag_len, 0]
                data_list.append(a)
        else:
            raise Exception('data_type must be x or y')
        return data_list
        
        
    @classmethod
    def regressor_loop(cls, x, y):
        slope_list, intercept_list = [], []
        r_value_list, p_value_list, std_err_list =  [], [], []
        a = P_regress.data_setup(x, data_type='x')
        b = P_regress.data(y, data_type='y')
        for i in range(len(x)):
            slope, intercept, r_value, p_value, std_err = stats.linregress(a,b)
            slope_list.append(slope)
            intercept_list.append(intercept)
            r_value_list.append(r_value)
            p_value_list.append(p_value)
            std_err_list.append(std_err)
        return {'slope': slope_list,  'intercept': intercept_list,
                'r_value': r_value_list, 'p_value': p_value_list, 
                'std_error' : std_err_list}

    
    @staticmethod
    def get_time_index(cutoff=12):
        x = CleanData.get_index()
        x = x.iloc[cutoff:, :]
        return {'Date', x}
    
    @classmethod
    def get_df(cls, x, y):
        a = P_regress.get_time_index()
        b = P_regress.regressor_loop(x, y)
        c = P_regress.combine_dicts(a, b)
        df = pd.DataFrame.from_dict(c)
        return df


