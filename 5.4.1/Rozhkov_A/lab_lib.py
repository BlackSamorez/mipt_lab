import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import curve_fit

def countWithSigma(val, arr):
    sigma = 0
    for i in arr:
        sigma += (i[1] / i[0]) ** 2
    sigma = np.sqrt(sigma) * abs(val)
    return [val, sigma]

def texAns(val):
    if len(val) == 1 or val[1] == 0:
        return r"$%g$" % (val[0])

    inacc = abs(val[1])
    precision = 0

    if inacc > 1:
        while int(inacc) > 10:
            precision -= 1
            inacc /= 10
        if 0.1 <= inacc and inacc <= 0.13 or 0.87 <= inacc and inacc <= 1:
            precision += 1
    else:
        while inacc < 1:
            precision += 1
            inacc *= 10
        if 1.0 <= inacc and inacc <= 1.3 or 9.7 <= inacc and inacc < 10:
            precision += 1

    return r"$%.*f \pm %.*f$" % (precision, np.round(val[0], precision), precision, abs(np.round(val[1], precision)))

def meanWithInacc(arr):
    mean = np.mean([x[0] for x in arr])
    n = len(arr)

    rand_inacc = np.sqrt(sum([ 1 / (n * (n - 1)) * (x[0] - mean)**2 for x in arr]))
    inacc = np.sqrt(rand_inacc**2 + np.mean([x[1] for x in arr])**2)

    return [mean, inacc]

def texTable(table, caption=""):
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


    print(r"""
    \end{tabular}
    \caption{""" + caption + r"""}
    \label{}
\end{table}
""")

def mnk(x, y):
    def func(x, k, b):
        return x * k + b

    popt, pcov = curve_fit(func, x, y, p0 = (0, 0))
    k, b = popt
    dk, db = np.sqrt(np.diag(pcov))

    return [k, dk], [b, db]

def mnk_line_get_points(x, y, dx, dy, k_b):
    minx = min(x) - max(dx)
    miny = min(y) - max(dy)
    maxx = max(x) + max(dx)
    maxy = max(y) + max(dy)

    p_x = [minx, maxx]
    p_y = [minx * k_b[0][0] + k_b[1][0], maxx * k_b[0][0] + k_b[1][0]]

    if miny > minx * k_b[0][0] + k_b[1][0]:
        p_x[0] = (miny - k_b[1][0]) / k_b[0][0]
        p_y[0] = miny

    if maxy < maxx * k_b[0][0] + k_b[1][0]:
        p_x[1] = (maxy - k_b[1][0]) / k_b[0][0]
        p_y[1] = maxy

    return p_x, p_y

def make_plot_no_mnk(file, title, xlabel, ylabel, x, y, dx, dy):

    mpl.rcParams['font.size'] = 16                   # Управление стилем, в данном случаем - размером шрифта
    plt.figure(figsize = (10,8), facecolor = "white") # Создаем фигуру

    # Подписываем оси и график
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    #plt.errorbar(x, y, "or", markersize = 9, label = 'Экспериментальные значения')
    plt.errorbar(x, y, xerr = dx, yerr = dy, fmt='.r', label = 'Экспериментальные значения')
    #plt.plot(x, y, "+b", label = "Экспериментальные данные", linewidth = 1)

    plt.grid(visible = True, which = 'major', axis = 'both', alpha = 1, linewidth = 0.9)   # Активируем сетку
    plt.grid(visible = True, which = 'minor', axis = 'both', alpha = 0.5, linestyle = ':')

    plt.minorticks_on()
    plt.tight_layout()
    plt.legend(loc = "best", fontsize = 12) # Активируем легенду графика

    plt.savefig("{}".format(file))
    plt.show()

