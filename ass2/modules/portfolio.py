class Portfolio(object):
    """
    Takes a list of period-wise returns of different stocks and converts them into a portfolio return
    """
    
    def __init__(self):
        pass
    
    def portfolio_weigths(self, df):
        _list = []
        for i in range(len(df)):
            w = 1/df.count(axis=1)[i]
            _list.append(w)
        return _list
    
    @classmethod
    def period_return(cls, df):
        _portfolio = df.sum(axis=1)
        _w = cls.portfolio_weigths(cls, df)
        new_list = [_w[i]*_portfolio[i] for i in range(len(_w))]
        new_df = pd.DataFrame(new_list, index=df.index)
        return new_df
            

#### test ####
#import pandas as pd
#import numpy as np
#df = pd.DataFrame([[1,2,3,np.nan],[np.nan,3,2,3]])
#print(df.count(axis=1)[0])
#ny = Portfolio()
#a = list(df.sum(axis=1))
#b = ny.portfolio_weigths(df)
#new_list = [a[i]*b[i] for i in range(len(a))]
#res = ny.period_return(df)
        
    