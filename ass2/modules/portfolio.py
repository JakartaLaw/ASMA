import pandas as pd
import numpy as np


class Portfolio(object):
    """
    Takes a list of period-wise returns of different stocks and converts 
    them into a portfolio return
    """

    @staticmethod
    """
    Assigns weights to the chosen stocks in the portfolio. 
    All stocks are equally weighted for this assignment
    """
    def portfolio_weigths(df, sum_of_weights):
        _list = []
        for i in range(len(df)):
            w = sum_of_weights / df.count(axis=1)[i]
            _list.append(w)
        return _list

    @classmethod
    """
    Takes the weigted portfolio as input and computes the monthly return
    """
    
    def portfolio_return(cls, df, sum_of_weights=1):
        _portfolio = df.sum(axis=1)
        _w = cls.portfolio_weigths(df, sum_of_weights=sum_of_weights)
        new_list = [_w[i] * _portfolio[i] for i in range(len(_w))]
        new_df = pd.DataFrame(new_list, index=df.index)
        return new_df

    @staticmethod
    """
    Takes two portfolios and weights them 50/50 into a new portfolio
    """
    def fifty_fifty(return1, return2):
        combined = return1.add(other=return2)
        weighted = combined.multiply(other=0.5)
        return weighted
