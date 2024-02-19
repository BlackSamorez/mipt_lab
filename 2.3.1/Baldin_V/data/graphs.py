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
        x = data[i]['t']
        y = [np.log(data[i]['P'][j]) for j in range(data[i].__len__())]
        plt.scatter(x, y)
        plt.grid()
        plt.xlabel('$t$, c')
        plt.ylabel('$\ln P$')
        plt.legend()
        plt.savefig(files[i])

data = readFiles(['data1.csv', 'data2.csv', 'data3.csv', 'data4.csv'])
drawGraphs(data, ['data1.pgf', 'data2.pgf', 'data3.pgf', 'data4.pgf'])
