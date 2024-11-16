from functools import reduce
from operator import add
from .var import Var, GroupVar
import sympy as sp
import numpy as np

"""
Данный файл отвечает за переопределение базовых операций для выполнения их с бъектами класса var
и перерасчёта погрешностей косвенных измерений
Входящие функции:
'sqrt', 'sin', 'cos', 'tg', 'ctg', 'arctg', 'arcctg', 'arcsin', 'arccos', 'sh', 'ch', 'th', 'cth', 'arcth', 'arcsh', 
'exp', 'ln', 'mean'
"""


def _mono_function(x, name_func_for_sympy: str, name_func_for_numpy: str = None,
                   real_name: str = None):
    """
    Эта функция позволяет создать функцию от одной переменной.
    Позволяет без головной боли запускать функции от разных типов данных не вызывая проблем
    :param x: Аргумент данной функции
    :param name_func_for_sympy: Название функции для sympy
    :param name_func_for_numpy: Название функции для numpy
    :param real_name: Имя функции, удобное для пользователя, должно быть перечислено в списке выше
    :return: Результат выполнения данной функции
    """
    if name_func_for_numpy is None:
        name_func_for_numpy = name_func_for_sympy
    if real_name is None:
        real_name = name_func_for_sympy

    if isinstance(x, GroupVar):
        return GroupVar(tuple(_all_funcs[real_name](var) for var in x))
    if isinstance(x, Var):
        return Var(getattr(sp, name_func_for_sympy)(x._story))
    else:
        return getattr(np, name_func_for_numpy)(x)


def sqrt(x):
    return _mono_function(x, 'sqrt')


def sin(x):
    return _mono_function(x, 'sin')


def cos(x):
    return _mono_function(x, 'cos')


def tg(x):
    return _mono_function(x, 'tan', real_name='tg')


def ctg(x):
    if isinstance(x, Var):
        return Var(sp.tan(sp.pi / 2 - x._story))
    elif isinstance(x, GroupVar):
        return _mono_function(x, 'ctg', real_name='ctg')
    else:
        return np.tan(np.pi / 2 - x)


def arctg(x):
    return _mono_function(x, 'atan', name_func_for_numpy='arctan', real_name='arctg')


def arcctg(x):
    if isinstance(x, Var):
        return Var(sp.pi / 2 - sp.atan(x._story))
    elif isinstance(x, GroupVar):
        return _mono_function(x, 'ctg', real_name='arcctg')
    else:
        return np.pi / 2 - np.arctan(x)


def arcsin(x):
    return _mono_function(x, 'asin', name_func_for_numpy='arcsin', real_name='arcsin')


def arccos(x):
    return _mono_function(x, 'acos', name_func_for_numpy='arccos', real_name='arccos')


def sh(x):
    return _mono_function(x, 'sinh', real_name='sh')


def ch(x):
    return _mono_function(x, 'cosh', real_name='ch')


def th(x):
    return _mono_function(x, 'tanh', real_name='th')


def cth(x):
    if isinstance(x, GroupVar):
        return _mono_function(x, 'cth', real_name='cth')
    return 1 / th(x)


def arcth(x):
    return _mono_function(x, 'atanh', name_func_for_numpy='arctanh', real_name='arcth')


def arcsh(x):
    return _mono_function(x, 'asinh', name_func_for_numpy='arcsinh', real_name='arcsh')


def arcch(x):
    return _mono_function(x, 'acosh', name_func_for_numpy='arccosh', real_name='arcch')


def exp(x):
    return _mono_function(x, 'exp')


def ln(x):
    return _mono_function(x, 'log', real_name='ln')


def mean(x: GroupVar):
    return reduce(add, x)/len(x)


_all_funcs = {'sqrt': sqrt, 'sin': sin, 'cos': cos, 'tg': tg, 'ctg': ctg, 'arctg': arctg, 'arcctg': arcctg,
              'arcsin': arcsin, 'arccos': arccos, 'sh': sh, 'ch': ch, 'th': th, 'cth': cth, 'arcth': arcth,
              'arcsh': arcch, 'exp': exp, 'ln': ln, 'mean': mean}


def step(x: GroupVar):
    """
    Возвращает просто разницу между переменными(x[i]-x[i-1]).
    Иногда это лучше чем использовать МНК
    """
    return GroupVar(tuple(x[i]-x[i-1] for i in range(1, len(x))))
