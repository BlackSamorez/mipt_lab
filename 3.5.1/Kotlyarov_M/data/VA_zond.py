import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# === 1. Загрузка данных ===
file_path = 'VA_zond.xlsx'
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)

currents = [5.0, 4.0, 3.02, 1.5]  # мА
data_dict = {}
for i, current in enumerate(currents):
    col_u = df.columns[2*i]
    col_i = df.columns[2*i + 1]
    u_data = df[col_u].dropna().values
    i_data = df[col_i].dropna().values
    data_dict[current] = {'U': u_data, 'I': i_data}

print("Данные успешно загружены.")

# === вспомогательные функции ===
def tanh_func(U, I_in, Te):
    return I_in * np.tanh(U / (2 * Te))

def dIdU_tanh(U, I_in, Te):
    # производная tanh: I_in/(2Te) * sech^2(U/(2Te))
    arg = U / (2 * Te) if Te != 0 else 0.0
    return (I_in / (2 * Te)) * (1.0 / np.cosh(arg))**2 if Te != 0 else 0.0

def fit_edge(u, i, n_points=5, side='right'):
    """Линейная аппроксимация n крайних точек.
       Возвращает (k, b, u_sel, i_sel) или (None, None, None, None)."""
    u = np.asarray(u)
    i = np.asarray(i)
    if len(u) < 2:
        return None, None, None, None
    idx_sorted = np.argsort(u)
    if side == 'right':
        idx_sel = idx_sorted[-n_points:]
    else:
        idx_sel = idx_sorted[:n_points]
    u_sel = u[idx_sel]
    i_sel = i[idx_sel]
    if len(u_sel) < 2:
        return None, None, None, None
    order = np.argsort(u_sel)
    u_sel = u_sel[order]
    i_sel = i_sel[order]
    A = np.vstack([u_sel, np.ones_like(u_sel)]).T
    k, b = np.linalg.lstsq(A, i_sel, rcond=None)[0]
    return float(k), float(b), u_sel, i_sel

def safe_fmt(x):
    if x is None:
        return "None"
    elif isinstance(x, float) and np.isnan(x):
        return "None"
    else:
        return f"{x:.6f}"

# === вспомогательные функции ===
def fit_edge_with_errors(u, i, n_points=5, side='right'):
    """Линейная аппроксимация n крайних точек с расчетом погрешностей.
       Возвращает (k, b, se_k, se_b, u_sel, i_sel) или (None, None, None, None, None, None)."""
    u = np.asarray(u)
    i = np.asarray(i)
    if len(u) < 2:
        return None, None, None, None, None, None
    
    idx_sorted = np.argsort(u)
    if side == 'right':
        idx_sel = idx_sorted[-n_points:]
    else:
        idx_sel = idx_sorted[:n_points]
    
    u_sel = u[idx_sel]
    i_sel = i[idx_sel]
    
    if len(u_sel) < 2:
        return None, None, None, None, None, None
    
    order = np.argsort(u_sel)
    u_sel = u_sel[order]
    i_sel = i_sel[order]
    
    # Линейная регрессия
    A = np.vstack([u_sel, np.ones_like(u_sel)]).T
    k, b = np.linalg.lstsq(A, i_sel, rcond=None)[0]
    
    # Расчет погрешностей
    n = len(u_sel)
    if n > 2:
        i_pred = k * u_sel + b
        residuals = i_sel - i_pred
        RSS = np.sum(residuals**2)  # Residual Sum of Squares
        MSE = RSS / (n - 2)  # Mean Square Error
        
        # Стандартные ошибки коэффициентов
        u_mean = np.mean(u_sel)
        Sxx = np.sum((u_sel - u_mean)**2)
        se_k = np.sqrt(MSE / Sxx)
        se_b = np.sqrt(MSE * (1/n + u_mean**2 / Sxx))
    else:
        se_k = None
        se_b = None
    
    return float(k), float(b), se_k, se_b, u_sel, i_sel

