#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обработки данных лабораторной работы по дифракции света на УЗ-волне.
Построение графиков x_m = f(m) и расчёт погрешности наклона.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from typing import Dict, List, Tuple

# =============================================================================
# ДАННЫЕ ЭКСПЕРИМЕНТА
# =============================================================================
# Формат: частота (Гц) -> список кортежей (порядок m, x в мкм)
DATA: Dict[int, List[Tuple[int, float]]] = {
    1_020_000: [
        (1, 152), (2, 304), (3, 436), (4, 584),
        (5, 708), (6, 844), (7, 976), (8, 1096)
    ],
    1_095_000: [
        (1, 136), (2, 272), (3, 404), (4, 556),
        (5, 704), (6, 844), (7, 996), (8, 1132)
    ],
    1_200_000: [
        (1, 80), (2, 160), (3, 316), (4, 472),
        (5, 636), (6, 788), (7, 952)
    ],
    1_270_000: [
        (1, 160), (2, 320), (3, 488), (4, 660),
        (5, 808), (6, 980), (7, 1136)
    ],
    1_360_000: [
        (1, 176), (2, 352), (3, 536)
    ]
}

# Погрешность измерения координаты x (мкм)
DX_MKM = 20.0

# Фокусное расстояние объектива (см) — для последующих расчётов
F_CM = 30.0

# Длина волны света (красный фильтр, примерное значение, нм)
LAMBDA_NM = 650.0


# =============================================================================
# ФУНКЦИИ ОБРАБОТКИ
# =============================================================================

def weighted_linear_fit(x: np.ndarray, y: np.ndarray, dy: np.ndarray) -> Tuple[float, float, float, float]:
    """
    Взвешенный метод наименьших квадратов для прямой y = k*x + b.
    
    Parameters
    ----------
    x : массив независимой переменной (порядки m)
    y : массив зависимой переменной (координаты x_m)
    dy : массив погрешностей y
    
    Returns
    -------
    k : коэффициент наклона
    dk : погрешность наклона
    b : свободный член
    db : погрешность свободного члена
    """
    w = 1.0 / dy**2
    
    S = np.sum(w)
    Sx = np.sum(w * x)
    Sy = np.sum(w * y)
    Sxx = np.sum(w * x * x)
    Sxy = np.sum(w * x * y)
    
    Delta = S * Sxx - Sx**2
    
    k = (S * Sxy - Sx * Sy) / Delta
    b = (Sxx * Sy - Sx * Sxy) / Delta
    
    # Погрешности параметров
    dk = np.sqrt(S / Delta)
    db = np.sqrt(Sxx / Delta)
    
    return k, dk, b, db


def calculate_ultrasound_params(slope_mkm: float, dslope_mkm: float, 
                                frequency_hz: float, f_cm: float, 
                                lambda_nm: float) -> Dict[str, float]:
    """
    Расчёт длины УЗ-волны и скорости звука по наклону графика.
    
    Формулы:
    Λ = f * λ / (slope), где slope = l_m/m в мкм
    v = Λ * ν
    
    Parameters
    ----------
    slope_mkm : наклон графика x_m(m) в мкм/порядок
    dslope_mkm : погрешность наклона
    frequency_hz : частота УЗ-генератора
    f_cm : фокусное расстояние объектива (см)
    lambda_nm : длина волны света (нм)
    
    Returns
    -------
    Словарь с рассчитанными величинами и их погрешностями
    """
    # Перевод в СИ
    slope_m = slope_mkm * 1e-6
    dslope_m = dslope_mkm * 1e-6
    f_m = f_cm * 1e-2
    lambda_m = lambda_nm * 1e-9
    
    # Длина УЗ-волны: Λ = f * λ / slope
    Lambda_m = f_m * lambda_m / slope_m
    # Относительная погрешность: dΛ/Λ = dslope/slope (пренебрегая погрешностями f и λ)
    dLambda_m = Lambda_m * (dslope_m / slope_m)
    
    # Скорость звука: v = Λ * ν
    v_ms = Lambda_m * frequency_hz
    # Погрешность: dv/v = sqrt((dΛ/Λ)^2 + (dν/ν)^2), пренебрегаем dν
    dv_ms = v_ms * (dLambda_m / Lambda_m)
    
    return {
        'Lambda_m': Lambda_m,
        'dLambda_m': dLambda_m,
        'Lambda_mm': Lambda_m * 1e3,
        'dLambda_mm': dLambda_m * 1e3,
        'v_ms': v_ms,
        'dv_ms': dv_ms
    }


