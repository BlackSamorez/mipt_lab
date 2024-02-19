import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

matplotlib.use('pgf')
matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

def readFiles(files):
    data = []
    for f in files:
        data += [pd.read_csv(f)]
    return data

def drawGraphs(data, files):
    if data.__len__() != files.__len__():
        raise 'mismatch of sizes'
    for i in range(data.__len__()):
        plt.figure(figsize=(7, 4))
        plt.xlabel('$t$, c')
        x = data[i]['t']
        z = np.linspace(0, max(x), num=1000)
        if i % 2 == 0:
            y = data[i]['P']
            plt.ylabel('$P$, $10^{-4}$ torr')
            plt.errorbar(x, y, xerr=0, yerr=0.1, fmt='k.')
        else:
            P_LIM = 0.56
            y = [np.log(data[i]['P'][j] - P_LIM) 
                 for j in range(data[i].__len__())]
            plt.errorbar(x, y, xerr=0, yerr=[np.abs(0.2/(j - P_LIM)) 
                                             for j in data[i]['P']], fmt='k.')
            plt.ylabel('$\ln (P - P_{{lim}})$')
        plt.scatter(x, y, s=5)
        [a, b] = np.polyfit(x, y, deg=1)
        plt.plot(z, a * z + b, label=f'$y={a:.2f}x+{b:.2f}')
        plt.grid()
        plt.legend()
        plt.savefig(files[i])

data = readFiles(['data1.csv', 'data2.csv', 'data3.csv', 'data4.csv'])
drawGraphs(data, ['data1.pgf', 'data2.pgf', 'data3.pgf', 'data4.pgf'])
