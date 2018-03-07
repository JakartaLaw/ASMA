
def date_fixer(x):
    import pandas as pd
    """
    x = column of dates formatted yyyymm
    """
    
    list_year = []
    for i in range(len(x)):
        s = str(x[i])
        y = s[0:4]
        m = s[4:6]
    
        list_year.append('{}-01-{}'.format(m,y))

    years_w = pd.to_datetime(list_year)
    return years_w

