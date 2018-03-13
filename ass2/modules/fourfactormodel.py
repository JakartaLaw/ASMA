from sklearn.linear_model import LinearRegression
from modules.stock import Stock
from modules.utils import to_latex_table
import pandas as pd


class FourFactorModel(object):

    def __init__(self, stock, portfolio):

        self.stock = stock
        self.portfolio = portfolio
        self.portfolio.columns = ['actual']

    def regress_model(self, model_name):

        self.model_name = model_name

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

        self.results = pd.DataFrame(results, index=[self.model_name])
        self.prediction = pd.DataFrame(lr.predict(X), index=X.index)
        self.prediction.columns = ['prediction']

    def get_results(self):
        return self.results

    def results_to_latex(self, file_name, decimals=3):
        to_latex_table(file_name, self.results, directory=None,
                       index=True, nr_decimals=decimals)

    def get_prediction(self):
        return pd.concat([self.prediction, self.portfolio], axis=1)
