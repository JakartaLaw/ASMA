from scipy import stats
from modules.performance import Performance
from modules.cleandata import CleanData
import numpy as np
import pandas as pd


class PortfolioRegress(object):
    
    def __init__(self):
       pass
  
    @staticmethod
    """
    Processes the data such that the regressand will be an average of 12
    subsequent observations and the regressor will be the preliminary obs.
    of the y (used for Q6)
    """
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
    
    @staticmethod
    """
    Standardizes the input variable s.t. mu = 0, sigma = 1 (used in Q6)
    """
    def standardize_data(data):
        std_list = []
        std_dev = Performance.std_dev(data, 1)
        avg_data = Performance.avg_return(data, 1)
        for i in range(len(data)):
            std_obs = (data[i] - avg_data)/std_dev
            std_list.append(std_obs)
        return std_list
        
    @classmethod
    """
    Custom made indicator function that assigns 1's to observations with
    high historical VS and 0 to the rest (used in Q7)
    """
    def indicator_func(cls, data, insample=12):
        indicator_list = []
        a = PortfolioRegress.data_setup(data, data_type='x', lag_len=12-insample)
        for i in range(insample, len(data)):
            if a[i] > np.mean(a[i-insample:i-1]):
                indicator = 1
            else:
                indicator = 0
            indicator_list.append(indicator)
        return pd.DataFrame(indicator_list)
        
    @classmethod
    """
    Executes the linear regression on the pre-cleaned data (OLS method)
    """
    def regressor_loop(cls, x, y, index_name, standardize=False, lag_x = 12, lag_y = 12):
        a = PortfolioRegress.data_setup(x, data_type='x', lag_len=lag_x)
        b = PortfolioRegress.data_setup(y, data_type='y', lag_len=lag_y)
        if standardize ==True:
            a = PortfolioRegress.standardize_data(a)
        else:
            pass
        slope, intercept, r_value, p_value, std_err = stats.linregress(a,b)
        n_dict=  {'slope': slope,  'intercept': intercept,
                'r_value': r_value, 'p_value': p_value, 
                'std_error' : std_err}
        return pd.DataFrame(n_dict, index = [index_name])
    
    

            
