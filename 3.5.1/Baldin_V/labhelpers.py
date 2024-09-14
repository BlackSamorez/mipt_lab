import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import minimize

def fit(f, params, x, y):
  """Аргументы:
    f - функция, которую мы хотим оптимизировать.
    params - начальное состояние параметров, можно просто передать нули,
        главное чтоб их было нужное количество
    x, y - точки, под которые подгоняем функцию
  """
  if len(x) != len(y):
    raise "Иксов должно быть столько же, сколько и игреков"
  def err(par, x_, y_):
    y1 = f(par, x_)
    return np.sum((y1-y_)**2)

  return minimize(err, params, args=(x, y)).x

def plotLinear(x, y, xerr=0, yerr=0, xlabel='', ylabel='',
               file='plot.pdf', color='blue'):
  plt.figure(figsize=(7, 4))
  plt.errorbar(x, y, fmt='b.', xerr=xerr, yerr=yerr)
  apprres = stats.linregress(x, y)

  z = np.linspace(min(x), max(x), 1000)
  plt.plot(z, apprres.slope * z + apprres.intercept, color='blue')

  plt.grid(which='major', linestyle='-')
  plt.grid(which='minor', linestyle='--')
  plt.minorticks_on()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.savefig(file)

  return apprres

def latexTab(df):
  tab = df.to_latex(index=False, float_format='%.2f')
  tab = tab.replace('\\\\\n', '\\\\ \\hline\n')
  tab = tab.replace('\\toprule', '\\hline')
  tab = tab.replace('\\midrule\n', '')
  tab = tab.replace('\\bottomrule\n', '')
  return tab
