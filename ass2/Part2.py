
# coding: utf-8

# # Part 1 - Assignment 2

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as snb

from modules.stock import Stock
from modules.portfolio import Portfolio
from modules.performance import Performance, CollectPerformance
from modules.cleandata import CleanData
from modules.portfolioregress import PortfolioRegress

#get_ipython().magic('matplotlib inline')


# # Preparation

# %% Initiating the Stock-instance


stock = Stock()

# %% Loading once more the returns and performance statistics
# for the high-low portfolio

s, d = stock.portfolio(kpi='bmit', highlow='highlow', return_dummy=True)
p = Portfolio.portfolio_return(s)
perf = Performance(p, 12, d, sum_of_weights=2)
p2 =perf.get_performance('bmit highlow')


# %% adjusting book-to-market data for industry

stock.industry_adjusted_data('bmit')

# %% Loading once more the returns and performance statistics
# for the high-low industry adjusted portfolio

s_i, d_i = stock.portfolio(kpi='adjusted_bmit', highlow='highlow', return_dummy=True)
p_i = Portfolio.portfolio_return(s_i)
perf_i = Performance(p_i, 12, d_i, sum_of_weights=2)
p2_i = perf.get_performance('industry adjusted high/low')

# %% Question 6 answers
 
reg = PortfolioRegress.regressor_loop(p, p, index_name=
                                'High-Low', standardize=True)
reg_i = PortfolioRegress.regressor_loop(p_i, p_i, index_name=
                                'High-Low ind. adjusted', standardize=True)
frames = [reg, reg_i]
q6 = pd.concat(frames)
# %% Question 7 answers

p_indicator = PortfolioRegress.indicator_func(p)
reg_2 = PortfolioRegress.regressor_loop(p_indicator, p, index_name=
                                'Performance Statistics', lag_x=0)
p_i_indicator = PortfolioRegress.indicator_func(p_i)
reg_2_i = PortfolioRegress.regressor_loop(p_i_indicator, p_i, index_name=
                                'Performance Statistics', lag_x=0)
frames = [reg_2, reg_2_i]
q7 = pd.concat(frames)
# %% Question 8 - start



