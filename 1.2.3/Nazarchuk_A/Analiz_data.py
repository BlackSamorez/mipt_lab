# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd


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


def make_grafic(x, y, xlabel, ylabel, caption, xerr, yerr, filename=None, subplot=None):
    if xerr == 0 and yerr == 0:
        subplot.scatter(x, y, label=caption)
    else:
        subplot.errorbar(x, y, yerr=yerr, xerr=0, linewidth=4,
                         linestyle='', label=caption)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    k = sum(x*y)/sum(x**2)
    sigma = 1 / len(x)**0.5*(sum(y**2)/sum(x**2)-k**2)**0.5
    b = (np.mean(x*y)-np.mean(x)*np.mean(y))/(np.mean(x**2)-np.mean(x)**2)
    a = np.mean(y)-np.mean(x)*b
    sigma_b = 1/len(x)**0.5*((np.mean(y**2)-np.mean(y)**2) /
                        (np.mean(x**2)-np.mean(x)**2)-b**2)**0.5
    sigma_a = sigma_b *(np.mean(x**2)-np.mean(x)**2) **0.5
    k = np.polyfit(x, y, 1)
    x = np.arange(min(x), max(x), 0.1)
    subplot.plot(x, x*b+a)
    plt.savefig('График.png')
    return a, b*10, sigma_a, sigma_b*10


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


fig, subplot = plt.subplots(figsize=(8, 6))
data = make_dic('Половинки.csv')
k = make_grafic(data['h']**2, data['I']*1000, xlabel='$h^2, м^2$',
                ylabel='I, г$\cdot м^2$', caption='Зависимость момента инерции половинок цилиндра от расстояния от центра до оси вращения', xerr=0.14, yerr=0.05, subplot=subplot)
data = make_dic('Диск.csv')
print(k)

arr = []
for key in data.keys():
    if key == 'I' or key == 'k' or key == 'I_t+I_pl' or key == 'I_pl':
        k = 1000
    else:
        k = 1
    a = list(data[key])
    for i in range(len(a)):
        if a[i] == round(a[i], 3):
            a[i] = int(a[i]*k)
        else:
            a[i] = round(a[i]*k, 3)
        a[i] = str(a[i])
    a.insert(0, key)
    arr.append(a)
data = arr
data = pd.DataFrame(data).T.values.tolist()
table = make_latex_table(data)

print(*table)
