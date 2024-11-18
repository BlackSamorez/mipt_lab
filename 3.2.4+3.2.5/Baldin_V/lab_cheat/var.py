from __future__ import annotations

from decimal import Decimal
from functools import total_ordering
from typing import Sequence, SupportsFloat, Dict, List, Union, overload, Callable, Optional, Tuple, Iterable
from warnings import catch_warnings, simplefilter

from numpy import sqrt, array, diag, isnan
from sympy.core.symbol import Symbol, Expr
from sympy.utilities import lambdify

DictSymVar: Dict[Symbol, Var] = {}


@total_ordering
class Var:
    """
    Класс Var один из самых главных классов в библиотеке lab_cheat.
    Он используется, чтобы хранить пару "значение ошибка" любой,
    непосредственно измеряемой переменной ИЛИ функцию, как вычислить
    косвенную переменную из прямых переменных. В этом классе нет
    публичных слотов.
    Для серий однотипных переменных удобнее использовать GroupVar.
    """

    @overload
    def __init__(self, _story: Expr, exp: int = 0):
        """
        Никогда не используйте Var(...) следующим образом.
        Это используется только библиотекой.
        """
        ...

    @overload
    def __init__(self, value: SupportsFloat, error: SupportsFloat, exp: int = 0):
        """
        Создаёт объект класса Var.
        :param value: приближенное значение непосредственно измеряемой величины
        :param error: стандартное отклонение
        :param exp: если exp!=0, тогда величина и ошибка будут изменены
        следующим образом:
            величина -> величина * 10 ** exp
            ошибка -> ошибка * 10 ** exp
        """
        ...

    def __init__(self, *args, exp: int = 0):
        if len(args) == 2:
            self._value: float = float(args[0]) * 10 ** exp
            self._error: float = float(args[1]) * 10 ** exp
            self._story: Symbol = Symbol('s' + str(id(self)))
            DictSymVar.update({self._story: self})
        else:
            self._story: Expr = args[0]

    def val_err(self) -> Tuple[float, float]:
        """
        :return: кортеж, содержащий перменную и значение
        (Этот метод более эффективен, чем вызов val() и err() по отдельности.)
        """
        args = tuple(self._story.free_symbols)
        func = lambdify(args, self._story, modules='numpy')
        base_vars = tuple(DictSymVar[sym] for sym in args)
        values = array(tuple(var._value for var in base_vars), dtype=float)
        diag_err = diag(array(tuple(var._error for var in base_vars)))
        val = func(*values)
        if isnan(val):
            raise TypeError('The argument does not belong to the definition scope')
        # проверяем, что значения функции с обеих сторон существуют
        err = sqrt(sum((estimated_error(func, values, diag_err[i], val)) ** 2 for i in range(len(values))))
        return val, err

    def val(self) -> float:
        """
        :return: значение вашей переменной
        """
        args = tuple(self._story.free_symbols)
        return lambdify(args, self._story, 'numpy')(*(DictSymVar[sym]._value for sym in args))

    def err(self) -> float:
        """
        :return: ошибки ваших переменных
        Ниже объясняется, как библиотека находит его:
            В большинстве случаев мы имеем случайные назависимые ошибки переменных:
            delta(f(x1, x2, ...)) ~= sqrt( (df/dx1 * delta(x1))**2 + (df/dx2 * delta(x2))**2 + ... ),

            Где ошибки x1, например, в этом методе вычисляются следующим образом:

            df/dx1 * delta(x1) = (f(x1+dx1, x2, ...) - f(x1 - dx1, x2, ...)) * BIG_NUMBER / 2
            dx1 = delta(x1) / BIG_NUMBER

            Как вы можете заметить, это похоже на нахождение частной производной.
            Вы можете изменить BIG_NUMBER внутри функции 'set_big_number' в этом модуле. (по стандарту 50)

        """
        return self.val_err()[1]

    def __repr__(self) -> str:
        """
        :return: краткое грубое представление переменной
        """
        return f'~{self.val()}'

    def __str__(self) -> str:
        """
        :return: строка выглядит как-то так "value \\pm error", где значение и ошибка округляются.
        Цифры одинакового поряка, от 40% ошибки не будут отображаться.
        Если ошибка ноль, не отобразятся числа порядка больше, 5% от значения.
        (40% и 5% могут быть изменены в 'set_error_accuracy' и 'value_accuracy' соответственно.)
        """
        return normalize(self)

    def __le__(self, other: Union[SupportsFloat, Var]) -> bool:
        """
        Подобно другим операциям порядка, сравнивает self.values с other.value или числом.
        """
        if isinstance(other, Var):
            return self.val() <= other.val()
        else:
            return self.val() <= float(other)

    def __eq__(self, other: Union[SupportsFloat, Var]) -> bool:
        """
        Подобно другим операциям порядка, сравнивает self.values с other.value или числом.
        """
        if isinstance(other, Var):
            return self.val() == other.val()
        else:
            return self.val() == float(other)

    def _binary_operation(self, other: TypicalArgument, func: Callable) -> Union[Var, GroupVar]:
        if isinstance(other, Var):
            return Var(func(self._story, other._story))
        if isinstance(other, SupportsFloat):
            return Var(func(self._story, float(other)))
        if isinstance(other, GroupVar):
            return GroupVar(tuple(func(self, other[i]) for i in range(len(other))))

    def __add__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: x + y)

    def __radd__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: y + x)

    def __sub__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: x - y)

    def __rsub__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: y - x)

    def __mul__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: x * y)

    def __rmul__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: y * x)

    def __truediv__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: x / y)

    def __rtruediv__(self, other: TypicalArgument) -> Var:
        return self._binary_operation(other, lambda x, y: y / x)

    def __pow__(self, power: TypicalArgument) -> Var:
        return self._binary_operation(power, lambda x, y: x ** y)

    def __pos__(self) -> Var:
        return self

    def __neg__(self) -> Var:
        return Var(-self._story)


