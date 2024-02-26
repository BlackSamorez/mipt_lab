import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

def readFiles(files):
    dfs = []
    for f in files:
        dfs += [pd.read_csv(f)]
    return dfs 

def drawFreq(dfs, files):
    z = np.linspace(0, 5, num=100)
    plt.figure(figsize=(7, 4))
    plt.xlabel('$n$')
    plt.ylabel('$f$, Hz')
    nums = [j for j in range(1, dfs[0].__len__() + 1)]
    for i in range (dfs.__len__()):
        for j in range(1, dfs[i].__len__()):
            print(nums)
            print(dfs[i].iloc[j, 1:])
            plt.scatter(nums, dfs[i].iloc[j, 1:], s=5)
            a, b = np.polyfit(nums, dfs[i].iloc[j, 1:], deg=1)
            plt.plot(z, a * z + b, label=f'$y = {a:.2f}x + {b:.2f}$')
        plt.grid()
        plt.legend()
        plt.savefig(files[i])

dfs = readFiles(['air.csv', 'co2.csv', 'temp.csv'])
drawFreq(dfs[:2], ['air.pgf', 'co2.pgf'])
