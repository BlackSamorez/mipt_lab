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


def make_dic(filename):
    data = np.array(read_csv(filename))
    data = np.transpose(data)
    dic = {}
    for i in range(len(data)):
        dic[data[i][0]] = np.array(data[i][1:]).astype(np.float)
    data = dic
    return data


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
    sigma[0] = abs(k*((sigma[0]/k)**2+(np.mean(yerr)/np.mean(y))**2 +
               (np.mean(xerr)/np.mean(x))**2)**0.5)
    if (b!=0):
        sigma[1] = abs(b*((sigma[1]/b)**2+(np.mean(yerr)/np.mean(y))**2 +
               (np.mean(xerr)/np.mean(x))**2)**0.5)
    else: sigma[1]=0

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
            return k, b, [sigma, 0]
        else:
            def f(x, k, b):
                return x*k + b
            k, sigma = curve_fit(f, xdata=x, ydata=y, sigma=sigma_y)
            sigma_b = np.sqrt(sigma[1][1])
            b = k[1]
            k = k[0]
            sigma = np.sqrt(sigma[0][0])

            return k, b, [sigma, sigma_b]
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


def make_fun(A0, T):
    def f(t, k, b):
        return A0/(1+A0*b*t)-k*0*A0*t/T
    return f


def make_fun_grafic(xmin, xmax, xerr, yerr, xlabel, ylabel, f, k, b, caption, subplot=None, color=None):
    if not subplot:
        subplot = plt
    x = np.arange(xmin, xmax, (xmax-xmin)/10000)
    subplot.plot(x, f(x, k, b), label=caption, color=color)


def A(lmbd, E):
    A = 1/3*s_0*E*(lmbd**2/2+1/lmbd-3/2)
    return A

def draw(lmbd, num, color):
    stri = str(num) +'.csv'
    data = make_dic(stri)
    data['T'] = data['T']/39/5+273
    t_0 = data['t'][0]
    T_0 = data['T'][0]
    data['t'] = data['t'][1:]
    data['T'] = data['T'][1:]
    x = data['t']-t_0
    y = np.log((data['T']-T_0)/T_0)
    yerr = (1/39/5/data['T'])*y
    stri = '$\lambda = '+str(lmbd)+'$'
    k, b, sigma = make_graffic(x, y, xlabel='t, c', ylabel='$ln(\Delta T/T_0)$', 
                 caption_point=stri, xerr=0.1, yerr=yerr, color=color)
    return np.exp(b)*T_0, sigma[1]

def make_gook():
    data = make_dic("Add.csv")
    x = 1+data['lambda']/l_0
    y = (data['m']) * g/10**3
    xerr = ((1/l_0)**2+(1/data['lambda'])**2)**0.5*x
    yerr = g*10**-3
    k, b, sigma = make_graffic(x-1, y, xlabel='', ylabel='f, Н',
                               caption_point='x = $\lambda - 1$', xerr=xerr,
                               yerr=yerr, color=['red', 'grey'], b=0)
    sigma = sigma[0]
    print(k, '  ', b, ' ', sigma, " ", sigma/k*100)
    print("E = ", k/s_0/10**6, '+-', sigma/s_0/10**6, '10^6 H/м^2')
    x = x-1/x**2
    y = (data['m']) * g/10**3
    xerr = ((1/l_0)**2+5*(1/data['lambda'])**2)**0.5*x
    yerr = g*10**-3
    k, b, sigma = make_graffic(x, y, xlabel='',
                               ylabel='f, Н', caption_point='x = $\lambda - 1/\lambda^2}$', xerr=xerr, yerr=yerr)
    sigma = sigma[0]
    print(k, '  ', b, ' ', sigma, " ", sigma/k*100)
    E = k*3/s_0
    E_err = sigma/s_0
    print("E = ", k*3/s_0/10**6, '+-', sigma/s_0/10**6, '10^6 H/м^2')
    plt.savefig('f(l)')
    plt.show()
    
    
    
    colors = [['forestgreen', 'darkgoldenrod',
               'maroon',   'darkblue', 'crimson', 'indigo'], 
              ['rosybrown', 'mediumpurple', 'sandybrown',
              'gold',  'greenyellow', 'lightgreen',
              'lightblue', 'lightsteelblue', 'plum', 'pink']]
    b=[0, 0, 0]
    sigma=[0, 0, 0]
    lmbd = np.array([1.87, 1.96, 1.69])
    b[0], sigma[0] = draw(lmbd[0], 2, [colors[0][0], colors[1][0]])
    b[1], sigma[1] = draw(lmbd[1], 3, [colors[0][1], colors[1][1]])
    b[2], sigma[2] = draw(lmbd[2], 5, [colors[0][2], colors[1][2]])
    plt.savefig('T(t)')
    plt.show()
    
    b=np.array(b)
    print(*b)
    print(*sigma)
    sigma=np.array(sigma)
    x = A(lmbd, E)
    y = b
    xerr = ((E_err/E)**2)**0.5*x
    yerr = sigma
    k, b, sigma = make_graffic(x, y, xlabel='A, Дж', ylabel='$\Delta T$, K', 
                               caption_point='Экстраполяция', xerr=xerr, yerr=yerr, 
                               b=0, color = ['red', 'grey'])
    sigma = sigma[0]
    print('C_l=', 1/k, "+-", sigma/k**2, 'e=', sigma/k*100, '%')
    c_l = 1/k/(rho*l_0/10**3*s_0)
    c_l_err = ((sigma/k)**2+(1/l_0)**2)**0.5*c_l
    print('c_l=', c_l, '+-', c_l_err, 'e=', c_l_err/c_l*100, '%')
    
    data = make_dic("Main.csv")
    data['T'] *= 1/39/5
    x = A(1+(data['H']-156)/l_0, E)
    y = data['T']
    xerr = ((E_err/E)**2+5*(1/data['H'])**2)**0.5*x
    k, b, sigma = make_graffic(x, y, xlabel='A, Дж', ylabel='$\Delta T$, K', 
                               caption_point='Быстрое растяжение', xerr=xerr, yerr=0, b=0)
    sigma = sigma[0]
    print('C_l=', 1/k, "+-", sigma/k**2, 'e=', sigma/k*100, '%')
    c_l = 1/k/(rho*l_0/10**3*s_0)
    c_l_err = ((sigma/k)**2+(1/l_0)**2)**0.5*c_l
    print('c_l=', c_l, '+-', c_l_err, 'e=', c_l_err/c_l*100, '%')
    plt.savefig('T(A)')
    plt.show()
    

m_0 = 142.7+152
l_0 = 107
rho = 1.2 * 10**3
s_0 = 12*1.8*10**-6
g = 9.83
make_gook()
