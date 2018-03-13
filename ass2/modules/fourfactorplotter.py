from modules.fourfactormodel import FourFactorModel
import matplotlib.pyplot as plt
import seaborn as sbn


def four_factor_plotter(four_factor_model, fig_name, save=False):
    """
    parameters
    ==========
    Four Factor model object
    """

    ff = four_factor_model.get_prediction('four_factor')
    capm = four_factor_model.get_prediction('CAPM')

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.set_title('four factor')
    ax2.set_title('CAPM')
    sbn.regplot('actual', 'prediction', data=ff, scatter_kws={'alpha': 0.3, 'color': 'red'}, ax=ax1)
    sbn.regplot('actual', 'prediction', data=capm, scatter_kws={
                'alpha': 0.3, 'color': 'red'}, ax=ax2)
    f.suptitle("{}".format(fig_name), fontsize=16)

    if save is True:
        f.savefig('{}.png'.format(fig_name))
