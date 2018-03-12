

class FourFactorModel(object):

    def __init__(self, stock, portfolio):

        self.stock = stock
        self.portfolio = portfolio

    def create_data(self):

        data = pd.concat([self.stock, self.portfolio], axis=1)
        data.rename({0: 'respons'}, inplace=True, axis=1)

        return data

    def regress_model(self):
