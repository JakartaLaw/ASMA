from sklearn.linear_model import LinearRegression
from modules.stock import Stock
from modules.utils import to_latex_table
import pandas as pd


class FourFactorModel(object):

    def __init__(self, stock, portfolio):

        self.stock = stock
        self.portfolio = portfolio
        self.portfolio.columns = ['actual']

    def four_factor_model(self):

        factors = self.stock.return_df('factors')
        X = factors.drop(['Tbillrate'], axis=1)
        y = self.portfolio
        cols = list(X.columns)

        lr = LinearRegression()
        lr.fit(X=X, y=y)
        r2, intercept, coef = lr.score(X, y), list(lr.intercept_)[0], lr.coef_[0]

        results = {'r2': r2, 'intercept': intercept}
        for i in range(len(cols)):

            results[cols[i]] = coef[i]

        self.four_factor = pd.DataFrame(results, index=['four factor'])
        self.four_factor_prediction = pd.DataFrame(lr.predict(X), index=X.index)
        self.four_factor_prediction.columns = ['prediction']

    def capm_model(self):

        factors = self.stock.return_df('factors')
        X = factors.drop(['Tbillrate', 'SMB', 'WML', 'HML'], axis=1)
        y = self.portfolio
        cols = list(X.columns)

        lr = LinearRegression()
        lr.fit(X=X, y=y)
        r2, intercept, coef = lr.score(X, y), list(lr.intercept_)[0], lr.coef_[0]

        results = {'r2': r2, 'intercept': intercept}
        for i in range(len(cols)):

            results[cols[i]] = coef[i]

        self.capm = pd.DataFrame(results, index=['capm'])
        self.capm_prediction = pd.DataFrame(lr.predict(X), index=X.index)
        self.capm_prediction.columns = ['prediction']

    def regress_model(self, model_name):

        self.capm_model()
        self.four_factor_model()

        self.model_name = model_name
        self.results = pd.concat([self.capm, self.four_factor])

    def get_results(self):
        return self.results

    def results_to_latex(self, file_name, decimals=3):
        to_latex_table(file_name, self.results, directory=None,
                       index=True, nr_decimals=decimals)

    def get_prediction(self, model):

        if model is 'CAPM':
            return pd.concat([self.capm_prediction, self.portfolio], axis=1)

        elif model is 'four_factor':
            return pd.concat([self.four_factor_prediction, self.portfolio], axis=1)
