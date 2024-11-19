import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plt_singleton(title, xlabel, ylabel):
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  plt.minorticks_on()
  plt.grid(linestyle='-', which='major')
  plt.grid(linestyle='--', which='minor')
  plt.legend()

from scipy.optimize import curve_fit

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
