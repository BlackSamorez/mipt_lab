# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:32:43 2022

@author: anna
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
from scipy.optimize import curve_fit
import matplotlib.colors


def read_csv(file_name):
    with open(file_name) as file:
        reader = list(csv.reader(file, delimiter=';',
                      quotechar=',', quoting=csv.QUOTE_MINIMAL))
    return reader


def make_latex_table(data):
    table = []
    table.append("\\begin{table}[h!]".replace('//', '\\'))
    table.append('\caption{}'.replace('/', '\\'))
    table.append("\label{}".replace('/', '\\'))
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
    subplot.plot(x, k*x+b, label=caption, color=color, linewidth=1)


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
    sigma = k*((sigma/k)**2+(np.mean(yerr)/np.mean(y))**2)**0.5

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


def make_all_temperature():
    T = np.array([22.4, 30.1, 40.2, 50.1, 55.1, 60.1])
    for i in range(len(T)):
        k, b, sigma = make_micro_temperature(
            T[i], [color_point[i], color_line[i]])
        sigma = k * 2*740/10**3 * ((1/740)**2+(sigma/k)**2)**0.5
        k = k * 2*740/10**3
        big_data['T'].append( T[i]+273)
        big_data['c'].append(k)
        big_data['c_sigma'].append(sigma) 
    plt.savefig('Temperature')
    plt.show()
    print(big_data['c'])
    big_data['c'] = np.array(big_data['c'])
    big_data['c_sigma'] = np.array(big_data['c_sigma'] )
    
    k, b, sigma = make_graffic(big_data['T'], y=big_data['c']**2/10**3, xlabel='T, K', 
                 ylabel='$c^2, (м/c^2)^2$', caption_point='', 
                 xerr=0, yerr=2*big_data['c']*big_data['c_sigma']/10**3, b=0)
    print('gamma_air_temp =', k*29/8.3, '+-', sigma*29/8.3)
    plt.savefig('CC_T')
    plt.show()


def make_micro_temperature(t, color):
    s = 'T='+str(t)+'.csv'
    data = make_dic(s)
    f = data['f']
    k = data['k']
    s = 't='+str(t)+'$^\circ C$'
    s_pic = s + '.png'
    k, b, sigma = make_graffic(k, f, xlabel='k - номер резонанса', ylabel='f, Гц',
                               caption_point=s, xerr=0, yerr=0.5, b=1, filename=s_pic,
                               color=color)
    return k, b, sigma


def make_all_frequency():
    F = np.array([4412, 3707, 3011, 5092, 5406])
    for i in range(len(F)):
        k, sigma = make_micro_frequency_air(
            F[i], [color_point[i], color_line[i]])
        big_data['lambda_air'].append(k*2)
        big_data['f_air'].append(F[i])
        big_data['lambda_sigma_air'].append(sigma*2)

    plt.savefig('Frequency_air')
    plt.show()

    F = np.array([4398, 4665, 3506, 3039, 2624])
    for i in range(len(F)):
        k, sigma = make_micro_frequency_co2(
            F[i], [color_point[i], color_line[i]])
        big_data['lambda_co2'].append(k*2)
        big_data['f_co2'].append(F[i])
        big_data['lambda_sigma_co2'].append(sigma*2)

    plt.savefig('Frequency_co2')
    plt.show()

    big_data['lambda_air'] = np.array(big_data['lambda_air'])
    big_data['lambda_sigma_air'] = np.array(big_data['lambda_sigma_air'])
    k, b, sigma = make_graffic(x=1/big_data['lambda_air']*10**3, y=big_data['f_air'],
                               xlabel='1/$\lambda$, 1/м', ylabel='f, Гц',
                               caption_point='Воздух',
                               xerr=1/big_data['lambda_air']**2 *
                               big_data['lambda_sigma_air']*10**3,
                               yerr=1, b=0, color=[color_point[3], color_line[0]])
    print('c_air= ', k, '+-', sigma)
    big_data['lambda_co2'] = np.array(big_data['lambda_co2'])
    big_data['lambda_sigma_co2'] = np.array(big_data['lambda_sigma_co2'])
    k, b, sigma = make_graffic(x=1/big_data['lambda_co2']*10**3, y=big_data['f_co2'],
                               xlabel='1/$\lambda$, 1/м', ylabel='f, Гц',
                               caption_point='Углекислый газ',
                               xerr=1/big_data['lambda_co2']**2 *
                               big_data['lambda_sigma_co2']*10**3,
                               yerr=1, b=0, color=[color_point[1], color_line[1]])
    print('c_co2= ', k, '+-', sigma)
    plt.savefig('f(la)')
    plt.show()


def make_micro_frequency_co2(t, color):
    s = 'Fc='+str(t)+'.csv'
    data = make_dic(s)
    L = data['L']
    k = data['k']
    for i in range(len(k)):
        k[i] += 5
    s = 'F='+str(t)+'Гц'
    s_pic = s + '.png'
    k, b, sigma = make_graffic(k, L, xlabel='k - номер резонанса', ylabel='L, мм',
                               caption_point=s, xerr=0, yerr=1, b=1, filename=s_pic,
                               color=color)
    return k, sigma


def make_micro_frequency_air(t, color):
    s = 'F='+str(t)+'.csv'
    data = make_dic(s)
    L = data['L']
    k = data['k']
    s = 'F='+str(t)+'Гц'
    s_pic = s + '.png'
    k, b, sigma = make_graffic(k, L, xlabel='k - номер резонанса', ylabel='L, мм',
                               caption_point=s, xerr=0, yerr=1, b=1, filename=s_pic,
                               color=color)
    return k, sigma


big_data = {}
big_data['lambda_air'] = []
big_data['f_air'] = []
big_data['lambda_sigma_air'] = []

big_data['lambda_co2'] = []
big_data['f_co2'] = []
big_data['lambda_sigma_co2'] = []

big_data['c'] = []
big_data['c_sigma'] = []
big_data['T'] = []


color_point =['black', 'red', 'green', 'brown','blue', 'y', 'm']
color_line = ['rosybrown', 'mediumpurple', 'sandybrown',
              'gold',  'greenyellow', 'lightgreen',
              'lightblue', 'lightsteelblue', 'plum', 'pink']


make_all_temperature()
make_all_frequency()

data = {}
data['c']=big_data['c']
data['c_sigma'] = big_data['c_sigma']
data['T'] = big_data['T']
arr = []
for key in data.keys():   
    a = list(data[key])
    for i in range(len(a)):
        a[i] = round(a[i], 3)
        a[i] = str(a[i])
    a.insert(0, key)
    arr.append(a)
data = arr
data = pd.DataFrame(data).T.values.tolist()
table = make_latex_table(data)
print(*table)

data = {}
data['lambda_co2']=big_data['lambda_co2']
data['f_co2'] = big_data['f_co2']
data['lambda_sigma_co2'] = big_data['lambda_sigma_co2']
arr = []
for key in data.keys():   
    a = list(data[key])
    for i in range(len(a)):
        a[i] = round(a[i], 3)
        a[i] = str(a[i])
    a.insert(0, key)
    arr.append(a)
data = arr
data = pd.DataFrame(data).T.values.tolist()
table = make_latex_table(data)
print(*table)
