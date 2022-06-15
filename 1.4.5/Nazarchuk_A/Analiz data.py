# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from scipy.optimize import curve_fit


def read_csv(file_name):
    with open(file_name) as file:
        reader = list(csv.reader(file, delimiter=';',
                      quotechar=',', quoting=csv.QUOTE_MINIMAL))
    return reader


def make_latex_table(data):
    table = []
    table.append("\\begin{table}".replace('//', '\\'))
    table.append("\label{}".replace('/', '\\'))
    table.append('\caption{}'.replace('/', '\\'))
    leng = len(data[0])
    stroka = 'c'.join(['|' for _ in range(leng+1)])
    table.append('\\begin{tabular}{'.replace('//', '\\')+stroka+'}')
    table.append('\hline')
    for i in range(len(data)):
        table.append(' & '.join(data[i]) + ' \\\\')
        table.append('\hline')
    table.append("\end{tabular}".replace('/', '\\'))
    table.append("\end{table}".replace('/', '\\'))
    return table


def make_point_grafic(x, y, xlabel, ylabel, caption, xerr, yerr, subplot=None, color=None):
    if not subplot:
        subplot = plt
    if xerr == 0 and yerr == 0:
        subplot.scatter(x, y, label=caption, color=color)
    else:
        subplot.errorbar(x, y, yerr=yerr, xerr=xerr, linewidth=4,
                         linestyle='', label=caption, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def make_line_grafic(xmin, xmax, xerr, yerr, xlabel, ylabel, k, b, caption, subplot=None, color=None):
    if not subplot:
        subplot = plt
    x = np.arange(xmin, xmax, (xmax-xmin)/10000)
    subplot.plot(x, k*x+b, label=caption, color=color)


def make_graffic(x, y, xlabel, ylabel, caption_point, xerr, yerr, k, b):
    fig, subplot = plt.subplots(figsize=(8, 6))
    make_point_grafic(x, y, xlabel=xlabel,
                      ylabel=ylabel, caption=caption_point,
                      xerr=0, yerr=0, subplot=subplot, color='black')
    make_line_grafic(xmin=min(x)-1, xmax=max(x)+1, xerr=xerr, yerr=yerr, xlabel='',
                     ylabel='', k=k, b=b,
                     caption='Theoretical dependence', subplot=subplot, color='red')
    if type(yerr) != np.ndarray:
        yerr = [yerr for _ in y]
    k, b, sigma = approx(x, y, 0, yerr)
    make_line_grafic(xmin=min(x)-1, xmax=max(x)+1, xerr=0, yerr=0, xlabel='',
                     ylabel='', k=k[0], b=b, caption='Approximation',
                     subplot=subplot, color='blue')
    subplot.legend()
    plt.show()
    return k[0], b, sigma[0]


def approx(x, y, b, sigma_y):
    if sigma_y[0] != 0:
        sigma_y = [1/i**2 for i in sigma_y]
    else:
        sigma_y = [1 for _ in y]
    if b == 0:
        def f(x, k):
            return k*x
        k, sigma = curve_fit(f, xdata=x, ydata=y, sigma=sigma_y)
        sigma = np.sqrt(np.diag(sigma))
        # print(sigma[0])
        # if not param:
        #     sigma_y = [1/i**0.5 for i in sigma_y]
        # y = np.array(y)
        # x = np.array(x)
        # sigma_y = np.array(sigma_y)
        # w = sum(1/sigma_y**2)
        # if not param:
        #     sigma_xy = sigma_y*x
        # else:
        #     sigma_xy = sigma_y
        # w_xy = sum(1/sigma_xy**2)
        # xy_sr = 1/w_xy*sum(1/sigma_xy**2*y*x)
        # x_2_sr = sum(x**2)/len(x)
        # k = xy_sr/x_2_sr
        # b = 0
        # if not param:
        #     w = sum(1/(2*sigma_y*y)**2)
        #     y2_sr = 1/w*sum(y**2*2*sigma_y*y)
        # else:
        #     y2_sr = sum(y**2)/len(y)
        # sigma = 1/k/2/(x_2_sr - xy_sr)
        # print(sigma)
        # k = [k]
        # sigma = [sigma]
        return k, b, sigma
    else:
        def f(x, k, b):
            return x*k + b
        k, b, sigma = curve_fit(f, xdata=x, ydata=y, sigma=sigma_y)
        sigma = np.sqrt(np.diag(sigma))
        return k, b, sigma


def find_delivation(data):
    data = np.array(data).astype(np.float)
    s = sum(data)/len(data)
    su = 0
    for i in data:
        su += (i-s)**2
    return (su/(len(data)-1))**0.5


def make_dic(filename):
    data = np.array(read_csv(filename))
    data = np.transpose(data)
    dic = {}
    for i in range(len(data)):
        dic[data[i][0]] = np.array(data[i][1:]).astype(np.float)
    data = dic
    return data


# read data
data = make_dic('Данные.csv')
data.pop('m_1')
data.pop('m_2')
data.pop('m_pod')

# make one graffic with lots of lines:
data['T'] = []
data['T'].append(data['m'][0]*9.83 / 1000)
data['T'].append(data['m'][8]*9.83 / 1000)
data['T'].append(data['m'][13]*9.83 / 1000)
data['T'].append(data['m'][19]*9.83 / 1000)
data['T'].append(data['m'][22]*9.83 / 1000)
data['T'] = np.array(data['T'])
data['T_str'] = []
for i in data['T']:
    data['T_str'].append('T='+str(round(i, 1))+'H')
data['T_str'] = np.array(data['T_str'])
fig, subplot = plt.subplots(figsize=(16, 12))
k = [0 for i in range(len(data['L']))]
s = [0 for i in range(len(data['L']))]
make_point_grafic(data['n'][0:8], data['nu'][0:8], xlabel='n гармоники',
                  ylabel="$\\nu_n$, Гц", caption=data['T_str'][0],
                  xerr=0, yerr=0, subplot=subplot)
make_point_grafic(data['n'][8:12], data['nu'][8:12], xlabel='n гармоники',
                  ylabel="$\\nu_n$, Гц", caption=data['T_str'][1],
                  xerr=0, yerr=0, subplot=subplot)
make_point_grafic(data['n'][12:16], data['nu'][12:16], xlabel='n гармоники',
                  ylabel="$\\nu_n$, Гц", caption=data['T_str'][2],
                  xerr=0, yerr=0,  subplot=subplot)
make_point_grafic(data['n'][16:20], data['nu'][16:20], xlabel='n гармоники',
                  ylabel="$\\nu_n$, Гц",
                  caption=data['T_str'][3],
                  xerr=0, yerr=0,  subplot=subplot)
make_point_grafic(data['n'][20:], data['nu'][20:], xlabel='n гармоники',
                  ylabel="$\\nu_n$, Гц", caption=data['T_str'][4],
                  xerr=0, yerr=0, subplot=subplot)
subplot.legend()
plt.show()


# make lots of grafics with only one one line in one
def line_of_one_harmonic(n1=0, n2=None):
    if not n2:
        n2 = len(data['n'])
    x = data['n'][n1:n2]
    y = data['nu'][n1:n2]
    k, b = 1/2/data['L'][n1]*100 * \
        (data['m'][n1]*9.81/data['rho'][n1]*10**(3))**0.5, 0
    T = 'T='+str(round(data['m'][n1]*9.83 / 1000, 1))+'H'
    k, b, sigma = make_graffic(x=x, y=y, xlabel='n гармоники', ylabel="$\\nu_n$, Гц",
                               caption_point=T, xerr=0, yerr=0, k=k, b=b)
    data['u'].append(k)
    data['u_sigma'].append(sigma)


data['u'] = []
data['u_sigma'] = []
line_of_one_harmonic(n2=8)
line_of_one_harmonic(8, 12)
line_of_one_harmonic(12, 16)
line_of_one_harmonic(16, 20)
line_of_one_harmonic(n1=20)
data['u'] = np.array(data['u'])
data['u_sigma'] = np.array(data['u_sigma'])


k, b, sigma = make_graffic(x=data['u']**2, y=data['T'], xlabel='T, H',
                           ylabel='$u^2$, м/$c^2$',
                           caption_point='Зависимость $u^2$ от T', xerr=0,
                           yerr=data['u_sigma']*2*data['u'], k=data['rho'][0]/10**6, b=0)
data['u_otn'] = data['u_sigma'] / data['u']
data['rho_otn'] = 2*data['u_otn']
rho_otn = (sum(data['rho_otn']**2)/len(data['rho_otn']))**0.5
sist = rho_otn*k
print(sigma/k*100)
sigma = (sigma**2 + sist**2)**0.5
print('rho_l=', k*10**6, '+-', sigma*10**6, 'мг/$м^3$')
