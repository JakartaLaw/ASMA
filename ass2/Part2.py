
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

# In[2]:


stock = Stock()


# # Question 1.1 - 1.2

# ### bmit




# In[5]:


s, d = stock.portfolio(kpi='bmit', highlow='highlow', return_dummy=True)
p = Portfolio.portfolio_return(s)
perf = Performance(p, 12, d, sum_of_weights=2)
p2 =perf.get_performance('bmit highlow')






# In[10]:


stock.composite_data('bmit', 'momit')

# In[13]:


s, d = stock.portfolio(kpi='bmit_momit', highlow='highlow', return_dummy=True)
p = Portfolio.portfolio_return(s)
perf = Performance(p, 12, d)
p2 = perf.get_performance('composite high/low')



# In[15]:


stock.industry_adjusted_data('bmit')
stock.industry_adjusted_data('momit')
stock.composite_data('adjusted_bmit', 'adjusted_momit')



# In[18]:


s, d = stock.portfolio(kpi='adjusted_bmit_adjusted_momit', highlow='highlow', return_dummy=True)
p = Portfolio.portfolio_return(s)
perf = Performance(p, 12, d)
p2 = perf.get_performance('composite adjusted high/low')

# %%
 
reg = PortfolioRegress.regressor_loop(p, p, index_name='Performance statistics', standardize=True)

# %%
p_indicator = PortfolioRegress.indicator_func(p)
reg_2 = PortfolioRegress.regressor_loop(p_indicator, p, index_name='Performance Statistics', lag_x=0)

