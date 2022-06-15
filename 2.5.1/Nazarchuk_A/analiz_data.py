# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
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
    if type(yerr) == float or type(yerr) == int:
        yerr = [yerr for _ in y]
    if type(xerr) == float or type(xerr) == int:
        xerr = [xerr for _ in x]

    if xerr[1] != 0 or yerr[1] != 0:
        subplot.errorbar(x, y, yerr=yerr, xerr=xerr, linewidth=4,
                         linestyle='', label=caption, color=color, ecolor=color,
                         elinewidth=1, capsize=3.4, capthick=1.4)
    else:
        subplot.scatter(x, y, linewidth=0.08, label=caption,
                        color=color, edgecolor='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def make_line_grafic(xmin, xmax, xerr, yerr, xlabel, ylabel, k, b, caption, subplot=None, color=None):
    if not subplot:
        subplot = plt
    x = np.arange(xmin, xmax, (xmax-xmin)/10000)
    subplot.plot(x, k*x+b, label=caption, color=color, linewidth=3)


def make_graffic(x, y, xlabel, ylabel, caption_point, xerr, yerr, k=None,
                 b=None, filename=None, color=None):
    # fig, subplot = plt.subplots(figsize=(8, 6))
    sublpot = plt
    if not color:
        color = ['limegreen', 'indigo']
    if k and b:
        make_line_grafic(xmin=min(x)-1, xmax=max(x)+1, xerr=xerr, yerr=yerr, xlabel='',
                         ylabel='', k=k, b=b,
                         caption='Theoretical dependence', subplot=plt, color='red')
    if type(yerr) == float or type(yerr) == int:
        yerr = [yerr for _ in y]
    k, b, sigma = approx(x, y, b, yerr)
    sigma = abs(k*((sigma/k)**2+(np.mean(yerr)/np.mean(y))**2 +
                   (np.mean(xerr)/np.mean(x))**2)**0.5)
    make_line_grafic(xmin=min(x)*0.98, xmax=max(x)*1.02, xerr=xerr, yerr=yerr, xlabel='',
                     ylabel='', k=k, b=b, caption=caption_point,
                     subplot=plt, color=color[1])

    make_point_grafic(x, y, xlabel=xlabel,
                      ylabel=ylabel, caption=caption_point,
                      xerr=xerr, yerr=yerr, subplot=plt, color=color[0])
    return k, b, sigma


def approx(x, y, b, sigma_y, f=None):
    if sigma_y[0] != 0:
        sigma_y = [1/i**2 for i in sigma_y]
    else:
        sigma_y = np.array([1 for _ in y])
    if f == None:
        if b == 0:
            def f(x, k):
                return k*x
            k, sigma = curve_fit(f, xdata=x, ydata=y, sigma=sigma_y)
            sigma = np.sqrt(np.diag(sigma))
            return k, b, sigma
        else:
            def f(x, k, b):
                return x*k + b
            k, sigma = curve_fit(f, xdata=x, ydata=y, sigma=sigma_y)
            b = k[1]
            k = k[0]
            sigma = np.sqrt(np.diag(sigma))

            return k, b, sigma[0]
    else:
        k, sigma = curve_fit(f, xdata=x, ydata=y, sigma=sigma_y)
        sigma = np.sqrt(np.diag(sigma))
        b = k[1]
        k = k[0]
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


def make_fun(A0, T):
    def f(t, k, b):
        return A0/(1+A0*b*t)-k*0*A0*t/T
    return f


def make_fun_grafic(xmin, xmax, xerr, yerr, xlabel, ylabel, f, k, b, caption, subplot=None, color=None):
    if not subplot:
        subplot = plt
    x = np.arange(xmin, xmax, (xmax-xmin)/10000)
    subplot.plot(x, f(x, k, b), label=caption, color=color)


def make_alcohol():
    small_data = make_dic('Data.csv')
    data['p_pv'] = []
    data['p_gl'] = []
    data['dp'] = []
    data['p_pv_sigma'] = []
    data['p_gl_sigma'] = []
    data['dp_sigma'] = []
    data['sigma_gl'] = []
    data['sigma_sigma_gl'] = []
    data['sigma_pv'] = []
    data['sigma_sigma_pv'] = []
    data['T'] = []
    for i in small_data.keys():
        if i != 'h':
            t = int(i[-2:len(i)])
            if t not in data['T']:
                data['T'].append(t)
            if i.find('pv') != -1:
                data['p_pv'].append(small_data[i].mean()*k_h_to_p)
                data['p_pv_sigma'].append(
                    (np.std(small_data[i])**2+0.5**2)**0.5**k_h_to_p)
            else:
                data['p_gl'].append(small_data[i].mean()*k_h_to_p)
                data['p_gl_sigma'].append(
                    (np.std(small_data[i])**2+0.5**2)**0.5*k_h_to_p)
        else:
            data['p_alco'] = (small_data[i].mean()*k_h_to_p)
            data['p_alco_sigma'] = (
                (np.std(small_data[i])**2+0.5**2)**0.5**k_h_to_p)
    data['r'] = 2*data['sigma_alco']/data['p_alco']*10**3
    data['r_sigma'] = data['r']*data['p_alco_sigma']/data['p_alco']

    for i in range(len(data['p_pv'])):
        data['dp'].append(data['p_gl'][i]-data['p_pv'][i])
        data['dp_sigma'].append(
            (data['p_gl_sigma'][i]**2+data['p_pv_sigma'][i]**2)**0.5)

    data['T'] = np.array(data['T'])
    data['dp'] = np.array(data['dp'])
    data['dh'] = (data['dp'][0] / 9.81/0.998 + data['h_teor'])/2
    data['dh_sigma'] = ((data['dp'][0] / 9.81/0.998 - data['dh'])
                        ** 2+(data['h_teor']-data['dh'])**2)**0.5

    for i in range(len(data['T'])):
        sigma = data['r']*data['p_pv'][i]/2
        sigma_sigma = sigma * \
            ((data['r_sigma']/data['r'])**2 +
             (data['p_pv_sigma'][i]/data['p_pv'][i])**2) ** 0.5
        data['sigma_pv'].append(sigma)
        data['sigma_sigma_pv'].append(sigma_sigma)

        sigma = data['r']*(data['p_gl'][i]-0.998*9.81*data['dh'])/2
        sigma_sigma = sigma * \
            ((data['r_sigma']/data['r'])**2 +
             (data['p_gl_sigma'][i]/data['p_gl'][i])**2) ** 0.5
        data['sigma_gl'].append(sigma)
        data['sigma_sigma_gl'].append(sigma_sigma)

    k, b, sigma = make_graffic(y=data['sigma_gl'], x=data['T']+273,
                               xlabel='T, K', ylabel='$\sigma$, мН/м',
                               caption_point='Измерения на глубине', xerr=0.1,
                               yerr=data['sigma_sigma_gl'],
                               color=['blue', 'lightgreen'])
    make_graffic(y=data['sigma_pv'], x=data['T']+273,
                 xlabel='T, K', ylabel='$\sigma$, мН/м',
                 caption_point='Измерения на поверхности', xerr=0.1,
                 yerr=data['sigma_sigma_pv'],
                 color=['red', 'y'])
    make_point_grafic(y=data['sigma_teor'], x=data['T']+273,
                      xlabel='T, K', ylabel='$\sigma$, мН/м',
                      caption='Табличные значения', xerr=0, yerr=0, color='purple')
    plt.legend()
    plt.savefig('sigma')
    plt.show()

    data['dsigma/dt'] = k
    data['dsigma/dt_sigma'] = sigma

    data['q'] = - (data['T']+273) * data['dsigma/dt']
    yerr = [data['sigma_sigma_gl'][i]/data['sigma_gl'][i]*data['q'][i]
            for i in range(len(data['q']))]

    make_graffic(y=data['q'], x=data['T'], xlabel='t, $^\circ$C',
                 ylabel='q, мДж/$м^2$', caption_point='', xerr=0.1, yerr=yerr,
                 color=['purple', 'orange'])
    plt.savefig('q')
    plt.show()

    data['U'] = data['sigma_gl'] + data['q']
    yerr = [((yerr[i]/data['q'][i])**2 +
            (data['sigma_sigma_gl'][i]/data['sigma_gl'][i])**2)**0.5*data['U'][i]
            for i in range(len(data['q']))]

    k, b1, sigma = make_graffic(y=data['U'], x=data['T'], xlabel='t, $^\circ$C',
                                ylabel='U/F, мДж/$м^2$', caption_point='', xerr=0.1,
                                yerr=yerr, color=['c', 'red'])
    plt.savefig('U')
    plt.show()
    print('k = ', k, '+-', sigma)
    print('b_exp =', b1+k*20, 'b_teor = ', b)

    for i in data.keys():
        data[i] = np.array(data[i])


k_h_to_p = 9.81 * 0.2
data = {}
data['sigma_alco'] = 22.8*10**(-3)
data['h_teor'] = 6
data['sigma_teor'] = [72.75, 71.18, 70.37, 69.56, 68.74, 67.91, 67.05, 66.18]
make_alcohol()
print('r=', data['r'], '+-', data['r_sigma'],
      '(', data['r_sigma']/data['r']*100, '%)')

dp = data['dp'].mean()
dp_sigma = data['dp_sigma'].mean()
print('dh_exp = ', dp / 9.81/0.998, '+-', dp_sigma/9.81/0.998)
print('dsigma/dt=', data['dsigma/dt'], '+-', data['dsigma/dt_sigma'],
      '(', -data['dsigma/dt_sigma']/data['dsigma/dt']*100, '%)')
