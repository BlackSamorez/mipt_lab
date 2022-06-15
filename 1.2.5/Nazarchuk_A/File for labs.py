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


def make_grafic(x, y, xlabel, ylabel, caption, xerr, yerr, filename=None):
    if filename != None:
        plt.figure(figsize=(8, 5))
    plt.errorbar(x, y, yerr=yerr, xerr=0, linewidth=4,
                 linestyle='', label=caption)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    k = sum(x*y)/sum(x**2)
    sigma = 1 / len(x)**0.5*(sum(y**2)/sum(x**2)-k**2)**0.5
    plt.plot(x, x*k)
    if filename != None:
        plt.savefig(filename)
    plt.show()
    return k, sigma


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


data = make_dic('Vrash.csv')
sigot = find_delivation(data['T'][1:6]) + 0.05
sigotabs = max(sigot / data['T'])
sigom = max(sigot / data['T'] * data['wpr'])
print('угловая скорость прецессии', 1 / np.mean(data['wpr']) * sigom)
k_graffic, sigma_graffic = make_grafic(data['m']*9.81*data['l']/1000/1000, data['wpr'],
            'Момент силы тяжести, Н $\cdot$ м',
            'Угловая скорость прецессии, 1/с',
            'Зависимость угловой скорости прецессии от момента сил',
            xerr=0, yerr=sigom, filename='График')

data['phi'] = np.arctan(data['delta x']/data['L'])
data['Mтр'] = data['m']*9.81*data['l']/1000 / \
    1000 * data['phi'] / 2 / np.pi/data['N']
sigma_sluch = find_delivation(
    data['Mтр'][0]+data['Mтр'][5:])/((len(data['Mтр'][5:])+1)**0.5)
sigma_sist = find_delivation(data['Mтр'][1:6])
sigma_Mtr = (sigma_sluch**2 + sigma_sist**2) ** 0.5
Mtr = np.mean(data['Mтр'])
print('момент сил трения: ', Mtr*1000, '+-', sigma_Mtr*1000)
print()

arr = []
for key in data.keys():
    if key == 'm' or key == 'T' or key == 'N' or key == 'wpr' or key == 'phi':
        a = list(data[key])
        for i in range(len(a)):
            if a[i] == round(a[i], 3):
                a[i] = int(a[i])
            else: 
                a[i]=round(a[i], 3)
            a[i]=str(a[i])
        a.insert(0, key)
        arr.append(a)
data = arr
data = pd.DataFrame(data).T.values.tolist()
table = make_latex_table(data)
# print(*table)


I0 = 1617.8/10**3*78.1**2/8/10**6
data = make_dic('Inertion.csv')
data['Tr'] = data['tr']/data['Nr']
data['Tc'] = data['tc']/data['Nc']
data['Ir'] = I0 * (data['Tr']**2/data['Tc']**2)
sigsr = find_delivation(data['Ir']) / (len(data['Ir'])) ** 0.5
data['sigI'] = ((data['Ir'] * (2 * sigotabs**2 * 4)**0.5)
                ** 2 + sigsr ** 2) ** 0.5
data['sigI'] /= data['Ir']


Ir = sum(data['Ir'])/len(data['Ir'])
sigI = sum(data['sigI'])/len(data['sigI'])
omega = 1/k_graffic/Ir/2/3.14
sigOm = (sigI**2 + sigma_graffic ** 2 / k_graffic**2) ** 0.5 * omega
print('частота вращения ротора: ', omega, '+-', sigOm)
print('момент инерции ротора:', Ir *1000, '+-', sigI*Ir*1000)