def calculate_central_derivative_with_error(u, i, n_points=3):
    """Расчет производной в нуле и ее погрешности методом центральных разностей."""
    if len(u) < n_points:
        return None, None
    
    idx_zero = np.argmin(np.abs(u))
    half_window = n_points // 2
    
    start_idx = max(0, idx_zero - half_window)
    end_idx = min(len(u), idx_zero + half_window + 1)
    
    u_window = u[start_idx:end_idx]
    i_window = i[start_idx:end_idx]
    
    if len(u_window) < 2:
        return None, None
    
    # Линейная регрессия для наклона
    A = np.vstack([u_window, np.ones_like(u_window)]).T
    k, b = np.linalg.lstsq(A, i_window, rcond=None)[0]
    
    # Погрешность наклона
    n = len(u_window)
    if n > 2:
        i_pred = k * u_window + b
        residuals = i_window - i_pred
        RSS = np.sum(residuals**2)
        MSE = RSS / (n - 2)
        
        u_mean = np.mean(u_window)
        Sxx = np.sum((u_window - u_mean)**2)
        se_k = np.sqrt(MSE / Sxx)
    else:
        se_k = None
    
    return float(k), se_k

# === вспомогательные функции ===
def calculate_tanh_derivative_error(I_in, Te, U, se_I_in, se_Te):
    """Расчет погрешности производной функции tanh в точке U."""
    if I_in is None or Te is None or Te == 0:
        return None, None, None
    
    x = U / (2 * Te)
    sech2 = (1.0 / np.cosh(x))**2
    
    # Производная: dI/dU = (I_in / (2 * Te)) * sech^2(U/(2*Te))
    dIdU = (I_in / (2 * Te)) * sech2
    
    # Погрешность производной через частные производные
    if se_I_in is not None and se_Te is not None:
        # Частная производная по I_in
        d_dIdU_dI_in = (1 / (2 * Te)) * sech2
        
        # Частная производная по Te
        d_dIdU_dTe = - (I_in / (2 * Te**2)) * sech2 + (I_in / (2 * Te)) * (-2 * sech2 * np.tanh(x) * (-U/(2*Te**2)))
        d_dIdU_dTe = - (I_in / (2 * Te**2)) * sech2 * (1 - x * np.tanh(x))
        
        se_dIdU = np.sqrt((d_dIdU_dI_in * se_I_in)**2 + (d_dIdU_dTe * se_Te)**2)
    else:
        se_dIdU = None
    
    return dIdU, se_dIdU

def calculate_tanh_intercept_error(I_in, Te, U, se_I_in, se_Te):
    """Расчет погрешности пересечения касательной к tanh с осью ординат."""
    if I_in is None or Te is None or Te == 0:
        return None, None, None
    
    x = U / (2 * Te)
    tanh_x = np.tanh(x)
    sech2 = (1.0 / np.cosh(x))**2
    
    # Значение функции в точке U
    I_U = I_in * tanh_x
    
    # Производная в точке U
    dIdU = (I_in / (2 * Te)) * sech2
    
    # Пересечение с осью ординат: b = I_U - dIdU * U
    b = I_U - dIdU * U
    
    # Погрешность пересечения через частные производные
    if se_I_in is not None and se_Te is not None:
        # Частные производные для I_U
        d_I_U_dI_in = tanh_x
        d_I_U_dTe = I_in * sech2 * (-U/(2*Te**2))
        
        # Частные производные для dIdU (уже вычислены ранее)
        d_dIdU_dI_in = (1 / (2 * Te)) * sech2
        d_dIdU_dTe = - (I_in / (2 * Te**2)) * sech2 * (1 - x * np.tanh(x))
        
        # Частные производные для b
        d_b_dI_in = d_I_U_dI_in - d_dIdU_dI_in * U
        d_b_dTe = d_I_U_dTe - d_dIdU_dTe * U
        
        se_b = np.sqrt((d_b_dI_in * se_I_in)**2 + (d_b_dTe * se_Te)**2)
    else:
        se_b = None
    
    return b, se_b

# === 3. Обработка данных ===
results = {}
n_points_asymptote = 4  # используем только 3-4 крайние точки

