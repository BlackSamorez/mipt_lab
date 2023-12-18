import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
# from scipy.optimize import minimize
import statistics as stat
import math

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

# Function to calculate error of linear regression
def lin_err(x, y):
    if len(x) != len(y):
        raise 'len(x) != len(y)'

    a, b = np.polyfit(x, y, 1)
    x_sq = [i ** 2 for i in x]
    y_sq = [i ** 2 for i in y]

    return (1 / (math.sqrt(len(x) - 2) * a)) * math.sqrt((stat.mean(y_sq) -
                                                    stat.mean(y) ** 2) /
                                                    (stat.mean(x_sq) -
                                                     stat.mean(x) ** 2) - a ** 2)


lerm = pd.read_csv('data/lermantov.csv')

# Getting data series from our dataframe
x = lerm.iloc[:, 1]

y = []
for i in range(2, 6):
    y.append(lerm.iloc[:, i])

# print(y)

a = [0] * 2
b = [0] * 2

colors = ['red', 'blue']
labels = ['acsending', 'descending']

fig = plt.figure(0, figsize = (5, 3))
# f, (ax1, ax2) = plt.subplots(1, 2, sharey = True)

for i in range(2):
    a[i], b[i] = np.polyfit(x, y[i], 1)
    plt.scatter(x, y[i], color = colors[i], label = labels[i])
    # plt.scatter(x, a[i + 2] * x + b[i + 2], color = colors[i], label = labels[i])

    plt.plot(x, a[i] * x + b[i], label = '$y = {0:.2f}x + {1:.2f}$'.format(a[i], b[i]), color =
             colors[i])
    # ax2.plot(x, a[i + 2] * x + b[i + 2])

# plt.scatter(x, y[0], color = 'red', label = 'ascending')
# plt.plot(x, a[0] * x + b[0], color = "red")
#
# plt.scatter(x, y[1], color = 'blue', label = 'descending')
# plt.plot(x, a[1] * x + b[1], color = "blue")
#
plt.grid(linestyle = '--')
plt.legend()

plt.xlabel('$P$, N$')
plt.ylabel('$n$, cm')

plt.savefig('graphs/lermant.pgf')

# arithmetic mean of k
coeff_k = stat.mean(a)

# error of coeff_k
eps_k = lin_err(x, y[0])

print('Epsilon_k = {0}'.format(eps_k))

# 2nd part of work
balk = pd.read_csv('data/balka.csv')

# balk = balk.dropna()

# filter(lambda v: v == v, balk)

print('balk = {0}'.format(balk))

P = []
ym = []
# print(balk.info())

for i in range(3, 33, 5):
    P.append(balk.iloc[i, 1:].to_list())
    ym.append(balk.iloc[i - 2, 1:].to_list())

# NANs deletion
for i in range(0, 6):
    P[i] = [p for p in P[i] if str(p) != 'nan']
    ym[i] = [ymax for ymax in ym[i] if str(ymax) != 'nan']


print('P = {0}'.format(P))
print('ym = {0}'.format(ym))
names = ['tree', 'steel', 'latun']


for i in range(1, 4):
    plt.figure(i, figsize = (5, 3))
    a = [0] * 2
    b = [0] * 2

    for j in range(2):
        idx = 2 * i - 2 + j
        # idx = np.isfinite(ym[index]) & np.isfinite(P[index])
        a[j], b[j] = np.polyfit(ym[idx], P[idx], 1)
        print('P[{0}] = {1}'.format(idx, P[idx]))
        print('ym[{0}] = {1}'.format(idx, ym[idx]))
        plt.scatter(ym[idx], P[idx], color = colors[j])
        # print(type(ym[index]))
        if b[j] >= 0:
            fmt = '$y = {0:.2f}x + {1:.2f}$'.format(a[j],
                                                   b[j])
        else:
            fmt = '$y = {0:.2f}x - {1:.2f}$'.format(a[j],
                                                   -b[j])

        plt.plot(np.array(ym[idx]),
                 a[j] * np.array(ym[idx]) + b[j], color = colors[j],
                 label = fmt)

        print('epsilon in {0}: {1}'.format(names[i - 1],
                                           lin_err(ym[idx], P[idx])))

    # graph appearance
    plt.grid(linestyle = '--')
    plt.xlabel('$y_{max}$, mm')
    plt.ylabel('$P$, N')
    plt.legend()
    plt.savefig('graphs/{0}.pgf'.format(names[i - 1]))