def make_plot_with_table_values(file, title, xlabel, ylabel, x, y, dx, dy, k_b, table_x, table_y):

    mpl.rcParams['font.size'] = 16                   # Управление стилем, в данном случаем - размером шрифта
    plt.figure(figsize = (10,8), facecolor = "white") # Создаем фигуру

    # Подписываем оси и график
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    #plt.errorbar(x, y, "or", markersize = 9, label = 'Экспериментальные значения')
    plt.errorbar(x, y, xerr = dx, yerr = dy, fmt='.r', label = 'Экспериментальные значения')
    #plt.plot(x, y, "+b", label = "Экспериментальные данные", linewidth = 1)

    if table_x != 0 and table_y != 0:
        plt.errorbar(table_x, table_y, fmt='xb', label = 'Табличные значения')

    x_lin = np.linspace(min(x), max(x), 1000)
    plt.plot(x_lin, [i * k_b[0][0] + k_b[1][0] for i in x_lin], "b", label = "Аппроксимация")

    plt.grid(visible = True, which = 'major', axis = 'both', alpha = 1, linewidth = 0.9)   # Активируем сетку
    plt.grid(visible = True, which = 'minor', axis = 'both', alpha = 0.5, linestyle = ':')

    plt.minorticks_on()
    plt.tight_layout()
    plt.legend(loc = "best", fontsize = 12) # Активируем легенду графика

    plt.savefig("{}".format(file))
    plt.show()

def make_polyfit(file, title, xlabel, ylabel, x, y, dx, dy, degree):

    mpl.rcParams['font.size'] = 16
    plt.figure(figsize = (10,8), facecolor = "white")

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.errorbar(x, y, xerr = dx, yerr = dy, fmt='.r', label = 'Экспериментальные значения')

    popt = np.polyfit(x, y, degree)

    def func(x):
        return (sum([popt[degree-i]*x[0]**i for i in range(degree+1)]), sum([(x[1]*popt[degree-i]*x[0]**(i-1)) for i in range(1, degree+1)]))

    x_lin = np.linspace(min(x), max(x), 1000)
    plt.plot(x_lin, [func((i, 0))[0] for i in x_lin], "b", label = "Аппроксимация")

    plt.grid(visible = True, which = 'major', axis = 'both', alpha = 1, linewidth = 0.9)   # Активируем сетку
    plt.grid(visible = True, which = 'minor', axis = 'both', alpha = 0.5, linestyle = ':')

    plt.minorticks_on()
    plt.tight_layout()
    plt.legend(loc = "best", fontsize = 12) # Активируем легенду графика

    plt.savefig("{}".format(file))
    plt.show()

    return func, popt


def make_mnk(file, title, xlabel, ylabel, x, y, dx, dy):

    k, b = mnk(x, y)

    make_plot_with_table_values(file, title, xlabel, ylabel, x, y, dx, dy, (k, b), 0, 0)

    return k, b

def make_mnk_with_table_values(file, title, xlabel, ylabel, x, y, dx, dy, table_x, table_y):

    k, b = mnk(x, y)

    make_plot_with_table_values(file, title, xlabel, ylabel, x, y, dx, dy, (k, b), table_x, table_y)

    return k, b

def make_mnk_direct_prop(file, title, xlabel, ylabel, x, y, dx, dy):

    mpl.rcParams['font.size'] = 16                   # Управление стилем, в данном случаем - размером шрифта
    plt.figure(figsize = (10,8), facecolor = "white") # Создаем фигуру

    # Подписываем оси и график
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    def func(x, k):
        return x * k

    popt, pcov = curve_fit(func, x, y, p0 = (0.0))
    k = popt[0]
    dk = np.sqrt(np.diag(pcov))[0]

    print("k: ({} +- {})".format(k, dk))

    #plt.errorbar(x, y, "or", markersize = 9, label = 'Экспериментальные значения')
    plt.errorbar(x, y, xerr = dx, yerr = dy, fmt='.r', label = 'Экспериментальные значения')
    #plt.plot(x, y, "+b", label = "Экспериментальные данные", linewidth = 1)

    x_lin = np.linspace(x[0], x[-1], 1000)
    plt.plot(x_lin, func(x_lin, k), "b", label = "Аппроксимация")

    plt.grid(visible = True, which = 'major', axis = 'both', alpha = 1, linewidth = 0.9)   # Активируем сетку
    plt.grid(visible = True, which = 'minor', axis = 'both', alpha = 0.5, linestyle = ':')

    plt.minorticks_on()
    plt.tight_layout()
    plt.legend(loc = "best", fontsize = 12) # Активируем легенду графика

    plt.savefig("{}".format(file))
    plt.show()

    return [k, dk]