for current, data in data_dict.items():
    print(f"\n--- Обработка данных для I_p = {current} мА ---")
    u_raw = np.asarray(data['U'])
    i_raw = np.asarray(data['I'])

    if len(u_raw) == 0:
        print("  Пустые данные, пропускаем.")
        continue

    # --- центрирование по I≈0 ---
    idx_cross = np.argmin(np.abs(i_raw))
    if idx_cross == 0 or idx_cross == len(i_raw) - 1:
        u_cross = float(u_raw[idx_cross])
    else:
        u1, u2 = float(u_raw[idx_cross-1]), float(u_raw[idx_cross+1])
        i1, i2 = float(i_raw[idx_cross-1]), float(i_raw[idx_cross+1])
        if i2 != i1:
            u_cross = float(u1 - i1 * (u2 - u1) / (i2 - i1))
        else:
            u_cross = float(u_raw[idx_cross])

    u_centered = u_raw - u_cross
    i_centered = i_raw.astype(float)

    # --- Метод 1: краевые прямые по конечным приращениям (3-4 крайние точки) ---
    slope_pos, intercept_pos, se_slope_pos, se_intercept_pos, pos_u_sel, pos_i_sel = fit_edge_with_errors(u_centered, i_centered, n_points_asymptote, side='right')
    slope_neg, intercept_neg, se_slope_neg, se_intercept_neg, neg_u_sel, neg_i_sel = fit_edge_with_errors(u_centered, i_centered, n_points_asymptote, side='left')

    # Расчет I_iн по методу конечных приращений
    if (intercept_pos is not None) and (intercept_neg is not None):
        I_iн_finite_upper = intercept_pos  # пересечение правой асимптоты с U=0
        I_iн_finite_lower = intercept_neg  # пересечение левой асимптоты с U=0
        I_iн_finite = 0.5 * (abs(intercept_pos) + abs(intercept_neg))  # среднее абсолютных значений
        
        # Погрешность I_iн_finite (среднее двух независимых измерений)
        if se_intercept_pos is not None and se_intercept_neg is not None:
            se_I_iн_finite = 0.5 * np.sqrt(se_intercept_pos**2 + se_intercept_neg**2)
        else:
            se_I_iн_finite = None
    else:
        I_iн_finite_upper = None
        I_iн_finite_lower = None
        I_iн_finite = None
        se_I_iн_finite = None

    # Наклон в нуле по методу конечных приращений
    dI_dU_finite, se_dI_dU_finite = calculate_central_derivative_with_error(u_centered, i_centered, n_points=5)

    # --- Метод 2: подгонка tanh и касательные в крайних точках ---
    # начальное приближение
    try:
        # Более точное начальное приближение для I_in
        I0_guess = np.max(np.abs(i_centered)) * 0.8 if len(i_centered) else 0.05
        # Начальное приближение для Te основано на наклоне в нуле
        if dI_dU_finite is not None and I0_guess > 0:
            Te_guess = I0_guess / (2 * abs(dI_dU_finite)) if abs(dI_dU_finite) > 1e-10 else 1.0
        else:
            Te_guess = 1.0
    except Exception:
        I0_guess = 0.05
        Te_guess = 1.0
    
    p0 = [I0_guess, Te_guess]

    try:
        # Добавляем ограничения для параметров
        bounds = ([0.001, 0.1], [np.inf, 50.0])  # I_in > 0, Te в разумных пределах
        popt, pcov = curve_fit(tanh_func, u_centered, i_centered, p0=p0, 
                              bounds=bounds, maxfev=20000)
        I_in_fit, Te_fit = float(popt[0]), float(popt[1])
        
        # Погрешности параметров из ковариационной матрицы
        perr = np.sqrt(np.diag(pcov))
        se_I_in_fit = float(perr[0]) if len(perr) > 0 else None
        se_Te_fit = float(perr[1]) if len(perr) > 1 else None
    except Exception as e:
        print(f"  (warning) Подгонка tanh не сошлась для I_p={current}: {e}")
        # запасные значения
        I_in_fit = I_iн_finite if (I_iн_finite is not None) else (np.max(np.abs(i_centered)) if len(i_centered) else 0.05)
        Te_fit = Te_guess
        se_I_in_fit = None
        se_Te_fit = None

    # --- Расчет касательных для tanh в крайних точках с погрешностями ---
    U_min, U_max = float(np.min(u_centered)), float(np.max(u_centered))
    
    # Касательные в крайних точках диапазона данных с погрешностями
    I_at_min = tanh_func(U_min, I_in_fit, Te_fit)
    I_at_max = tanh_func(U_max, I_in_fit, Te_fit)
    
    # Производные в крайних точках с погрешностями
    k_min, se_k_min = calculate_tanh_derivative_error(I_in_fit, Te_fit, U_min, se_I_in_fit, se_Te_fit)
    k_max, se_k_max = calculate_tanh_derivative_error(I_in_fit, Te_fit, U_max, se_I_in_fit, se_Te_fit)
    
    # Пересечения с осью ординат с погрешностями
    b_min, se_b_min = calculate_tanh_intercept_error(I_in_fit, Te_fit, U_min, se_I_in_fit, se_Te_fit)
    b_max, se_b_max = calculate_tanh_intercept_error(I_in_fit, Te_fit, U_max, se_I_in_fit, se_Te_fit)

    # Пересечение касательных с осью ординат (U=0) для метода tanh
    I_iн_tanh_upper = b_max  # пересечение правой касательной с U=0
    I_iн_tanh_lower = b_min  # пересечение левой касательной с U=0
    I_iн_tanh = 0.5 * (abs(b_max) + abs(b_min))  # среднее абсолютных значений
    
    # Погрешность среднего I_iн для метода tanh
    if se_b_min is not None and se_b_max is not None:
        se_I_iн_tanh = 0.5 * np.sqrt(se_b_min**2 + se_b_max**2)
    else:
        se_I_iн_tanh = None

    # Пересечение самих касательных (для графика)
    if abs(k_min - k_max) > 1e-14:
        U_cross_tanh = (b_max - b_min) / (k_min - k_max)
        I_cross_tanh = k_min * U_cross_tanh + b_min
    else:
        U_cross_tanh = 0.0
        I_cross_tanh = 0.5 * (b_min + b_max)

    # Производная в нуле по методу tanh
    dI_dU_at_zero_tanh = (I_in_fit / (2 * Te_fit)) if Te_fit != 0 else None
    
    # Погрешность производной в нуле для метода tanh
    if dI_dU_at_zero_tanh is not None and se_I_in_fit is not None and se_Te_fit is not None:
        # Используем формулу для погрешности частного
        rel_error_I = se_I_in_fit / I_in_fit
        rel_error_Te = se_Te_fit / Te_fit
        se_dI_dU_at_zero_tanh = abs(dI_dU_at_zero_tanh) * np.sqrt(rel_error_I**2 + rel_error_Te**2)
    else:
        se_dI_dU_at_zero_tanh = None

    # --- сохраняем результаты ---
    results[current] = {
        # данные
        'u_cross': u_cross,
        'u_centered': u_centered,  # ДОБАВЛЕНО
        'i_centered': i_centered,  # ДОБАВЛЕНО
        # метод конечных приращений (краевые прямые по 3-4 точкам)
        'slope_pos': slope_pos, 'intercept_pos': intercept_pos, 
        'se_slope_pos': se_slope_pos, 'se_intercept_pos': se_intercept_pos,
        'pos_u_sel': pos_u_sel, 'pos_i_sel': pos_i_sel,
        'slope_neg': slope_neg, 'intercept_neg': intercept_neg,
        'se_slope_neg': se_slope_neg, 'se_intercept_neg': se_intercept_neg,
        'neg_u_sel': neg_u_sel, 'neg_i_sel': neg_i_sel,
        'I_iн_finite_upper': I_iн_finite_upper, 'I_iн_finite_lower': I_iн_finite_lower, 
        'I_iн_finite': I_iн_finite, 'se_I_iн_finite': se_I_iн_finite,
        'dI_dU_finite': dI_dU_finite, 'se_dI_dU_finite': se_dI_dU_finite,
        # tanh fit и касательные в крайних точках с погрешностями
        'I_in_fit': I_in_fit, 'Te_fit': Te_fit,
        'se_I_in_fit': se_I_in_fit, 'se_Te_fit': se_Te_fit,
        'tanh_k_min': k_min, 'tanh_b_min': b_min, 'se_tanh_k_min': se_k_min, 'se_tanh_b_min': se_b_min,
        'tanh_k_max': k_max, 'tanh_b_max': b_max, 'se_tanh_k_max': se_k_max, 'se_tanh_b_max': se_b_max,
        'U_min': U_min, 'U_max': U_max,
        'I_iн_tanh_upper': I_iн_tanh_upper, 'I_iн_tanh_lower': I_iн_tanh_lower, 
        'I_iн_tanh': I_iн_tanh, 'se_I_iн_tanh': se_I_iн_tanh,
        'U_cross_tanh': U_cross_tanh, 'I_cross_tanh': I_cross_tanh,
        'dI_dU_at_zero_tanh': dI_dU_at_zero_tanh, 'se_dI_dU_at_zero_tanh': se_dI_dU_at_zero_tanh
    }

    # печать результатов - ПОЛНЫЕ ДАННЫЕ ПО ОБОИМ МЕТОДАМ
    print("Метод конечных приращений (3-4 крайние точки):")
    print(f"  I_iн (верхняя асимптота): {safe_fmt(I_iн_finite_upper)} ± {safe_fmt(se_intercept_pos)} мА")
    print(f"  I_iн (нижняя асимптота): {safe_fmt(I_iн_finite_lower)} ± {safe_fmt(se_intercept_neg)} мА") 
    print(f"  I_iн (среднее): {safe_fmt(I_iн_finite)} ± {safe_fmt(se_I_iн_finite)} мА")
    print(f"  Наклон правой асимптоты: {safe_fmt(slope_pos)} ± {safe_fmt(se_slope_pos)} мА/В")
    print(f"  Наклон левой асимптоты: {safe_fmt(slope_neg)} ± {safe_fmt(se_slope_neg)} мА/В")
    print(f"  dI/dU в нуле: {safe_fmt(dI_dU_finite)} ± {safe_fmt(se_dI_dU_finite)} мА/В")
    
    print("Метод tanh (касательные в крайних точках):")
    print(f"  I_iн (верхняя касательная): {safe_fmt(I_iн_tanh_upper)} ± {safe_fmt(se_b_max)} мА")
    print(f"  I_iн (нижняя касательная): {safe_fmt(I_iн_tanh_lower)} ± {safe_fmt(se_b_min)} мА")
    print(f"  I_iн (среднее): {safe_fmt(I_iн_tanh)} ± {safe_fmt(se_I_iн_tanh)} мА")
    print(f"  Наклон правой касательной: {safe_fmt(k_max)} ± {safe_fmt(se_k_max)} мА/В")
    print(f"  Наклон левой касательной: {safe_fmt(k_min)} ± {safe_fmt(se_k_min)} мА/В")
    print(f"  I_in (параметр подгонки): {safe_fmt(I_in_fit)} ± {safe_fmt(se_I_in_fit)} мА")
    print(f"  Te (из fit): {safe_fmt(Te_fit)} ± {safe_fmt(se_Te_fit)} эВ")
    print(f"  dI/dU в нуле (из fit): {safe_fmt(dI_dU_at_zero_tanh)} ± {safe_fmt(se_dI_dU_at_zero_tanh)} мА/В")
    
    # Расчет температуры по методу конечных приращений (по формуле 5.26)
    if I_iн_finite is not None and dI_dU_finite is not None and dI_dU_finite != 0:
        Te_finite = I_iн_finite / (2 * abs(dI_dU_finite))
        
        # Погрешность Te_finite (формула для частного)
        if se_I_iн_finite is not None and se_dI_dU_finite is not None:
            rel_error_I = se_I_iн_finite / I_iн_finite
            rel_error_dI_dU = se_dI_dU_finite / abs(dI_dU_finite)
            se_Te_finite = Te_finite * np.sqrt(rel_error_I**2 + rel_error_dI_dU**2)
        else:
            se_Te_finite = None
            
        print(f"  Te (по методу конечных приращений): {safe_fmt(Te_finite)} ± {safe_fmt(se_Te_finite)} эВ")

        # === Объединение результатов по двум методам ===
    combined_results = {}

    # Объединение для I_iн
    I_iн_values = []
    I_iн_errors = []

    if I_iн_finite is not None and se_I_iн_finite is not None:
        I_iн_values.append(I_iн_finite)
        I_iн_errors.append(se_I_iн_finite)

    if I_iн_tanh is not None and se_I_iн_tanh is not None:
        I_iн_values.append(I_iн_tanh)
        I_iн_errors.append(se_I_iн_tanh)

    if len(I_iн_values) > 0:
        if len(I_iн_values) == 2:
            # Средневзвешенное по двум методам
            weights = [1/err**2 for err in I_iн_errors]
            I_iн_combined = np.average(I_iн_values, weights=weights)
            # Погрешность средневзвешенного
            se_I_iн_combined = 1 / np.sqrt(sum(weights))
        else:
            # Только один метод
            I_iн_combined = I_iн_values[0]
            se_I_iн_combined = I_iн_errors[0]

        combined_results['I_iн'] = I_iн_combined
        combined_results['se_I_iн'] = se_I_iн_combined

    # Объединение для температуры электронов
    Te_values = []
    Te_errors = []

    # Температура из метода конечных приращений
    if I_iн_finite is not None and dI_dU_finite is not None and dI_dU_finite != 0:
        Te_finite = I_iн_finite / (2 * abs(dI_dU_finite))
        if se_I_iн_finite is not None and se_dI_dU_finite is not None:
            rel_error_I = se_I_iн_finite / I_iн_finite
            rel_error_dI_dU = se_dI_dU_finite / abs(dI_dU_finite)
            se_Te_finite = Te_finite * np.sqrt(rel_error_I**2 + rel_error_dI_dU**2)
            Te_values.append(Te_finite)
            Te_errors.append(se_Te_finite)

    # Температура из метода tanh
    if Te_fit is not None and se_Te_fit is not None:
        Te_values.append(Te_fit)
        Te_errors.append(se_Te_fit)

    if len(Te_values) > 0:
        if len(Te_values) == 2:
            weights = [1/err**2 for err in Te_errors]
            Te_combined = np.average(Te_values, weights=weights)
            se_Te_combined = 1 / np.sqrt(sum(weights))
        else:
            Te_combined = Te_values[0]
            se_Te_combined = Te_errors[0]

        combined_results['Te'] = Te_combined
        combined_results['se_Te'] = se_Te_combined

    # Объединение для производной в нуле
    dIdU_values = []
    dIdU_errors = []

    if dI_dU_finite is not None and se_dI_dU_finite is not None:
        dIdU_values.append(dI_dU_finite)
        dIdU_errors.append(se_dI_dU_finite)

    if dI_dU_at_zero_tanh is not None and se_dI_dU_at_zero_tanh is not None:
        dIdU_values.append(dI_dU_at_zero_tanh)
        dIdU_errors.append(se_dI_dU_at_zero_tanh)

    if len(dIdU_values) > 0:
        if len(dIdU_values) == 2:
            weights = [1/err**2 for err in dIdU_errors]
            dIdU_combined = np.average(dIdU_values, weights=weights)
            se_dIdU_combined = 1 / np.sqrt(sum(weights))
        else:
            dIdU_combined = dIdU_values[0]
            se_dIdU_combined = dIdU_errors[0]

        combined_results['dIdU'] = dIdU_combined
        combined_results['se_dIdU'] = se_dIdU_combined

    # Сохраняем объединенные результаты
    results[current]['combined'] = combined_results

    # Печать объединенных результатов
    print("\nОБЪЕДИНЕННЫЕ РЕЗУЛЬТАТЫ (по двум методам):")
    if 'I_iн' in combined_results:
        print(f"  I_iн: {safe_fmt(combined_results['I_iн'])} ± {safe_fmt(combined_results['se_I_iн'])} мА")
    if 'Te' in combined_results:
        print(f"  Te: {safe_fmt(combined_results['Te'])} ± {safe_fmt(combined_results['se_Te'])} эВ")
    if 'dIdU' in combined_results:
        print(f"  dI/dU: {safe_fmt(combined_results['dIdU'])} ± {safe_fmt(combined_results['se_dIdU'])} мА/В")