class GroupVar:
    """
    Этот класс реализует идею серии подобных измерений. Ведёт себя аналогично массиву numpy.
    Итак, сложение, умножение двух GroupVar это соответствующая операция между Vars внутри GroupVars.
    Единственный слот в этом классе - это 'переменная'. Это список, содержащий Vars.
    (Чтобы читать документацию к классу, необходимо понимать соответствующие методы в классе Var.)
    """

    @overload
    def __init__(self, variables: Sequence[Var], exp=0):
        """
        Создаёт пару класса "Var(значение, ошибка)" и передаёт её в 'self.variables'
        :param variables: что-то, содержащее Vars
        :param exp: если exp!=0, тогда все переменные будут изменены следующим образом:
        переменная -> переменная * 10 ** exp
        """
        ...

    @overload
    def __init__(self, values: Sequence[SupportsFloat], errors: Sequence[SupportsFloat], exp=0):
        """
        Создаёт пару класса "Var(значение, ошибка)" и передаёт её в 'self.variables'
        :param values: что-то, содержащее числа
        :param errors: что-то, содержащее числа
        :param exp: если exp!=0, тогда все переменные будут изменены следующим образом:
        переменная -> переменная * 10 ** exp
        """
        ...

    @overload
    def __init__(self, values: Sequence[SupportsFloat], error: SupportsFloat, exp=0):
        """
        Схоже с предыдущим перегруженным методом __init__, но все ошибки внутри переменных будут теми же.
        Аналогично вызову GroupVar(значение, [ошибка]*len(значение), exp)
        """
        ...

    def __init__(self, *args, exp=0):
        if len(args) == 2:
            values, errors = args[0], {True: args[1], False: [args[1]] * len(args[0])}[hasattr(args[1], '__iter__')]
            if len(values) != len(errors):
                raise TypeError('Arguments must be the same length')
            self.variables: List[Var] = [Var(val, err) * 10 ** exp for val, err in zip(values, errors)]
        elif isinstance(args[0][0], Var):
            self.variables: List[Var] = [var * 10 ** exp for var in args[0]]
        else:
            raise TypeError('Unexpected type of arguments')

    def val_err(self) -> Tuple[Tuple[float, ...], Tuple[float, ...]]:
        """
        :return: Кортеж, состоящий из (кортежа значений) и (кортежа переменных).
        """
        return tuple(zip(*(var.val_err() for var in self)))

    def val(self) -> List[float]:
        """
        :return: список значений
        """
        return [var.val() for var in self.variables]

    def err(self) -> List[float]:
        """
        :return: список ошибок
        """
        return [var.err() for var in self.variables]

    def __getitem__(self, item: Union[int, slice, Iterable[int]]):
        """
        Если тип элемента 'целое число', тогда возвращает self.variables[элемент].
        Если тип элемента 'срез', тогда возвращает GroupVar(self.variables[элемент]).
        Если тип элемента 'список[целые числа]', тогда возвращает GroupVar([self.variables[i] for i in элемент]).

        """
        if isinstance(item, slice):
            return GroupVar(self.variables[item])
        if hasattr(item, '__iter__'):
            return GroupVar([self.variables[i] for i in item])
        return self.variables[item]

    def __iter__(self):
        return self.variables.__iter__()

    def __len__(self) -> int:
        return len(self.variables)

    def __repr__(self):
        return str([var.__repr__() for var in self.variables])

    def __str__(self):
        return str([var.__str__() for var in self.variables])

    def _binary_operation(self, other: TypicalArgument, func: Callable) -> Union[Var, GroupVar]:
        if isinstance(other, GroupVar):
            if len(self) != len(other):
                raise TypeError('Arguments must be the same length')
            return GroupVar(tuple(func(self[i], other[i]) for i in range(len(self))))
        else:
            return GroupVar(tuple(func(var, other) for var in self.variables))

    def __add__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: x + y)

    def __radd__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: y + x)

    def __sub__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: x - y)

    def __rsub__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: y - x)

    def __mul__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: x * y)

    def __rmul__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: y * x)

    def __truediv__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: x / y)

    def __rtruediv__(self, other: TypicalArgument) -> GroupVar:
        return self._binary_operation(other, lambda x, y: y / x)

    def __pow__(self, power: Union[TypicalArgument]) -> GroupVar:
        return self._binary_operation(power, lambda x, y: x ** y)

    def __pos__(self) -> GroupVar:
        return self

    def __neg__(self) -> GroupVar:
        return GroupVar([-var for var in self.variables])


