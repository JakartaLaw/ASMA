# StockPicker class should be transfered in here when done
# Should not be used as class


class StockPicker(object):

    @staticmethod
    def get_stock(stocks, stock, time=None, kpi=None):

        s = stocks[stock]

        if kpi is None:
            if time is None:
                return s
            else:
                return s.loc[s.index[time]]

        else:
            if time is None:
                return s[kpi]
            else:
                return s[kpi].loc[s.index[time]]

    @staticmethod
    def get_index(stocks):
        # This assumes that all stocks has the same index
        return stocks[0].index

    @staticmethod
    def list_stocks(stocks):
        list_stocks = [stock for stock in stocks]

    @classmethod
    def rank_stocks_at_t(cls, stocks, time, kpi, ascending=True):
        """ Rank stock at time t

        Returns
        =======
        series_rank : pd.Series (object) each element is a rank
        index corresponding to stock
        """

        list_stocks = cls.list_stocks(stocks)
        series_kpi = pd.Series([cls.get_stock(stocks, stock, time, kpi)
                                for stock in stocks], index=list_stocks)
        series_rank = series_kpi.rank(pct=True, ascending=ascending)

        return series_rank

    @classmethod
    def rank_stocks(cls, stocks, kpi, ascending=True):
        """
        Parameters
        ==========
        kpi : (string) key performance indicator of interest
        performance : (string) top/bottom, the best performing or worst performing

        Returns
        =======
        df : pd.DataFrame (object), each columns corresponds to
                ranking, and each element corresponds to stock in given year.

        """

        index = cls.get_index(stocks)
        ranks_at_t = list()
        for t in range(len(index)):
            cls.rank_stocks_at_t(stocks=stocks, time=t, kpi=kpi, ascending=ascending)

        return pd.DataFrame(ranks_at_t, index=index)
