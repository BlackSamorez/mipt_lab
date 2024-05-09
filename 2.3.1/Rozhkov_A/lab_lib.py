import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from scipy.optimize import curve_fit

def countWithSigma(val, arr):
    sigma = 0
    for i in arr:
        sigma += (i[1] / i[0]) ** 2
    sigma = np.sqrt(sigma) * val
    return [val, sigma]

def texAns(val, precision):
    return "$({} \pm {})$".format(np.round(val[0], precision), np.round(val[1], precision))

def meanWithInacc(arr):
    mean = np.mean([x[0] for x in arr])
    n = len(arr)

    rand_inacc = np.sqrt(sum([ 1 / (n * (n - 1)) * (x[0] - mean)**2 for x in arr]))
    inacc = np.sqrt(rand_inacc**2 + np.mean([x[1] for x in arr])**2)

    return [mean, inacc]

def texTable(table):
    print("")
    print(r"""
\begin{table}[!ht]
    \centering
    \begin{tabular}{|%s}
        \hline
""" % ("c|" * len(table[0])))

    for i in table:
        print("        ", end = "")
        for j in range(len(i)):
            print(i[j], end = "")
            if j != len(i) - 1:
                print(" & ", end = "")

        print(r"\\ \hline")


    print("""
    \end{tabular}
    \caption{}
    \label{}
\end{table}
""")

def make_mnk(file, title, xlabel, ylabel, x, y, dx, dy):

    mpl.rcParams['font.size'] = 16                   # Управление стилем, в данном случаем - размером шрифта
    plt.figure(figsize = (8,8), facecolor = "white") # Создаем фигуру

    # Подписываем оси и график
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    def func(x, k, b):
        return x * k + b

    popt, pcov = curve_fit(func, x, y, p0 = (0.0, 0.0))
    k, b = popt
    dk, db = np.sqrt(np.diag(pcov))

    print("k: ({} +- {})".format(k, dk))
    print("b: ({} +- {})".format(b, db))

    #plt.errorbar(x, y, "or", markersize = 9, label = 'Экспериментальные значения')
    plt.errorbar(x, y, xerr = dx, yerr = dy, fmt='.r', label = 'Экспериментальные значения')
    #plt.plot(x, y, "+b", label = "Экспериментальные данные", linewidth = 1)

    x_lin = np.linspace(x[0], x[-1], 1000)
    plt.plot(x_lin, func(x_lin, k, b), "b", label = "Аппроксимация")

    plt.grid(visible = True, which = 'major', axis = 'both', alpha = 1, linewidth = 0.9)   # Активируем сетку
    plt.grid(visible = True, which = 'minor', axis = 'both', alpha = 0.5, linestyle = ':')

    plt.minorticks_on()
    plt.tight_layout()
    plt.legend(loc = "best", fontsize = 12) # Активируем легенду графика

    plt.savefig("{}".format(file))
    plt.show()

    return [k, dk], [b, db]
