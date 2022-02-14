# для запуска введите в терминале: bokeh serve performance_widget.py
# и перейдите по сгенерированной ссылке на локальный сервер

from sympy import besseli, besselk, lambdify, symbols, sqrt, pi, diff
from anaflow import get_lap_inv
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, HoverTool
from bokeh.plotting import figure


def liquid_rate(time, mu1, mu2, k1, k2, h1, h2, phi1, phi2, rw, pw, re1, pe1, re2, pe2, ct1, ct2):
    s, r = symbols('s, r')
    kappa1 = k1/(phi1*mu1*ct1)
    kappa2 = k2/(phi2*mu2*ct2)
    arg1_r, arg1_re1, arg1_rw = sqrt(s / kappa1) * r, sqrt(s / kappa1) * re1, sqrt(s / kappa1) * rw
    arg2_r, arg2_re2, arg2_rw = sqrt(s / kappa2) * r, sqrt(s / kappa2) * re2, sqrt(s / kappa2) * rw

    p1 = (pw - pe1) / s * \
         (besselk(0, arg1_re1) * besseli(0, arg1_r) - besseli(0, arg1_re1) * besselk(0, arg1_r)) / \
         (besselk(0, arg1_re1) * besseli(0, arg1_rw) - besseli(0, arg1_re1) * besselk(0, arg1_rw))

    p2 = (pw - pe2) / s * \
         (besselk(1, arg2_re2) * besseli(0, arg2_r) + besseli(1, arg2_re2) * besselk(0, arg2_r)) / \
         (besselk(1, arg2_re2) * besseli(0, arg2_rw) + besseli(1, arg2_re2) * besselk(0, arg2_rw))

    q1 = ((2 * pi * k1 * h1 * rw) / mu1) * diff(p1, r).subs(r, rw)
    q2 = ((2 * pi * k2 * h2 * rw) / mu2) * diff(p2, r).subs(r, rw)

    p1 = lambdify([s, r], p1)
    p2 = lambdify([s, r], p2)
    q1 = lambdify(s, q1)
    q2 = lambdify(s, q2)

    rate1 = 86400 * get_lap_inv(q1)(time)
    rate2 = 86400 * get_lap_inv(q2)(time)

    rate = rate1 + rate2

    return rate1, rate2, rate


t = np.logspace(2, 7, 40)

Q1, Q2, Q = liquid_rate(t, 0.0014, 0.0014, 1e-14, 1e-14, 10, 10, 0.2,
         0.2, 0.1, 10132500, 50, 25331250, 50, 25331250, 4.9345e-10, 4.9345e-10)

source = ColumnDataSource(data=dict(x=t/3600, y1=Q1, y2=Q2, y3=Q))


plot = figure(height=600, width=700, title='Зависимость дебита от времени', tools='crosshair,pan,reset,save,wheel_zoom',
              x_axis_type='log', x_axis_label='t, ч', y_axis_label='Q, куб.м/сут')
plot.xgrid.minor_grid_line_color = 'navy'
plot.xgrid.minor_grid_line_alpha = 0.04
plot.ygrid.minor_grid_line_color = 'navy'
plot.ygrid.minor_grid_line_alpha = 0.04

plot.line('x', 'y1', source=source, line_width=1, line_alpha=1, color='red', legend_label='Q1')
plot.line('x', 'y2', source=source, line_width=1, line_alpha=1, color='blue', legend_label='Q2')
plot.line('x', 'y3', source=source, line_width=1, line_alpha=1, color='orange', legend_label='Q=Q1+Q2')

plot.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
    ('t', '@x'),
    ('Q1', '@y1'),
    ('Q2', '@y2'),
    ('Q=Q1+Q2', '@y3'),
]))

text = TextInput(title='Заголовок', value='Зависимость дебита от времени')
mu1_sl = Slider(title='Вязкость 1, сПз', value=1.4, start=0.1, end=4.8, step=0.1)
mu2_sl = Slider(title='Вязкость 2, сПз', value=1.4, start=0.1, end=4.8, step=0.1)

k1_sl = Slider(title='Проницаемость 1, мД', value=10, start=5, end=505, step=10)
k2_sl = Slider(title='Проницаемость 2, мД', value=10, start=5, end=505, step=10)

h1_sl = Slider(title='Мощность пласта 1, м', value=10, start=1, end=15, step=0.5)
h2_sl = Slider(title='Мощность пласта 2, м', value=10, start=1, end=15, step=0.5)

phi1_sl = Slider(title='Пористость 1', value=0.2, start=0.05, end=0.3, step=0.01)
phi2_sl = Slider(title='Пористость 2', value=0.2, start=0.05, end=0.3, step=0.01)

rw_sl = Slider(title='Радиус скважины, м', value=0.14, start=0.05, end=0.4, step=0.05)
pw_sl = Slider(title='Забойное давление, атм', value=100, start=50, end=300, step=1)

pe1_sl = Slider(title='Начальное давление на контуре 1, атм', value=250, start=100, end=400, step=10)
pe2_sl = Slider(title='Начальное давление на контуре 2, атм', value=250, start=100, end=400, step=10)

ct1_sl = Slider(title='Сжимаемость 1', value=4.9345e-10, start=4.9345e-11, end=4.9345e-9, step=1e-11,
                format='0[.]000000000000')
ct2_sl = Slider(title='Сжимаемость 2', value=4.9345e-10, start=4.9345e-11, end=4.9345e-9, step=1e-11,
                format='0[.]00000000000000')


def update_title(attrname, old, new):
    plot.title.text = text.value


def update_data(attrname, old, new):
    t = np.logspace(2, 7, 40)
    Q1, Q2, Q = liquid_rate(t, mu1_sl.value/1000, mu2_sl.value/1000, k1_sl.value*1e-15, k2_sl.value*1e-15, h1_sl.value,
                            h2_sl.value, phi1_sl.value, phi2_sl.value, rw_sl.value, pw_sl.value*101325, 50,
                            pe1_sl.value*101325, 50, pe2_sl.value*101325, ct1_sl.value, ct2_sl.value)
    source.data = dict(x=t/3600, y1=Q1, y2=Q2, y3=Q)


text.on_change('value', update_title)
for w in [mu1_sl, mu2_sl, k1_sl, k2_sl, h1_sl, h2_sl, phi1_sl, phi2_sl, rw_sl, pw_sl, pe1_sl, pe2_sl, ct1_sl, ct2_sl]:
    w.on_change('value', update_data)


inputs = column(text, mu1_sl, mu2_sl, k1_sl, k2_sl, h1_sl, h2_sl, phi1_sl, phi2_sl, rw_sl, pw_sl, pe1_sl, pe2_sl,
                ct1_sl, ct2_sl)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = 'liquid_rate'
