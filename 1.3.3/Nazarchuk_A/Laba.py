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
                 b=None, filename=None, color=None, koef=[0.9, 1.1]):
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

    make_line_grafic(xmin=min(x)*koef[0], xmax=max(x)*koef[1], xerr=xerr, yerr=yerr, xlabel='',
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
    
    
def draw(data, start, finish, color):
    x = data['p'][start:finish]
    y = data['Q'][start:finish]
    xerr = 0.01 * x
    yerr = (0.01 ** 2 + (0.3/data['t'][start:finish])**2)**0.5 * y
    
    if (data['w'][start]==0):
        caption = 'Лам., d=' + str(data['d'][start])+'мм'
        b = 0
        k, b, sigma = make_graffic(x, y*10**6, xlabel='$\Delta P, Па$', ylabel='Q,$10^{-6} м^3$/c', 
                     caption_point=caption, xerr=xerr, yerr=yerr, color=color, b=b, koef=[0.5, 1.5])
        return k/10**6, b/10**6, [sigma[0]/10**6, sigma[1]/10**6]
    else:
        caption = 'Турб., d=' + str(data['d'][start])+'мм'
        make_point_grafic(x, y*10**6, xlabel='$\Delta P, Па$', ylabel='Q,$10^{-6}$ 1/c', 
                     caption=caption, xerr=xerr, yerr=yerr, color=color[1])
        k, b, sigma = approx(x, y, b=None, sigma_y=yerr)
        sigma[0] = abs(k*((sigma[0]/k)**2+(np.mean(yerr)/np.mean(y))**2 +
               (np.mean(xerr)/np.mean(x))**2)**0.5)
        return k, b, sigma
    
def make_delta():
    data = make_dic('P(x).csv')
    data['p'] *= koef
    data['d'] *= 10**(-3)
    x = data['l']
    y = data['p']
    make_point_grafic(x[:4], y[:4], xlabel='x, cм', ylabel='P, Па', caption='d=3.95 мм',
                 xerr=0, yerr=0.01*y[:4])
    make_point_grafic(x[4:], y[4:], xlabel='x, cм', ylabel='P, Па', caption='d=5.1 мм',
                 xerr=0, yerr=0.01*y[4:], color='red')
    plt.legend()

def make_q():
    data = make_dic('Q=const.csv')
    data['p'] *= koef
    data['d'] *= 10**(-3)/2
    data['Q'] = data['Q']/data['t']/10**3
    data['Q_ln'] = np.log(data['Q']/data['Q'][0])
    data['R_ln'] = np.log(data['d']/data['d'][0])
    x = np.array([data['R_ln'][i] for i in range(len(data['R_ln'])) if data['boo'][i]==0])
    y = np.array([data['Q_ln'][i] for i in range(len(data['R_ln'])) if data['boo'][i]==0])
    xerr = 0.01 * x
    yerr = 0.01 * y
    data['Q_ln'] = np.log(data['Q']/data['Q'][1])
    data['R_ln'] = np.log(data['d']/data['d'][1])
    k_lam, b, sigma_lam = make_graffic(x, y, xlabel='ln(R/$R_0$)', ylabel='ln(Q/$Q_0$)', 
                 caption_point='Ламинарный', xerr=xerr, yerr=yerr, b=0, 
                 color=colors[0])
    x = np.array([data['R_ln'][i] for i in range(len(data['R_ln'])) if data['boo'][i]==1])
    y = np.array([data['Q_ln'][i] for i in range(len(data['R_ln'])) if data['boo'][i]==1])
    xerr = 0.01 * x
    yerr = 0.01 * y
    k_tur, b, sigma_tur = make_graffic(x, y, xlabel='ln(R/$R_0$)', ylabel='ln(Q/$Q_0$)', 
                 caption_point='Турбулентный', xerr=xerr, yerr=yerr, b=0, 
                 color=colors[3])
    print('lami = ', k_lam, '+-', sigma_lam[0], 'e = ', sigma_lam[0]/k_lam*100, '%')
    print('turb = ', k_tur, '+-', sigma_tur[0], 'e = ', sigma_tur[0]/k_tur*100, '%')
    

def make_strange():
    data = make_dic('Main.csv')
    data['p'] *= koef
    data['Q'] = data['Q']/data['t']/10**3
    data['R'] = data['d']/2/10**3
    nu = 19.97 * 10**-6
    Re = rho * data['Q']/np.pi/data['R']/nu
    phi = data['R']**5*data['p']*np.pi/l/rho/data['Q']**2
    x = phi
    y = Re
    
    xerr = (30*0.01**2)**0.5*x
    yerr = (0.01**2*2)**0.5*y
    make_point_grafic(x, y, xlabel='$\psi$', ylabel='Re', 
                 caption='', xerr=xerr, yerr=yerr)
    Re_kr = 1700
    x = np.array([phi[i] for i in range(len(data['Q'])) if Re[i]>Re_kr])
    y = np.array([Re[i] for i in range(len(data['Q'])) if Re[i]>Re_kr])
    xerr = (30*0.01**2)**0.5*x
    yerr = (0.01**2*2)**0.5*y
    k, b, sigma = make_graffic(x, y, xlabel='$\psi$', ylabel='Re', caption_point='Турбулентный', 
                 xerr=xerr, yerr=yerr, color=colors[4])
    print(k)

    
def make_all():
    data = make_dic('Main.csv')
    data['p'] *= koef
    data['Q'] = data['Q']/data['t']/10**3
    start = 0
    num = 0
    d=[data['d'][0]]
    d_sigma = [data['sigma_d'][0]]
    boo = 0
    k = [];b = [];sigma = [];x = [];y = [];nu=[];sigma_nu=[];Re_kr=[]
    for i in range(len(data['w'])):
        if not(data['w'][i] == boo):
            ki, bi, sigmai = draw(data, start, i, colors[num])
            d.append(data['d'][i])
            d_sigma.append(data['sigma_d'][i])
            k.append(ki)
            b.append(bi)
            sigma.append(sigmai)
            start = i+1
            num+=1
            boo = 1 - boo
    ki, bi, sigmai = draw(data, start, len(data['w'])-1, colors[num])
    k.append(ki)
    b.append(bi)
    sigma.append(sigmai)   
    plt.legend()     
    data['d'] = np.array(d)
    data['sigma_d'] = np.array(d_sigma)
    i = 0
    while i <(len(k)-1):
        f = (b[i]-b[i+1])/(k[i+1]-k[i])
        x.append(f)
        y.append(10**6*(b[i]+f*k[i]))
        i+=2
    plt.scatter(x, y, linewidth=3, color='darkblue')
    y = np.array(y)
    i = 0
    while i <(len(k)-1):
        f = 1/k[i] * np.pi*data['d'][i]**4/16/8/l*10**(6-12)
        nu.append(f[0])
        sig = ((sigma[i][0]/k[i])**2+16*(data['sigma_d'][i]/data['d'][i])**2)**0.5*f
        sigma_nu.append(sig[0])
        i+=2
    nu = np.array(nu)
    sigma_nu = np.array(sigma_nu)
    print('nu = ', nu)
    print('sigma_nu = ',*sigma_nu)
    
    i=0
    while i <(len(k)-1):
       Re_kr.append((rho * y[i//2]/nu[i//2]/np.pi/data['d'][i]*2*10**3)[0]) 
       i+=2
    print('Re_kr = ',*Re_kr)
    plt.savefig('Q(P)')
    plt.show()
    make_delta()
    plt.savefig('P(x)')
    plt.show()
    make_q()
    plt.savefig('Q(R)')
    plt.show()
    make_strange()
    plt.savefig('Re(psi)')
    
    
    
    
    
    
    
koef = 0.2 * 9.8067 * 0.9910   
l = 0.4 
rho = 1.185
colors = [['forestgreen', 'rosybrown'], ['darkgoldenrod', 'mediumpurple'],
          ['maroon', 'sandybrown'], ['darkblue', 'gold'], 
          ['crimson', 'greenyellow'], ['indigo', 'lightgreen']]

make_all()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    