import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

FIGSIZE=(10,5)

def plt_singleton(title, xlabel, ylabel):
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  plt.minorticks_on()
  plt.grid(linestyle='-', which='major')
  plt.grid(linestyle='--', which='minor')
  plt.legend()

def plot_linear(x, y, xerr, yerr, color='blue', label='Аппроксимация', datalabel='',
                fmt='k.', xmin=0, xmax=100):
  plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt=fmt, label=datalabel)
  [a, b] = np.polyfit(x, y, deg=1)
  x = np.linspace(xmin, xmax, 1000)
  plt.plot(x, a * x + b, color=color, label=label)

def fit(f, x, y):
  """Аргументы:
      f - функция, которую мы хотим оптимизировать.
      params - начальное состояние параметров, можно просто передать нули,
          главное чтоб их было нужное количество
      x, y - точки, под которые подгоняем функцию
  """
  if len(x) != len(y):
    raise "Иксов должно быть столько же, сколько и игреков"

  return curve_fit(f, x, y)
