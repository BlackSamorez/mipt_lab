import sys as _sys
from typing import SupportsFloat, Tuple, Union, List, Callable, Optional, Sequence

import numpy as np
from numpy import argmin as _argmin
from numpy import argsort as _argsort
from numpy import var as _var
from scipy.interpolate import UnivariateSpline as _UnivariateSpline
from scipy.optimize import fmin as _fmin
from scipy.optimize import curve_fit as _curve_fit

from lab_cheat import *
from .table import rus_tex_formula
from .var import set_value_accuracy, set_error_accuracy, set_big_number, normalize, GroupVar

_rare_used_funcs = [set_value_accuracy, set_error_accuracy, set_big_number, rus_tex_formula, normalize]

"""
Данный файл содержит в себе особые функции, расширяющие возможности библиотеки.
"""


def slicer(var: GroupVar, left_val: Optional[SupportsFloat] = None,
           right_val: Optional[SupportsFloat] = None,
           excluding: Optional[List[SupportsFloat]] = None) -> Union[List[int]]:
    """
    Создаёт список индексов переменных, лежащих в заданном промежутке,
    исключая точки, наиблизжайшие к значениям из чёрного списка
    :param var: GroupVar с переменными
    :param left_val: Левая граница, если None, то -бесконечность
    :param right_val: Левая граница, если None, то -бесконечность
    :param excluding: Если None, то []
    Ex:
    >>> v = GroupVar(range(10), 0)
    >>> s = slicer(v, left_val=1.1, right_val=8, excluding=[3.1, 6.3, 0])
    >>> v[s].val()
    [2.0, 4.0, 5.0, 7.0, 8.0]
    """
    vals = var.val()
    if left_val is None:
        left_val = float('-inf')
    if right_val is None:
        right_val = float('inf')
    # if excluding is None:
    #     needed_part = filter(lambda x: left_val <= x < right_val, var)
    #     return slice(var.variables.index(min(needed_part), var.variables.index(max(needed_part))))
    excluding_elements = {_argmin(tuple(map(lambda x: abs(x - ex), vals))) for ex in excluding} \
        if excluding is not None else set()
    return sorted(
        list(filter(lambda i: left_val <= vals[i] <= right_val and i not in excluding_elements, range(len(vals)))))


def sorting(x: Union[array, List, GroupVar], y: Union[array, List, GroupVar]) -> Tuple[
    Union[array, List, GroupVar], Union[array, List, GroupVar]]:
    """
    Сортирует точки по значениям по оси X, возвращает отсортированные списки с координатами
    :param x: Итерируемый объект с абсциссами точек
    :param y: Итерируемый объект с абсциссами точек
    :return: кортеж с 2умя элементами: итерируемые объекты с координатами по X и по Y
    """
    if isinstance(x, list) and isinstance(y, list):
        indexes = _argsort(array(x))
        return [x[i] for i in indexes], [y[i] for i in indexes]
    elif isinstance(x, GroupVar) and isinstance(y, GroupVar):
        indexes = _argsort(array(x.val()))
        return GroupVar([x[i] for i in indexes]), GroupVar([y[i] for i in indexes])
    else:
        try:
            indexes = _argsort(x)
            x: array
            y: array
            return x[indexes], y[indexes]
        except Exception:
            raise TypeError('x and y must be the same type')


def smoothing(x: Union[array, List, GroupVar], y: Union[array, List, GroupVar], smooth_factor) -> Callable:
    """
    Строит сглаженную функцию через данные точки, возвращает её
    :param x: Итерируемый объект с абсциссами точек
    :param y: Итерируемый объект с ординатами точек
    :param smooth_factor:
    :return: Сглаженная функция через заданные точки
    """
    # todo: сделать покопаться в _UnivariateSpline и учитывать каждую точку с весом ошибки
    x, y = sorting(x, y)
    if isinstance(x, GroupVar):
        x = x.val()
    if isinstance(y, GroupVar):
        y = y.val()
    x, y = map(array, [x, y])
    f = _UnivariateSpline(x, y)
    f.set_smoothing_factor(smooth_factor)
    # todo: лучше, конечно, было бы если возвращаемая функция была приведена к sympy.Function и её можно было бы
    #  хранить, как sin это позволило бы передавать ей на вход Var и GroupVar!
    return f


