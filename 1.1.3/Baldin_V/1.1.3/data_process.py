import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
# import statistics as stat
# import locale
# from decimal import Decimal
# from scipy.optimize import minimize

# Эти 2 строки сохраняют пустой график с названием 1.pgf.
# Хз зачем это, если у вас будет работать без этого, можно смело удалять.
# plt.savefig('1.pgf')
# plt.show()

# local number format
# locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})


# counts the number of elements which located in a given interval
def perc_counter(data, dev):
    count = 0
    mean = np.mean(data)
    for val in data:
        if abs(val - mean) < dev:
            count += 1
    return count / len(data)

# функция, считывающая сразу несколько файлов(на вход идут пути к ним)
def read_files(files):
    ret = []
    for f in files:
        ret += [pd.read_csv(f)]
    return ret

data = np.array(read_files(['data/my_data.csv'])).flatten()

# print(data)

num_bins = 20

# standart deviation
sigma = np.std(data)
print('stdev =', sigma)

percentage = [perc_counter(data, sigma), perc_counter(data, 2 * sigma),
              perc_counter(data, 3 * sigma)]

print('percentage of values in sigma intervals:', percentage)

# sample mean
mean = np.mean(data)

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(data, num_bins, density = True)

# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mean)) ** 2))
ax.plot(bins, y, label = 'normal distribution')
ax.legend()
ax.set_xlabel('$R$, $\Omega$')
ax.set_ylabel('$y$, $\Omega^{-1}$')

# write sigma value on the given position
# plt.text(504, 0.35, '$\sigma = %.1f$ $\Omega$' % sigma)
# plt.text(504, 0.33, '$\langle R \\rangle = %.1f$ $\Omega$' % average)

y_min, y_max = ax.get_ylim()

plt.vlines(x = [mean - sigma, mean + sigma],
           ymin = y_min, ymax = y_max, linestyle = '--', colors = 'red',
           label = '$\langle R \\rangle \pm \sigma')

plt.vlines(x = [mean - 2 * sigma, mean + 2 * sigma],
           ymin = y_min, ymax = y_max, linestyle = '--', colors = 'blue',
           label = '$\langle R \\rangle \pm 2\sigma$')

plt.vlines(x = [mean - 3 * sigma, mean + 3 * sigma],
           ymin = y_min, ymax = y_max, linestyle = '--', colors = 'green',
           label = '$\langle R \\rangle \pm 3\sigma$')

plt.axvline(x = mean + 2 * sigma, linestyle = '--', color = 'blue')
# Tweak spacing to prevent clipping of ylabel
plt.legend()
fig.tight_layout()
# plt.show()
plt.savefig('graphs/my_hist.pgf')