def process_frequency(freq_hz: int, data: List[Tuple[int, float]], 
                     dx_mkm: float = DX_MKM) -> Dict:
    """
    Обработка данных для одной частоты.
    
    Returns
    -------
    Словарь с результатами: наклоном, погрешностями, рассчитанными параметрами
    """
    m_vals = np.array([d[0] for d in data], dtype=float)
    x_vals = np.array([d[1] for d in data], dtype=float)
    dx_vals = np.full_like(x_vals, dx_mkm)
    
    # Взвешенная линейная регрессия
    k, dk, b, db = weighted_linear_fit(m_vals, x_vals, dx_vals)
    
    # Расчёт параметров УЗ-волны
    params = calculate_ultrasound_params(k, dk, freq_hz, F_CM, LAMBDA_NM)
    
    # Коэффициент детерминации R² для оценки качества拟合
    y_pred = k * m_vals + b
    ss_res = np.sum((x_vals - y_pred)**2)
    ss_tot = np.sum((x_vals - np.mean(x_vals))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    
    return {
        'freq_hz': freq_hz,
        'n_points': len(data),
        'slope_mkm': k,
        'dslope_mkm': dk,
        'intercept_mkm': b,
        'dintercept_mkm': db,
        'r_squared': r_squared,
        'm_vals': m_vals,
        'x_vals': x_vals,
        **params
    }


# =============================================================================
# ПОСТРОЕНИЕ ГРАФИКОВ
# =============================================================================

def plot_all_frequencies(results: List[Dict], save_path: str = None):
    """
    Построение всех графиков x_m = f(m) на одном рисунке с подплотами.
    """
    n_freqs = len(results)
    cols = 2
    rows = (n_freqs + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(12, 5*rows), squeeze=False)
    fig.suptitle('Зависимость координаты максимума $x_m$ от порядка $m$', 
                 fontsize=14, fontweight='bold')
    
    colors = plt.cm.tab10(np.linspace(0, 1, n_freqs))
    
    for idx, res in enumerate(results):
        ax = axes[idx // cols][idx % cols]
        
        m = res['m_vals']
        x = res['x_vals']
        freq_mhz = res['freq_hz'] / 1e6
        
        # Данные с погрешностями
        ax.errorbar(m, x, yerr=DX_MKM, fmt='o', color=colors[idx], 
                   ecolor='gray', capsize=3, label='Эксперимент', zorder=2)
        
        # Линия регрессии
        m_fit = np.linspace(min(m)*0.9, max(m)*1.1, 100)
        x_fit = res['slope_mkm'] * m_fit + res['intercept_mkm']
        ax.plot(m_fit, x_fit, '-', color=colors[idx], 
               label=f'$k$={res["slope_mkm"]:.1f}±{res["dslope_mkm"]:.1f} мкм', 
               zorder=1)
        
        ax.set_xlabel('Порядок максимума $m$', fontsize=11)
        ax.set_ylabel('Координата $x_m$, мкм', fontsize=11)
        ax.set_title(f'ν = {freq_mhz:.3f} МГц\n$R^2$ = {res["r_squared"]:.4f}', 
                    fontsize=10, pad=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=9)
        ax.set_axisbelow(True)
    
    # Убрать пустые подплоты
    for idx in range(n_freqs, rows * cols):
        ax = axes[idx // cols][idx % cols]
        ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Графики сохранены в {save_path}")
    
    plt.show()


def plot_summary_table(results: List[Dict]):
    """
    Вывод сводной таблицы результатов в консоль.
    """
    print("\n" + "="*85)
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("="*85)
    print(f"{'Частота, МГц':>14} | {'N':>3} | {'Наклон, мкм':>14} | {'v, м/с':>12} | {'Λ, мм':>10} | {'R²':>6}")
    print("-"*85)
    
    for res in results:
        freq_mhz = res['freq_hz'] / 1e6
        slope_str = f"{res['slope_mkm']:.2f} ± {res['dslope_mkm']:.2f}"
        v_str = f"{res['v_ms']:.0f} ± {res['dv_ms']:.0f}"
        lam_str = f"{res['Lambda_mm']:.4f} ± {res['dLambda_mm']:.4f}"
        r2_str = f"{res['r_squared']:.4f}"
        
        print(f"{freq_mhz:14.3f} | {res['n_points']:3d} | {slope_str:>14} | {v_str:>12} | {lam_str:>10} | {r2_str:>6}")
    
    print("="*85)
    
    # Среднее значение скорости звука
    v_values = [r['v_ms'] for r in results if r['n_points'] >= 4]
    dv_values = [r['dv_ms'] for r in results if r['n_points'] >= 4]
    
    if v_values:
        v_mean = np.mean(v_values)
        # Погрешность среднего (стандартная ошибка)
        v_std = np.std(v_values, ddof=1) / np.sqrt(len(v_values)) if len(v_values) > 1 else np.mean(dv_values)
        print(f"\nСредняя скорость звука (для N≥4): v = {v_mean:.0f} ± {v_std:.0f} м/с")
        print(f"Теоретическое значение (20°C): ~1480 м/с")
        print(f"Отклонение: {abs(v_mean - 1480):.0f} м/с ({abs(v_mean - 1480)/1480*100:.2f}%)")


# =============================================================================
# ОСНОВНАЯ ПРОГРАММА
# =============================================================================

def main():
    print("Обработка данных лабораторной работы: Дифракция света на УЗ-волне")
    print(f"Параметры: f = {F_CM} см, λ = {LAMBDA_NM} нм, Δx = {DX_MKM} мкм\n")
    
    # Обработка всех частот
    results = []
    for freq_hz, data in sorted(DATA.items(), key=lambda x: x[0]):
        res = process_frequency(freq_hz, data)
        results.append(res)
        print(f"✓ Частота {freq_hz/1e6:.3f} МГц: "
              f"k = {res['slope_mkm']:.2f} ± {res['dslope_mkm']:.2f} мкм, "
              f"R² = {res['r_squared']:.4f}")
    
    # Построение графиков
    plot_all_frequencies(results, save_path='diffraction_plots.png')
    
    # Сводная таблица
    plot_summary_table(results)
    
    # Дополнительный график: зависимость v от частоты (проверка постоянства)
    plot_velocity_vs_frequency(results)


def plot_velocity_vs_frequency(results: List[Dict]):
    """
    График зависимости рассчитанной скорости звука от частоты.
    """
    valid = [r for r in results if r['n_points'] >= 4]
    if not valid:
        return
    
    freq_mhz = np.array([r['freq_hz']/1e6 for r in valid])
    v_ms = np.array([r['v_ms'] for r in valid])
    dv_ms = np.array([r['dv_ms'] for r in valid])
    
    plt.figure(figsize=(8, 5))
    plt.errorbar(freq_mhz, v_ms, yerr=dv_ms, fmt='o', capsize=4, 
                label='Экспериментальные значения')
    
    # Теоретическая линия
    plt.axhline(y=1480, color='r', linestyle='--', label='Теория (~1480 м/с при 20°C)')
    
    plt.xlabel('Частота УЗ-генератора, МГц', fontsize=11)
    plt.ylabel('Скорость звука в воде, м/с', fontsize=11)
    plt.title('Зависимость рассчитанной скорости звука от частоты', fontsize=12, pad=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend()
    plt.tight_layout()
    plt.savefig('velocity_vs_frequency.png', dpi=300, bbox_inches='tight')
    print("График v(ν) сохранён в velocity_vs_frequency.png")
    plt.show()


if __name__ == "__main__":
    main()