def fmin(f: Callable, x0: Union[Var, SupportsFloat], x: Optional[GroupVar] = None, y: Optional[GroupVar] = None) \
        -> Union[Var, SupportsFloat]:
    """
    Функция для очень аккуратного поиска минимума функции
    :param f: Функция для поиска минимума
    :param x0: Точка рядом с минимумом
    :params x and y: чтобы аккуратнее посчитать ошибку определения минимума
    :return: Абсциссу точки минимума
    """
    # TODO: сделать так, чтоб искало минимум на заднанном промежутке. (Потому что, при данной реализации минимум
    #  функции-колокола будет ниже, чем любая переданная точка. Что не есть хорошо)
    v, _sys.stdout = _sys.stdout, None
    if isinstance(x0, Var):
        x0 = x0.val()
    x_min = _fmin(f, x0)[0]
    if isinstance(y, GroupVar) and isinstance(x, GroupVar):
        x, y = sorting(x, y)
        i_min = sorted(list(x.val()) + [x_min]).index(x_min)
        if i_min == len(x):
            f_min, y_err, err = f(x_min), y[i_min - 1].err(), x[i_min - 1].err()
        else:
            f_min, y_err, err = f(x_min), y[i_min].err(), x[i_min].err()
        x_err_approx = sqrt(2 * y_err / (f(x_min + err) + f(x_min - err) - 2 * f_min)) * err
        _sys.stdout = v
        return Var(x_min, sqrt(x_err_approx ** 2 + err ** 2))
    else:
        _sys.stdout = v
        return x_min


def fmax(f: Callable, x0: Union[Var, SupportsFloat], x: Optional[GroupVar] = None, y: Optional[GroupVar] = None) \
        -> Union[Var, SupportsFloat]:
    """
    Функция для очень аккуратного поиска максимума функции, работает на основе fmin
    :param f: Функция для поиска минимума
    :param x0: Точка рядом с минимумом
    :params x and y: чтобы аккуратнее посчитать ошибку определения минимума
    :return: Абсциссу точки максимума
    """
    return fmin(lambda t: -f(t), x0, x=x, y=y)


def curve_fit(f: Callable, x: GroupVar, y: GroupVar, p0: Optional[Sequence[SupportsFloat]] = None):
    """
    Функция, аппроксимирующая любую прямую к данным точкам
    :param f: Функция от x, должна принимать кроме x ещё другие параметры для аппроксимации
    :param x: Итерируемый объект с координатами точек по оси абсцисс
    :param y: Итерируемый объект с координатами точек по оси ординат
    :param p0: Итерируемый объект с начальными значениями аппроксимируемых параметров
    (Их количество на 1 меньше, чем значений, принимаемых функцией f).
    Указание данного параметра сильно ускорит аппроксимацию функции
    :return:
    """
    initial_p = None if p0 is None else np.array(p0)
    too_small_err = np.any(np.asarray(y.err()) < 1/np.finfo(np.float_).max)
    sigma = None if too_small_err else y.err()
    p_opt, p_cov = _curve_fit(f, xdata=x.val(), ydata=y.val(), p0=initial_p, sigma=sigma)
    return GroupVar(p_opt, np.diag(p_cov))


def sigma(variable: Union[GroupVar, Sequence]):
    """
    Считает отклонение точек массива
    :param variable: Итерируемый объект с точками
    :return: Дисперсию данных точек
    """
    if isinstance(variable, GroupVar):
        variable = variable.val()
    return sqrt(_var(variable))
