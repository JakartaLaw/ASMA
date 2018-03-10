import pandas as pd
import numpy as np

class Portfolio(object):
    """
    Takes a list of period-wise returns of different stocks and converts them into a portfolio return
    """
    
    @staticmethod
    def portfolio_weigths(df):
        _list = []
        for i in range(len(df)):
            w = 1/df.count(axis=1)[i]
            _list.append(w)
        return _list
    
    @classmethod
    def period_return(cls, df):
        _portfolio = df.sum(axis=1)
        _w = cls.portfolio_weigths(df)
        new_list = [_w[i]*_portfolio[i] for i in range(len(_w))]
        new_df = pd.DataFrame(new_list, index=df.index)
        return new_df
    
    def __init__(self, df):
        self.df_portfolio = self.period_return(df)
        
    def get_portfolio(self):
        return self.df_portfolio
            
