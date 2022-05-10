import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.optimize import curve_fit


def approx_func(X, a1, a2, a3, a4, b):
    x1, x2, x3, x4 = X
    return a1 * x1 + a2 * x2 + a3*x3 +a4*x4 + b


data1 = pd.read_csv(os.path.join('datasets', 'reservoir_train800_scenario1.csv'))


input_data = data1.T.iloc[:4, :]
oil_rates_data = data1.T.iloc[4:, :]


print(input_data)
print(oil_rates_data)

sns.scatterplot(x=data1['PERMX CRACK (mD)'], y=data1['OIL RATE 1 (SM3/DAY)'], hue=data1['PORO CRACK'])
#sns.lineplot(data=oil_rates_data)
#plt.xticks(rotation=90)
plt.grid()
plt.show()

popt, _ = curve_fit(approx_func, (data1['PORO MATRIX'], data1['PERMX MATRIX (mD)'], data1['PERMX CRACK (mD)'],
                                  data1['PORO CRACK']), data1['OIL RATE 1 (SM3/DAY)'])
a1, a2, a3, a4, b = popt
print(b)

current = 1
y = approx_func((data1['PORO MATRIX'], data1['PERMX MATRIX (mD)'],
                 data1['PERMX CRACK (mD)'], data1['PORO CRACK']), a1, a2, a3, a4, b)
print()
print(y)
# sns.boxplot(x=(y - data1['OIL RATE 1 (SM3/DAY)']) / data1['OIL RATE 1 (SM3/DAY)'] * 100)
# plt.show()
