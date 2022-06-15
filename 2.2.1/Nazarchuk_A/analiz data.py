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
    if type(yerr)==float or type(yerr)==int:
        yerr = [yerr for _ in y]
    if type(xerr)==float or type(xerr)==int:
        xerr = [xerr for _ in x]
        
    if xerr[1] != 0 or yerr[1] != 0:
        subplot.errorbar(x, y, yerr=yerr, xerr=xerr, linewidth=4,
                         linestyle='', label=caption, color=color, ecolor=color,
                         elinewidth= 1, capsize= 3.4, capthick= 1.4)
    else:
        subplot.scatter(x, y, linewidth=0.08, label=caption, color=color,edgecolor='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def make_line_grafic(xmin, xmax, xerr, yerr, xlabel, ylabel, k, b, caption, subplot=None, color=None):
    if not subplot:
        subplot = plt
    x = np.arange(xmin, xmax, (xmax-xmin)/10000)
    subplot.plot(x, k*x+b, label=caption, color=color, linewidth=3)


def make_graffic(x, y, xlabel, ylabel, caption_point, xerr, yerr, k=None, b=None, filename=None):
    fig, subplot = plt.subplots(figsize=(8, 6))
    make_point_grafic(x, y, xlabel=xlabel,
                      ylabel=ylabel, caption=caption_point,
                      xerr=xerr, yerr=yerr, subplot=plt, color='limegreen')
    if k and b:
        make_line_grafic(xmin=min(x)-1, xmax=max(x)+1, xerr=xerr, yerr=yerr, xlabel='',
                         ylabel='', k=k, b=b,
                         caption='Theoretical dependence', subplot=plt, color='red')
    if type(yerr)==float or type(yerr)==int:
        yerr = [yerr for _ in y]
    k, b, sigma = approx(x, y, b, yerr)

    make_line_grafic(xmin=min(x)*0.9, xmax=max(x)*1.1, xerr=xerr, yerr=yerr, xlabel='',
                     ylabel='', k=k, b=b, caption='Approximation',
                     subplot=plt, color='indigo')
    plt.legend()
    plt.savefig(filename)
    plt.show()
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


def make_all(file_name):
    # make all with ln(u/u0) from t
    data = make_dic(file_name)
    p1 = file_name.rindex('.')
    p2 = file_name.rindex('_')
    p = float(file_name[p2+1:p1])
    filename = 'U(t)+'+str(p)[0:2]
    k, b, sigma = approx(data['t'], np.log(
        data['U']/data['U'][0]), b=1, sigma_y=[0])
    make_graffic(data['t'], np.log(data['U']/data['U'][0]), 't, c',
                 '$ln (U/U_0)$', str(p)+' торр', xerr=0, 
                 yerr=2.5/100*np.log(data['U']/data['U'][0]), filename=filename)
    const = -5.5*10**(2)*1200*10**(-3*2)/2 * 10**4
    data['D'] = []
    D = k*const
    big_data['D'].append(D)
    big_data['1/p'].append(1/p)
    print('k ', sigma/k*100, 'V', 30/1200*100, ' L/s ', 0.5/5.5*100)
    sigma = D*np.sqrt((sigma/k)**2+(30/1200)**2+(0.5/5.5)**2)
    big_data['sigma'].append(abs(sigma))
    big_data['eps'].append(sigma/D)


big_data = {}
big_data['D'] = []
big_data['1/p'] = []
big_data['sigma'] = []
big_data['eps']=[]

file_names = ['20190424_1556111038781_62.4.csv',
              '20190424_1556112285774_106.csv',
              '20190424_1556113788279_146.5.csv',
              '20190424_1556109894267_48.5.csv',
              '20190424_1556113788279_22.6.csv']
for file_name in file_names[0:-1]:
    make_all(file_name)
    
# get xerr and k:    
xerr = [7.65/2*i**2 for i in big_data['1/p']]
k, b, sigma = make_graffic(x=big_data['1/p'], y=big_data['D'], 
             xlabel='1/p, 1/торр', ylabel='D, $sm^2/s$', caption_point='Experimental points', 
             xerr=xerr, yerr=big_data['sigma'], filename='D(p)', b=0)

# make latex table
p = [1/i for i in big_data['1/p']]
data = {'D':big_data['D'], 'sigma':big_data['sigma'],'p':p}
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

# get k and D(p0):
sigma[0]=np.sqrt(sigma[0]**2+(2.5/100)**2)
print(k[0], '+-', sigma[0], ' k')

p0=756.2
D_p0= k[0]*1/p0
sigma_d = np.sqrt((sigma[0]**2)/k**2+(7.65/2/p0)**2)*D_p0
print('D_p0' ,D_p0, '+-', sigma_d)

# get v_sr and lyambda:
v_sr = np.sqrt(8*8.31*293/np.pi/4*10**3)
ly = 3*D_p0/v_sr
sigma_ly = sigma_d/D_p0*ly
print('lambda= ',ly*10**3,'+-', sigma_ly*10**3)
sigma = (1.38*10**(-23)*293)/(133.322*p0*ly*10**(-4))
sigma_s = sigma*np.sqrt((7.65/2/p0)**2+(sigma_ly/ly)**2)
print('sigma= ',sigma*10**(19), '+-', sigma_s*10**19)


# make all with he more then air:
make_all(file_names[-1])
k = big_data['D'][-1]/big_data['1/p'][-1]
D_p0_1= k*1/p0
sigma_d_1 = D_p0_1*np.sqrt((7.65/2/p0)**2+(7.65/2*big_data['1/p'][-1])**2+
                           (big_data['sigma'][-1]/big_data['D'][-1])**2)
print(D_p0_1, '+-', sigma_d_1, 'd_po_1')

