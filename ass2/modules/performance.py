import pandas as pd

class Performance(object):
    
    def __init__(self):
        pass
    
    def geo_return(self, df):
        my_list = []
        for i in range(len(df[0])):
            _rr = df[0][i]+1
            my_list.append(_rr)
        _n = df[0].count()
        geo_return = np.prod(np.array(my_list))**(1/_n) -1
        return geo_return 
        
    def ar_return(self, df):
        _sum = df[0].sum()
        _n = df[0].count()
        return _sum/_n
    

