import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.optimize import curve_fit


def save_fig(fig_id, tight_layout=True, fig_extension='png', resolution=300):
    path = os.path.join('images', fig_id + '.' + fig_extension)
    print('Saving figure', fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


class ReservoirMetamodel:
    def __init__(self, data):
        self.data = data
        self.data_train = data[:int(4 * len(data) / 13)]
        self.data_valid = data[int(4 * len(data) / 13):int(5 * len(data) / 13)]
        self.data_test = data[int(5 * len(data) / 13):]

    def print_info(self):
        print(self.data.info())

    def print_describe(self):
        print(self.data.describe())

    def plot_parameters_distributions(self):
        self.data.hist(bins=50, figsize=(20, 30))
        save_fig('parameters_histograms')

    def corr_matrix(self):
        return self.data_train.corr()

    def plot_corr_heat_map(self):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=1)
        plt.figure()
        corr_matrix = self.corr_matrix()
        ax = sns.heatmap(corr_matrix, cmap='coolwarm', annot=False, vmin=-1, vmax=1)
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=20)
        save_fig('corr_matrix_1')

    def manual_approximation(self):

        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=2)

        def approx_func(X, a1, a2, a3, b):
            x1, x2 = X
            return a1 * x1 + a2 * x2 + a3 * x1 * x2 + b

        popt, _ = curve_fit(approx_func, (self.data_train['PERMX CRACK (mD)'], self.data_train['PORO CRACK']),
                            self.data_train['OIL RATE 1 (SM3/DAY)'])

        a1, a2, a3, b = popt

        y = approx_func((self.data_test['PERMX CRACK (mD)'], self.data_test['PORO CRACK']), a1, a2, a3, b)

        plt.figure()
        sns.boxplot(x=(y - self.data_test['OIL RATE 1 (SM3/DAY)']) / self.data_test['OIL RATE 1 (SM3/DAY)'] * 100)
        plt.xlabel('Ошибка прогноза, в процентах')
        save_fig('manual_approximation_test_errors_boxplot')

    def all_scatter_plot(self):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=2)
        plt.figure()
        sns.scatterplot(x=self.data['PERMX CRACK (mD)'], y=self.data['OIL RATE 1 (SM3/DAY)'],
                        hue=self.data['PORO CRACK'])

        save_fig('all_data_scatterplot')


if __name__ == '__main__':
    metamodel = ReservoirMetamodel(pd.read_csv(os.path.join('datasets', 'reservoir_train800_scenario1.csv')))
    metamodel.print_info()
    metamodel.plot_parameters_distributions()
    metamodel.plot_corr_heat_map()
    metamodel.all_scatter_plot()
    metamodel.manual_approximation()
