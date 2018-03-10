def create_stock(self, n_stock):

    bmit, iait, rit, momit = self.bmit[n_stock], self.iait[n_stock], self.rit[n_stock], self.momit[n_stock]

    stock = pd.concat([bmit, iait, rit, momit], axis=1)
    stock.columns = self.kpi_list

    return stock

def all_stocks(self):
    """Depreciated"""

    list_of_cols = list(self.bmit.columns)
    stocks = dict()

    for i in list_of_cols:
        stocks[i] = self.create_stock(i)

    self.stocks = stocks
    return stocks
