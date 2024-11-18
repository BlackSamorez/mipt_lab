from .var import Var, GroupVar
import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from numpy import isnan, nan, array
from copy import deepcopy
import matplotlib.pyplot as plt
from sys import argv


def read_data(file_path=''):
    """
    Отвечает за открытие окошка с выбором файла и импортом его в программу.
    :param file_path: Путь к файлу с данными лабы, который вы выбрали для анализа, если не передавать этот параметр,
    программа выведет вам выбранный путь.
    :return: DataFrame с данными из файла, если файл не выбран, возвращает None
    """
    if file_path == '':
        file_path = askopenfilename(title="Выберите файл")
        print("Путь к вашему файлу:", file_path, "Чтобы скрыть это сообщение и не выбирать файл при каждом "
                                                 "запуске программы, пожалуйста скопируйте "
                                                 "данный путь в аргумент функции read_data"
                                                 "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    file_type = file_path.split(".")[-1]
    if file_path != '':
        if file_type in ["xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt"]:
            out_data = pd.read_excel(file_path, header=None)
        elif file_type == "csv":
            out_data = pd.read_csv(file_path)
        else:
            showerror("Ошибка формата данных", "Неподдерживаемый формат данных")
            out_data = read_data()
        return out_data
    print("Файл не выбран")
    return None


def shredder(dataf: pd.DataFrame, show_result=False):
    """
    Функция, которая отвечает за нарезку листа на маленькие таблички. Сама ищет таблицы в DataFrame, дробит по таблицам
    максимальных размеров. Для корректного ввода данных необходимо, чтобы все значения в таблицах были числового
    формата, а названия столбцов - текстового.
    :param dataf: DataFrame, с данными вашей лабы, который нужно разделить на таблички
    (Обычно используется результат работы функции read_data).
    :param show_result: Нужно ли вывести, на какие таблички был поделен документ.
    :return: Возвращает dict с константами, ключи - названия констант, значения - объекты класса Var,
    т. е. числа + погрешности.
    """
    if type(dataf) != pd.DataFrame:
        raise TypeError("Функция shredder_upd получила на вход вместо pd.DataFrame", type(dataf))
    constants = {}
    tables = []
    for m in range(dataf.shape[0]):
        for n in range(dataf.shape[1]):
            obj = dataf.iloc[m, n]
            logic = type(obj) == str
            if not logic:
                logic = not isnan(dataf.iloc[m, n])
            if logic:
                cord_n, t = _table_check([m, n], dataf)
                table = dataf.iloc[m:cord_n[0] + 1, n:cord_n[1] + 1]
                if t:
                    for i in range(table.shape[0]):
                        constants[table.iloc[i, 0]] = Var(table.iloc[i, 1], table.iloc[i, 2])
                else:
                    name = []
                    for i in table.iloc[0]:
                        name.append(i)
                    table.columns = name
                    tables.append(deepcopy(table.iloc[1:]))
                dataf = _table_del([m, n], cord_n, dataf)
    if show_result:
        if len(constants.keys()) != 0:
            print(constants)
        for i in tables:
            show_df(i)
    return constants, tables


def get_into_groupvar_col_to_col(data_frame: pd.DataFrame):
    """
    Превращает табличку с погрешностями в формате столбец величины - столбец погрешности в словарь с GroupVar
    :param data_frame: Табличка в правильном виде (Получается из shredder)
    :return: Словарь, где ключи - названия столбцов с данными, а значения - GroupVar с данными
    """
    table = {}
    if len(data_frame.columns) == 0:
        raise TypeError("Столбцы не обнаружены, нужен хотя бы один")
    if len(data_frame.columns) % 2 == 1:
        raise TypeError("Похоже, один из столбцов без напарника с погрешностью, т. к. количество столбцов нечётно")
    for index in range(0, len(data_frame.columns), 2):
        table[data_frame.columns[index]] = GroupVar(data_frame[data_frame.columns[index]],
                                                    data_frame[data_frame.columns[index + 1]])
    return table


def get_into_groupvar_col_named(data_frame: pd.DataFrame):
    """
    Превращает табличку с погрешностями в формате столбец величины и если название следующего начинается с delta,
    то с погрешностью в словарик из GroupVar
    :param data_frame: Табличка в правильном виде (Получается из shredder)
    :return: Словарь, где ключи - названия столбцов с данными, а значения - GroupVar с данными
    """
    # TODO: Сделать так, чтобы столбцы с delta могли иметь одинаковые названия
    if len(data_frame.columns) == 0:
        raise TypeError("Столбцы не обнаружены, нужен хотя бы один")
    table = {}
    for index in range(len(data_frame.columns)):
        if not ("delta" in data_frame.columns[index]):
            if index + 1 != len(data_frame.columns):
                if "delta" in data_frame.columns[index + 1]:
                    table[data_frame.columns[index]] = GroupVar(data_frame[data_frame.columns[index]],
                                                                data_frame[data_frame.columns[index + 1]])
                else:
                    table[data_frame.columns[index]] = GroupVar(data_frame[data_frame.columns[index]], 0)
            else:
                table[data_frame.columns[index]] = GroupVar(data_frame[data_frame.columns[index]], 0)
    return table


def get_into_groupvar_col_last_err(data_frame: pd.DataFrame):
    """
    Принимает DataFrame в формате столбцов, последнее значение в каждом из которых - погрешность.
    :param data_frame: DataFrame в указанном формате.
    :return: Словарь, ключи в котором - названия столбцов, а их значения - GroupVar.
    """
    if len(data_frame.columns) == 0:
        raise TypeError("Столбцы не обнаружены, нужен хотя бы один")
    table = {}
    for index in range(len(data_frame.columns)):
        table[data_frame.columns[index]] = GroupVar(data_frame[data_frame.columns[index]].iloc[0:-1],
                                                    data_frame[data_frame.columns[index]].iloc[-1])
    return table


def quick_use_form(dictionary: dict, name_dct=None, index=None):
    """
    Преобразует словарь с данными для более быстрого использования в коде.
    Может выводить строки для явной задачи переменных.
    :param name_dct: Название данного словаря в основной программе.
    Если передать этот параметр будет конструироваться строка для явной инициализации.
    :param index: Индекс переданного словаря в списке, если он в таковом содержится.
    Example: Словарь, который нужно сделать удобнее, лежит в массиве arr, с индексом i,
    тогда name_dct = 'arr', index = i
    :param dictionary: словарь с ключами вида "<название величины>, <её размерность>"
    :return: Словарь, дополненный упрощёнными ключами
    """
    # Проверка данных на корректность ввода
    if type(dictionary) != dict:
        raise TypeError("Функция quick_use_form в качестве 1ого аргумента вместо dict получила", type(dictionary))
    if name_dct is not None and type(name_dct) != str:
        raise TypeError("Функция quick_use_form в качестве 2ого аргумента вместо str получила", type(name_dct))
    if index is not None and type(index) != int:
        raise TypeError("Функция quick_use_form в качестве 3ого аргумента вместо int получила", type(index))
    if len(dictionary.keys()) == 0:
        return dictionary

    # Добавление в словарь ключей с отброшенной погрешностью
    keys_arr = list(dictionary.keys())
    list_for_copy = []
    for key in keys_arr:
        if key.count(',') != 0:
            key_up = key.split(',')[0]
            list_for_copy.append(key_up)
            dictionary[key_up] = dictionary[key]
        else:
            list_for_copy.append(key)

    # Построение строки для явной инициализации переменных
    if name_dct is not None:
        print(', '.join(list_for_copy), '= ', end='')
        if index is not None:
            for i in range(len(list_for_copy)):
                list_for_copy[i] = name_dct + '[' + str(index) + ']' + '[\'' + list_for_copy[i] + '\']'
        else:
            for i in range(len(list_for_copy)):
                list_for_copy[i] = name_dct + '[\'' + list_for_copy[i] + '\']'
        print(', '.join(list_for_copy))
    return dictionary


def to_latex(formula):
    pass


def _table_check(cord_v, data: pd.DataFrame):
    """
    Внутренняя функция, отвечающая за определение размеров таблицы по её верхнему левому углу. Для неё очень важно,
    чтобы названия столбцов были str, а значения непустыми ячейками с числами.
    :param cord_v: Координаты верхнего левого угла рассматриваемой таблички.
    :param data: DataFrame, из которого нужно выделить таблицу.
    """
    cord_n = deepcopy(cord_v)
    if type(data.iloc[cord_v[0] + 1, cord_v[1]]) == str or isnan(data.iloc[cord_v[0] + 1, cord_v[1]]):
        try:
            e1 = data.iloc[cord_v[0], cord_v[1] + 1]
            e2 = data.iloc[cord_v[0], cord_v[1] + 2]
        except IndexError:
            raise TypeError("При рассмотрении таблицы с верхним левым углом в", cord_v, "произошла ошибка.",
                            "Программа рассматривает её как набор констант, но у неё не хватает столбцов,"
                            "должно быть 3: с названием <str>, со значением <int, float> и с погрешностью <int, float>")
        if type(e1) == str or isnan(e1):
            raise TypeError("При рассмотрении таблицы с верхним левым углом в", cord_v, "произошла ошибка.",
                            "Программа рассматривает её как набор констант, но во 2ом её столбце должно быть",
                            "значение константы, т. е. int или float, а не", e1)
        if type(e2) == str or isnan(e2):
            raise TypeError("При рассмотрении таблицы с верхним левым углом в", cord_v, "произошла ошибка.",
                            "Программа рассматривает её как набор констант, но в 3ом её столбце должно быть",
                            "значение погрешности, т. е. int или float, а не", e2)

        # Проверяем, подходит ли под строку констант следующая строка
        not_last_str = not data.shape[0] - 1 == cord_n[0]
        if not_last_str:
            val = data.iloc[cord_n[0] + 1, cord_n[1] + 1]
            err = data.iloc[cord_n[0] + 1, cord_n[1] + 2]
            name_correct = type(data.iloc[cord_n[0] + 1, cord_n[1]]) == str
            val_correct = type(val) != str and not isnan(val)
            err_correct = type(err) != str and not isnan(err)
            while name_correct and val_correct and err_correct and not_last_str:
                cord_n[0] += 1
                not_last_str = not data.shape[0] - 1 == cord_n[0]
                if not_last_str:
                    val = data.iloc[cord_n[0] + 1, cord_n[1] + 1]
                    err = data.iloc[cord_n[0] + 1, cord_n[1] + 2]
                    name_correct = type(data.iloc[cord_n[0] + 1, cord_n[1]]) == str
                    val_correct = type(val) != str and not isnan(val)
                    err_correct = type(err) != str and not isnan(err)

        cord_n[1] += 2
        return cord_n, True
    else:
        not_last_str = not data.shape[0] - 1 == cord_n[0]
        value_type = type(data.iloc[cord_n[0] + 1, cord_n[1]])
        while not_last_str and value_type in [int, float] and not isnan(data.iloc[cord_n[0] + 1, cord_n[1]]):
            cord_n[0] += 1
            if data.shape[0] - 1 == cord_n[0]:
                break
            value_type = type(data.iloc[cord_n[0] + 1, cord_n[1]])

        val = data.iloc[cord_n[0], cord_n[1] + 1]
        not_last_col = not data.shape[1] - 1 == cord_n[1]
        val_correct = type(val) in [int, float] and not isnan(val)
        not_diff_sized = True
        if data.shape[0] - 1 != cord_n[0]:
            next_num = data.iloc[cord_n[0] + 1, cord_n[1] + 1]
            not_diff_sized = type(next_num) not in [int, float] or isnan(next_num)
        if not_last_col:
            while not_last_col and val_correct and not_diff_sized:
                cord_n[1] += 1
                if data.shape[1] - 1 == cord_n[1]:
                    break
                val = data.iloc[cord_n[0], cord_n[1] + 1]
                val_correct = type(val) in [int, float] and not isnan(val)
                if data.shape[0] - 1 != cord_n[0]:
                    next_num = data.iloc[cord_n[0] + 1, cord_n[1] + 1]
                    not_diff_sized = type(next_num) not in [int, float] or isnan(next_num)
        return cord_n, False


def _table_del(cord_v, cord_n, data):
    """
    Внутренняя функция, отвечающая за удаление области из DataFrame
    :param cord_v: Координаты верхнего левого угла удаляемой области
    :param cord_n: Координаты нижнего правого угла удаляемой области
    :param data: DataFrame, из которого нужно удалить область
    :return: DataFrame с областью заменённой на np.nan (Удалённой)
    """
    data.iloc[cord_v[0]:cord_n[0] + 1, cord_v[1]:cord_n[1] + 1] = nan
    return data


def show_df(df):
    """
    Отвечает за красивый вывод таблиц в браузер, используется для отладки работы программы.
    :param df: DataFrame, который нужно вывести
    """
    col_width = 2.0
    row_height = 0.625
    font_size = 14
    header_color = '#757575'
    row_colors = ['#f1f1f2', 'w']
    edge_color = 'w'
    bbox = [0, 0, 1, 1]
    header_columns = 0

    size = (array(df.shape[::-1]) + array([0, 1])) * array([col_width, row_height])
    fig, ax = plt.subplots(figsize=size)
    ax.axis('off')

    mpl_table = ax.table(cellText=df.values, bbox=bbox, colLabels=df.columns)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)
    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    plt.show()