TypicalArgument = Union[SupportsFloat, Var, GroupVar]

error_accuracy: float = 0.4
value_accuracy: float = 0.05


def set_error_accuracy(accuracy: float):
    """Смотреть документацию Var.__str__"""
    global error_accuracy
    error_accuracy = accuracy


def set_value_accuracy(accuracy: float):
    """Смотреть документацию Var.__str__"""
    global value_accuracy
    value_accuracy = accuracy


def suitable_accuracy(val: float, err: float) -> int:
    """Находит необходимое число цифр, которое было показано в документации Var.__str__"""
    if err == 0:
        return Decimal.from_float(val * value_accuracy).adjusted()
    return Decimal.from_float(err * error_accuracy).adjusted()


def normalize(var: Var, accuracy: Optional[int] = None, UTF_ed = False) -> str:
    """То же самое, что str(var), но Вы можете установить число цифр, которое будет показано, в параметре 'accuracy'"""
    val, err = var.val_err()
    if accuracy is None:
        accuracy = suitable_accuracy(val, err)
    if UTF_ed:
        return r'{0} ± {1}'.format(
            *({True: float, False: int}[accuracy < 0](round(num, -accuracy)) for num in (val, err)))
    return r'{0} \pm {1}'.format(
        *({True: float, False: int}[accuracy < 0](round(num, -accuracy)) for num in (val, err)))


BIG_NUMBER = 50


def set_big_number(n: int):
    """Смотреть документацию Var.err"""
    global BIG_NUMBER
    BIG_NUMBER = n


def estimated_error(func: Callable[[...], float], values: array, err_vector: array, val: float):
    err_vector /= BIG_NUMBER
    # ловим предупреждения превращая их в ошибки
    with catch_warnings():
        simplefilter("error")
        try:
            v_plus = func(*(values + err_vector))
        except RuntimeWarning:
            try:
                return (val - func(*(values - err_vector))) * BIG_NUMBER
            except RuntimeWarning:
                raise TypeError('Your errors are too big')
        try:
            v_minus = func(*(values - err_vector))
        except RuntimeWarning:
            return (val - v_plus) * BIG_NUMBER
        return (v_plus - v_minus) / 2 * BIG_NUMBER
