import tkinter as tk
from string import printable as english_symbols
from typing import List, Tuple, Optional

from .var import GroupVar, suitable_accuracy


def rus_tex_formula(formula: str) -> str:
    """
    Перевариает формулу с русскими символами так, чтобы Tex нормально это всё дело записал
    :param formula: Формула
    :return: Формула, с форматированными русскими буквами
    """
    ret, rus_now = '', False
    for char in formula:
        if rus_now is (char in english_symbols):
            ret += {True: '}', False: '\\text{'}[rus_now]
            rus_now = not rus_now
        ret += char
    if rus_now is True: ret += '}'
    return ret


def to_table(exel: str, transpose=False) -> List[List[float]]:
    """
    Поглощает Excel файл в массивчик элементов
    :param exel: Путь к файлу Excel
    :param transpose: Транспонировать ли?
    :return: 2 мерный массив со столбцами и строками из файла Excel
    """
    table = tuple(map(lambda x: x.split('\t'), exel.split('\n')))[:-1]
    if transpose:
        table = list(zip(*table))
    return [[float(table[j][i]) for j in range(len(table)) if table[j][i] != ''] for i in range(len(table[0]))]


class TexTable:
    """
    Класс с табличкой теха, с помощью функций данного класса можно слепить Теховскую табличку
    """

    def __init__(self):
        self._numbers: List[Tuple[str, ...], ...] = []
        self._titles: List[str, ...] = []

    def add(self, group_var: GroupVar, title: str, show_err=False):
        """
        Добавляет столбец в Тех таблицу
        :param group_var: GroupVar с точками
        :param title: Название нового столбца
        :param show_err: Нужно ли показать ошибку прямо в таблице?
        :return: Себя же, для однострочной записи
        """
        values, errors = group_var.val_err()
        accuracy = round(sum(suitable_accuracy(values[i], errors[i]) for i in range(len(group_var))) / len(group_var))
        needed_type = {True: float, False: int}[accuracy < 0]
        self._numbers.append(tuple(map(lambda val: str(needed_type(round(val, -accuracy))), values)))
        self._titles.append(title)
        if show_err is True:
            self._numbers.append(tuple(map(lambda err: str(needed_type(round(err, -accuracy))), errors)))
            self._titles.append('\\Delta ' + title)
        return self

    def show(self, caption: Optional[str] = None, numerate: bool = True, colours=('C0C0C0', 'EFEFEF', 'C0C0C0'),
             color_frequency: int = 2):
        """
        Выводит табличку в окне tkinter
        :param caption: non used
        :param numerate: Нумеровать ли?
        :param colours: Цвета таблички
        :param color_frequency: Частота смены цвета
        :return: ничего
        """
        if numerate is True:
            self._numerating()
        self._show_tk_window(self._begin() + self._write_titles(colours) +
                             self._write_numbers(numerate, colours, color_frequency) + self._end())

    def _numerating(self):
        """
        Нумерует строки
        :return: ничего
        """
        self._titles = [''] + self._titles
        max_num = max(map(len, self._numbers))
        self._numbers = [tuple(str(i) for i in range(1, max_num + 1))] + self._numbers

    def _begin(self):
        return "\\begin{center} \n" + \
               "\\textbf{Таблица @} \\\\ \n" + \
               "\\begin{tabular}{|" + "".join(['c|'] * len(self._titles)) + "}\n"

    def _write_titles(self, colours):
        return "\\hline\n" + \
               "\\rowcolor[HTML]{" + colours[0] + "}\n" + \
               "".join([' $' + rus_tex_formula(title) + '$ &' for title in self._titles])[:-1] + "\\\\ \\hline\n"

    def _write_numbers(self, numerate, colours, color_frequency):
        result = ''
        for string in range(max(map(len, self._numbers))):
            result += ("\\rowcolor[HTML]{" + colours[1] + "}\n" if (string + 1) % color_frequency == 0 else '') + \
                      ("\\cellcolor[HTML]{" + colours[2] + "} " if numerate else '')
            for column in range(len(self._titles)):
                result += _safe_get(self._numbers[column], string, ' ') + ' & '
            result = result[:-2] + '\\\\ \\hline\n'
        return result

    @staticmethod
    def _end():
        return "\\end{tabular}\n" + \
               "\end{center}\n"

    @staticmethod
    def _show_tk_window(text):
        """
        Функция, реализующая комбинацию "ctrl + A"
        :param text: Текст, который надо выделить
        :return: ничего
        """
        root = tk.Tk()
        text_tk = tk.Text(width=100, height=30, wrap=tk.WORD)
        text_tk.insert(float(0), text)
        text_tk.pack(expand=tk.YES, fill=tk.BOTH)

        # ctrl+A does not mean selecting all automatically, that's why i make it by myself

        def select_all(event):
            event.widget.tag_add(tk.SEL, '1.0', tk.END)
            return 'break'

        text_tk.bind('<Control-a>', select_all)
        root.mainloop()


def _safe_get(lst: Tuple, i: int, default):
    """
    Выдаёт объект из списка не вызывая ошибки
    :param lst: Список, из которого нужно получить объект
    :param i: Индекс этого объекта
    :param default: То, что нужно вывести, если элемента не оказалось
    :return: Элемент списка или default
    """
    return lst[i] if i < len(lst) else default