# === 4. Построение графика ===

plt.figure(figsize=(14, 8))
colors = ['blue', 'orange', 'green', 'red']

for idx, (current, data) in enumerate(data_dict.items()):
    if current not in results:
        continue
    res = results[current]
    u_centered = res['u_centered']
    i_centered = res['i_centered']
    color = colors[idx % len(colors)]

    # точки
    plt.plot(u_centered, i_centered, 'o', color=color, label=f'I_p={current} мА (данные)')

    # tanh (используем параметры fit I_in_fit, Te_fit)
    I_in_fit = res['I_in_fit']; Te_fit = res['Te_fit']
    u_smooth = np.linspace(u_centered.min(), u_centered.max(), 500)
    plt.plot(u_smooth, tanh_func(u_smooth, I_in_fit, Te_fit), '-', color=color, lw=2, label=f'I_p={current} мА (tanh аппрокс.)')

    # касательные по tanh (на концах), рисуем от края к нулю (не уводя слишком далеко)
    kL = res['tanh_k_min']; bL = res['tanh_b_min']
    kR = res['tanh_k_max']; bR = res['tanh_b_max']
    U_min = res['U_min']; U_max = res['U_max']
    span = U_max - U_min if U_max != U_min else 1.0
    u_tan_left = np.linspace(U_min, min(U_min + 0.6*span, 0.0), 200)
    u_tan_right = np.linspace(max(U_max - 0.6*span, 0.0), U_max, 200)
    plt.plot(u_tan_left, kL*u_tan_left + bL, '--', color=color, lw=1.6, label=f'I_p={current} мА (касательные tanh)')
    plt.plot(u_tan_right, kL*u_tan_right + bR, '--', color=color, lw=1.6)
    # точка пересечения касательных (I_iн по tanh)
    Uc = res['U_cross_tanh']; Ic = res['I_iн_tanh']
    plt.scatter(Uc, Ic, s=60, color=color, edgecolor='k', zorder=10, label=f'I_iн(tanh)={safe_fmt(Ic)} мА')

    # краевые асимптоты по конечным приращениям (продлить до 0)
    k_pos = res['slope_pos']; b_pos = res['intercept_pos']
    k_neg = res['slope_neg']; b_neg = res['intercept_neg']
    if (k_pos is not None) and (b_pos is not None):
        u_line_pos = np.linspace(0.0, U_max, 200)
        plt.plot(u_line_pos, k_pos*u_line_pos + b_pos, '-.', color=color, lw=1.2, label=f'I_p={current} мА (асимпт. конеч. приращ.)')
        # показать точки, по которым считали правую аппроксимацию
        pos_u = res.get('pos_u_sel'); pos_i = res.get('pos_i_sel')
        if pos_u is not None:
            plt.plot(pos_u, pos_i, 'x', color=color, alpha=0.8)
    if (k_neg is not None) and (b_neg is not None):
        u_line_neg = np.linspace(U_min, 0.0, 200)
        plt.plot(u_line_neg, k_neg*u_line_neg + b_neg, '-.', color=color, lw=1.2)
        neg_u = res.get('neg_u_sel'); neg_i = res.get('neg_i_sel')
        if neg_u is not None:
            plt.plot(neg_u, neg_i, 'x', color=color, alpha=0.8)

# оформление
plt.xlabel('U, В')
plt.ylabel('I, мА')
plt.title('ВАХ двойного зонда в плазме при разных токах разряда')
plt.grid(True)

# лимиты чтобы точка пересечения не выпала (расширяем немного диапазон)
all_u = np.concatenate([res['u_centered'] for res in results.values()])
all_i = np.concatenate([res['i_centered'] for res in results.values()])
xpad = 0.1 * (all_u.max() - all_u.min()) if (all_u.max() - all_u.min()) != 0 else 1.0
ypad = 0.2 * (all_i.max() - all_i.min()) if (all_i.max() - all_i.min()) != 0 else 1.0
plt.xlim(all_u.min() - xpad, all_u.max() + xpad)
plt.ylim(all_i.min() - ypad, all_i.max() + ypad)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
plt.savefig('VA_zond.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nОбработка завершена. График сохранен как VA_zond.png.")

