import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
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

    def plot_parameters_distributions(self, suffix='_unknown'):
        self.data.iloc[:, 41:].hist(bins=50, figsize=(15, 10))
        save_fig('parameters_histograms' + suffix)

    def corr_matrix(self):
        return self.data_train.corr()

    def plot_corr_heat_map(self, suffix='_unknown'):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=1)
        plt.figure()
        corr_matrix = self.corr_matrix()
        ax = sns.heatmap(corr_matrix, cmap='coolwarm', annot=False, vmin=-1, vmax=1)
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=20)
        save_fig('corr_matrix' + suffix)

    def all_scatter_plot(self):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=2)
        plt.figure()
        sns.scatterplot(x=self.data['PERMX CRACK (mD)'], y=self.data['OIL RATE 1 (SM3/DAY)'],
                        hue=self.data['PORO CRACK'])
        save_fig('all_data_scatterplot_1')

    def manual_approximation(self):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=2)

        def approx_func(X, a1, a2, a3, b):
            x1, x2 = X
            return a1 * x1 + a2 * x2 + a3 * x1 * x2 + b

        ys = []
        for i in range(1, 61):
            popt, _ = curve_fit(approx_func, (self.data_train['PERMX CRACK (mD)'], self.data_train['PORO CRACK']),
                                self.data_train[f'OIL RATE {i} (SM3/DAY)'])
            a1, a2, a3, b = popt
            y = approx_func((self.data_test['PERMX CRACK (mD)'], self.data_test['PORO CRACK']), a1, a2, a3, b)
            if i == 1:
                print(type(y))
            ys.append(y)
        return ys

    def data_scaler(self, input):
        num_attribs = list(input)
        num_pipeline = Pipeline([
            ('selector', DataFrameSelector(num_attribs)),
            ('std_scaler', StandardScaler())
        ])
        train_input_prepared = num_pipeline.fit_transform(input)
        return train_input_prepared

    def linear_regression(self):
        lin_regs = []
        for i in range(1, 61):
            lin_reg = LinearRegression()
            lin_reg.fit(self.data_scaler(self.data_train.iloc[:, 0:4]), self.data_train[f'OIL RATE {i} (SM3/DAY)'])
            lin_regs.append(lin_reg)
        return lin_regs

    def neigh_regression(self):
        neigh_regs = []
        for i in range(1, 61):
            neigh_reg = KNeighborsRegressor(n_neighbors=4)
            neigh_reg.fit(self.data_scaler(self.data_train.iloc[:, 0:4]), self.data_train[f'OIL RATE {i} (SM3/DAY)'])
            neigh_regs.append(neigh_reg)
        return neigh_regs

    def svm_regression(self):
        svm_regs = []
        for i in range(1, 61):
            svm_reg = SVR(C=250.0, epsilon=0.01)
            svm_reg.fit(self.data_scaler(self.data_train.iloc[:, 0:4]), self.data_train[f'OIL RATE {i} (SM3/DAY)'])
            svm_regs.append(svm_reg)
        return svm_regs

    def extra_trees_regression(self):
        extra_trees_regs = []
        for i in range(1, 61):
            extra_trees_reg = ExtraTreesRegressor(n_estimators=500, random_state=42)
            extra_trees_reg.fit(self.data_scaler(self.data_train.iloc[:, 0:4]),
                                self.data_train[f'OIL RATE {i} (SM3/DAY)'])
            extra_trees_regs.append(extra_trees_reg)
        return extra_trees_regs

    def plot_errors_boxplot(self, approx='linear_regression_test_errors_boxplot', suffix='_unknown'):
        sns.set(rc={'figure.figsize': (20, 15)}, font_scale=2)
        relative_errors = []
        if approx == 'manual_approximation_test_errors_boxplot':
            y = self.manual_approximation()
            for i in range(1, 61):
                relative_error = (y[i - 1] - self.data_test[f'OIL RATE {i} (SM3/DAY)']) / self.data_test[
                    f'OIL RATE {i} (SM3/DAY)'] * 100
                relative_errors.append(relative_error)
        elif approx == 'extra_trees_regression_test_errors_boxplot':
            extra_trees_regs = self.extra_trees_regression()
            for i in range(1, 61):
                relative_error = (extra_trees_regs[i - 1].predict(self.data_scaler(self.data_test.iloc[:, 0:4])) -
                                  np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) / \
                                 (np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) * 100
                relative_errors.append(relative_error)
        elif approx == 'nearest_neighs_approximation_test_errors_boxplot':
            neigh_regs = self.neigh_regression()
            for i in range(1, 61):
                relative_error = (neigh_regs[i - 1].predict(self.data_scaler(self.data_test.iloc[:, 0:4])) -
                                  np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) / \
                                 (np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) * 100
                relative_errors.append(relative_error)
        elif approx == 'svm_approximation_test_errors_boxplot':
            svm_regs = self.svm_regression()
            for i in range(1, 61):
                relative_error = (svm_regs[i - 1].predict(self.data_scaler(self.data_test.iloc[:, 0:4])) -
                                  np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) / \
                                 (np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) * 100
                relative_errors.append(relative_error)
        else:
            lin_regs = self.linear_regression()
            for i in range(1, 61):
                relative_error = (lin_regs[i - 1].predict(self.data_scaler(self.data_test.iloc[:, 0:4])) -
                                  np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) / \
                                 (np.array(self.data_test[f'OIL RATE {i} (SM3/DAY)'])) * 100
                relative_errors.append(relative_error)
        plt.figure()
        plt.xticks(rotation=90)
        sns.boxplot(data=relative_errors)
        plt.xlabel('?????????? ????????????')
        plt.ylabel('???????????? ????????????????, ?? ??????????????????')
        save_fig(approx + suffix)


if __name__ == '__main__':
    dataset_file = 'reservoir_train800_scenario2.csv'
    metamodel = ReservoirMetamodel(pd.read_csv(os.path.join('datasets', dataset_file)))
    # metamodel.print_info()
    # metamodel.plot_parameters_distributions(suffix=dataset_file[-14:-4]+'_2')
    # metamodel.plot_corr_heat_map(suffix=dataset_file[-14:-4])
    # metamodel.all_scatter_plot()
    # metamodel.manual_approximation()

    metamodel.plot_errors_boxplot('svm_approximation_test_errors_boxplot', suffix=dataset_file[-14:-4])
