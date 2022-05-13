import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import ExtraTreesRegressor
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


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x[self.attribute_names].values


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

        save_fig('all_data_scatterplot_1')

    def data_scaler(self, input):
        num_attribs = list(input)
        num_pipeline = Pipeline([
            ('selector', DataFrameSelector(num_attribs)),
            ('std_scaler', StandardScaler())
        ])
        train_input_prepared = num_pipeline.fit_transform(input)
        return train_input_prepared

    def linear_regression(self):
        lin_reg = LinearRegression()
        lin_reg.fit(self.data_scaler(self.data_train.iloc[:, 0:4]), self.data_train['OIL RATE 1 (SM3/DAY)'])
        return lin_reg

    def linear_regression_tests_boxplot(self):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=2)
        lin_reg = self.linear_regression()
        relative_error = (lin_reg.predict(self.data_scaler(self.data_test.iloc[:, 0:4])) -
                          np.array(self.data_test['OIL RATE 1 (SM3/DAY)'])) / \
                         (np.array(self.data_test['OIL RATE 1 (SM3/DAY)'])) * 100
        plt.figure()
        sns.boxplot(x=relative_error)
        plt.xlabel('Ошибка прогноза, в процентах')
        save_fig('linear_regression_test_errors_boxplot')

    def extra_trees(self):
        extra_trees_reg = ExtraTreesRegressor(n_estimators=1000, random_state=42)
        extra_trees_reg.fit(self.data_scaler(self.data_train.iloc[:, 0:4]), self.data_train['OIL RATE 1 (SM3/DAY)'])
        return extra_trees_reg

    def extra_trees_tests_boxplot(self):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=2)
        extra_trees_reg = self.extra_trees()
        relative_error = (extra_trees_reg.predict(self.data_scaler(self.data_test.iloc[:, 0:4])) -
                          np.array(self.data_test['OIL RATE 1 (SM3/DAY)'])) / \
                         (np.array(self.data_test['OIL RATE 1 (SM3/DAY)'])) * 100
        plt.figure()
        sns.boxplot(x=relative_error)
        plt.xlabel('Ошибка прогноза, в процентах')
        save_fig('extra_trees_regression_test_errors_boxplot')


if __name__ == '__main__':
    metamodel = ReservoirMetamodel(pd.read_csv(os.path.join('datasets', 'reservoir_train800_scenario1.csv')))
    # metamodel.print_info()
    # metamodel.plot_parameters_distributions()
    # metamodel.plot_corr_heat_map()
    # metamodel.all_scatter_plot()
    # metamodel.manual_approximation()

    metamodel.linear_regression_tests_boxplot()
    metamodel.extra_trees_tests_boxplot()
