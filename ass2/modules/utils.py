
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

        list_year.append('{}-01-{}'.format(m, y))

    years_w = pd.to_datetime(list_year)
    return years_w


def to_latex_table(file_name, df, directory=None, index=False, nr_decimals=2):
    """
    Parameters
    ==========
    file_name : name of table (without .tex)
    df : pandas.DataFrame (object) which has to be rendered to latex
    index : should the index of the DataFrame be shown
    """

    df = df.round(nr_decimals)

    if directory is None:
        with open('{}.tex'.format(file_name), 'w') as tf:
            tf.write(df.to_latex(index=index))
    else:
        with open('{}//{}.tex'.format(directory, file_name), 'w') as tf:
            tf.write(df.to_latex(index=index))
