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
    make_point_grafic(x, y, xlabel=xlabel,
                      ylabel=ylabel, caption=caption_point,
                      xerr=xerr, yerr=yerr, subplot=plt, color=color[0])
    if k and b:
        make_line_grafic(xmin=min(x)-1, xmax=max(x)+1, xerr=xerr, yerr=yerr, xlabel='',
                         ylabel='', k=k, b=b,
                         caption='Theoretical dependence', subplot=plt, color='red')
    if type(yerr) == float or type(yerr) == int:
        yerr = [yerr for _ in y]
    k, b, sigma = approx(x, y, b, yerr)
    sigma = k*((sigma/k)**2+(np.mean(yerr)/np.mean(y))**2 +
               (np.mean(xerr)/np.mean(x))**2)**0.5
    
    make_line_grafic(xmin=min(x)*0.9, xmax=max(x)*1.1, xerr=xerr, yerr=yerr, xlabel='',
                     ylabel='', k=k, b=b, caption=None,
                     subplot=plt, color=color[1])
    plt.legend()
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


def make_micro(t, color):
    name = 't='+str(t)+'.csv'
    data = make_dic(name)
    data['U_p'] = np.array(data['U_p'])
    data['U_e'] = np.array(data['U_e'])
    data['R'] = 10*data['U_p']/data['U_e']
    data['Q'] = data['U_p']*data['U_e']/10/10**6
    xerr = (2*(0.0035/100)**2+(0.01/100)**2)**0.5
    yerr = (2*(0.0035/100)**2)**0.5
    k, b, sigma = make_graffic(y=data['R'], x=data['Q'], xlabel='Q, Вт',
                               ylabel='R, Ом', caption_point='T='+str(t),
                               xerr=xerr*data['Q'],
                               yerr=yerr*data['R'], b=1, color=color)
    return k, b, sigma


def make_all():
    t_all = [22, 30, 40, 50, 60, 70]
    for i in range(len(t_all)):
        k, b, sigma = make_micro(t_all[i], [color_point[i], color_line[i]])
        big_data['t'].append(t_all[i]+273)
        big_data['R0'].append(b)
        big_data['R/Q'].append(k)
        big_data['sigma'].append(sigma/k)
        print(k,b, sigma, t_all[i])
    plt.savefig('Нагрузка')
    plt.show()
    big_data['t']=np.array(big_data['t'])
    big_data['R0']=np.array(big_data['R0'])
    big_data['R/Q']=np.array(big_data['R/Q'])
    big_data['sigma']=np.array(big_data['sigma'])
    plt.show()
    yerr=[big_data['R0'][i]*big_data['sigma'][i] for i in range(len(big_data['R0']))]
    k, b, sigma = make_graffic(big_data['t'], y=big_data['R0'], xlabel='T, K', ylabel='$R_0$, Ом',
                 caption_point='', xerr=0, yerr=yerr)
    plt.savefig('R(T)')
    plt.show()
    make_micro(50, None)
    R_273=b+273*k
    print('alpha = ', k/R_273*10**3, '+-', sigma/R_273*10**3, '*10^3')
    big_data['ksi'] =1/2/np.pi/347*10**3*np.log(10/0.05)* 1/ big_data['R/Q']*k*10**3
    big_data['ksi_err'] = big_data['ksi']*((sigma/k)**2+
                                               (np.mean(big_data['sigma']))**0.5)
       


big_data = {'t': [], 'R0': [], 'R/Q': [], 'sigma': []}
color_point = ['forestgreen', 'darkgoldenrod',
               'maroon',   'darkblue', 'crimson', 'indigo']
color_line = ['rosybrown', 'mediumpurple', 'sandybrown',
              'gold',  'greenyellow', 'lightgreen',
              'lightblue', 'lightsteelblue', 'plum', 'pink']
make_all()
print(big_data)
