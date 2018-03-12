from scipy import stats
from modules.performance import Performance
from modules.cleandata import CleanData
import numpy as np
import pandas as pd


class P_Regress(object):
    
    def __init__(self):
       pass
    
 #   @staticmethod
 #   def combine_dicts(first_dict, last_dict):
 #        z = {**first_dict, **last_dict}
 #        return z

    
    @staticmethod
    def data_setup(data, data_type='x', lag_len=12):
        data_list = []
        if data_type == 'y':
            for i in range(lag_len, len(data)):  
                a = Performance.geo_return(data.iloc[i-lag_len:i, 0], 12)
                data_list.append(a)
        elif data_type == 'x':
            for i in range (lag_len, len(data)):
                a = data.iloc[i-lag_len, 0]
                data_list.append(a)
        else:
            raise Exception('data_type must be x or y')
        return data_list
        
        
    @classmethod
    def regressor_loop(cls, x, y):
        a = P_Regress.data_setup(x, data_type='x')
        b = P_Regress.data_setup(y, data_type='y')
        slope, intercept, r_value, p_value, std_err = stats.linregress(a,b)
        n_dict=  {'slope': slope,  'intercept': intercept,
                'r_value': r_value, 'p_value': p_value, 
                'std_error' : std_err}
        return pd.DataFrame.from_dict(n_dict, orient = 'index')

    
  #  @staticmethod
  #  def get_time_index(cutoff=12):
  #      x = CleanData.get_index()
  #      x = x[cutoff:]
  #      x = list(x)
  #      return {'Date': x}
    
  #  @classmethod
  #  def get_df(cls, x, y):
  #      a = P_Regress.get_time_index()
  #      b = P_Regress.regressor_loop(x, y)
  #      c = P_Regress.combine_dicts(a, b)
  #      df = pd.DataFrame.from_dict(c)
  #      return df
    

