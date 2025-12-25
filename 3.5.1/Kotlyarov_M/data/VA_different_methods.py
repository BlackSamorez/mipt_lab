import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline, CubicSpline
import warnings
warnings.filterwarnings('ignore')

# Загрузка данных
file_path = 'VA_I_discharge.xlsx'
df = pd.read_excel(file_path, header=0)

# Извлечение и очистка данных
try:
    U_up_raw = df['повышение I_р']
    I_up_mA_raw = df['Unnamed: 1']
    U_down_raw = df['понижение I_р'] 
    I_down_mA_raw = df['Unnamed: 3']

    U_up = pd.to_numeric(U_up_raw, errors='coerce').dropna().values
    I_up_mA = pd.to_numeric(I_up_mA_raw, errors='coerce').dropna().values
    U_down = pd.to_numeric(U_down_raw, errors='coerce').dropna().values
    I_down_mA = pd.to_numeric(I_down_mA_raw, errors='coerce').dropna().values

    min_len_up = min(len(U_up), len(I_up_mA))
    U_up = U_up[:min_len_up]
    I_up_mA = I_up_mA[:min_len_up]

    min_len_down = min(len(U_down), len(I_down_mA))
    U_down = U_down[:min_len_down]
    I_down_mA = I_down_mA[:min_len_down]

except KeyError as e:
    print(f"Ошибка: столбец {e} не найден.")
    exit(1)

print("Данные загружены:")
print(f"Повышение тока: {len(U_up)} точек")
print(f"Понижение тока: {len(U_down)} точек")

# --- РАЗЛИЧНЫЕ МЕТОДЫ АППРОКСИМАЦИИ ---

def polynomial_degree3(U, I):
    """Полином 3-й степени"""
    coeffs = np.polyfit(U, I, 3)
    return np.poly1d(coeffs)

def polynomial_degree4(U, I):
    """Полином 4-й степени"""
    coeffs = np.polyfit(U, I, 4)
    return np.poly1d(coeffs)

def polynomial_degree5(U, I):
    """Полином 5-й степени"""
    coeffs = np.polyfit(U, I, 5)
    return np.poly1d(coeffs)

def cubic_spline_no_smooth(U, I):
    """Кубический сплайн без сглаживания"""
    return CubicSpline(U, I)

def univariate_spline_medium(U, I):
    """UnivariateSpline со средним сглаживанием"""
    return UnivariateSpline(U, I, s=len(U)*2)

def univariate_spline_low(U, I):
    """UnivariateSpline с малым сглаживанием"""
    return UnivariateSpline(U, I, s=len(U)*0.5)

def univariate_spline_very_low(U, I):
    """UnivariateSpline с очень малым сглаживанием"""
    return UnivariateSpline(U, I, s=len(U)*0.1)

# --- РАСЧЕТ СОПРОТИВЛЕНИЯ ДЛЯ КАЖДОГО МЕТОДА ---
def calculate_resistance_for_method(method_func, U, I, method_name, U_min=240, U_max=320):
    """Расчет сопротивления для конкретного метода аппроксимации"""
    
    # Сортировка по напряжению
    sorted_idx = np.argsort(U)
    U_sorted = U[sorted_idx]
    I_sorted = I[sorted_idx]
    
    try:
        # Создаем аппроксимирующую функцию
        approx_func = method_func(U_sorted, I_sorted)
        
        # Для графика: вся кривая
        U_full = np.linspace(U_sorted.min(), U_sorted.max(), 1000)
        I_full = approx_func(U_full)
        
        # Для расчета: только диапазон 240-320 В
        U_calc = np.linspace(U_min, U_max, 500)
        I_calc = approx_func(U_calc)
        
        # Производная dI/dU
        if hasattr(approx_func, 'derivative'):
            dI_dU = approx_func.derivative()(U_calc)
        else:
            # Для полиномов
            dI_dU = np.polyder(approx_func)(U_calc)
        
        # Дифференциальное сопротивление R_диф = dU/dI (в кОм)
        R_diff = np.full_like(dI_dU, np.nan)
        valid_mask = (np.abs(dI_dU) > 1e-6)
        R_diff[valid_mask] = 1.0 / dI_dU[valid_mask]
        
        # Берем модуль и фильтруем физические значения
        R_diff_abs = np.abs(R_diff)
        physical_mask = (R_diff_abs > 1) & (R_diff_abs < 200) & valid_mask
        
        if np.any(physical_mask):
            max_R = np.max(R_diff_abs[physical_mask])
            max_R_idx = np.argmax(R_diff_abs[physical_mask])
            max_R_U = U_calc[physical_mask][max_R_idx]
            
            return max_R, U_full, I_full, True, max_R_U
        else:
            return None, U_full, I_full, False, None
            
    except Exception as e:
        print(f"Ошибка в методе {method_name}: {e}")
        return None, None, None, False, None

# --- МЕТОД КОНЕЧНЫХ РАЗНОСТЕЙ ---
def calculate_finite_differences(U, I, U_min=240, U_max=320):
    """Метод конечных разностей"""
    
    sorted_idx = np.argsort(U)
    U_sorted = U[sorted_idx]
    I_sorted = I[sorted_idx]
    
    range_mask = (U_sorted >= U_min) & (U_sorted <= U_max)
    U_filtered = U_sorted[range_mask]
    I_filtered = I_sorted[range_mask]
    
    if len(U_filtered) < 2:
        return None, None
    
    dU = np.diff(U_filtered)
    dI = np.diff(I_filtered)
    
    mask = (np.abs(dI) > 0.05) & (np.abs(dU) > 0.5)
    dU_filtered = dU[mask]
    dI_filtered = dI[mask]
    
    if len(dU_filtered) == 0:
        return None, None
    
    R_diff = np.abs(dU_filtered / dI_filtered)
    U_mid = (U_filtered[:-1][mask] + U_filtered[1:][mask]) / 2
    
    if len(R_diff) > 0:
        max_R = np.max(R_diff)
        max_R_idx = np.argmax(R_diff)
        max_R_U = U_mid[max_R_idx]
        
        return max_R, max_R_U
    return None, None

# --- СПИСОК МЕТОДОВ ДЛЯ СРАВНЕНИЯ ---
methods = [
    ("Полином 3-й степени", polynomial_degree3),
    ("Полином 4-й степени", polynomial_degree4),
    ("Полином 5-й степени", polynomial_degree5),
    ("Кубический сплайн", cubic_spline_no_smooth),
    ("UnivariateSpline (s=2n)", univariate_spline_medium),
    ("UnivariateSpline (s=0.5n)", univariate_spline_low),
    ("UnivariateSpline (s=0.1n)", univariate_spline_very_low)
]

# --- ПОСТРОЕНИЕ ГРАФИКОВ ДЛЯ КАЖДОГО МЕТОДА ---
print("\n" + "="*70)
print("СРАВНЕНИЕ МЕТОДОВ АППРОКСИМАЦИИ")
print("="*70)

# Создаем большую фигуру с подграфиками
fig, axes = plt.subplots(3, 3, figsize=(18, 15))
axes = axes.flatten()

# Метод конечных разностей (отдельный график)
max_R_up_fd, max_U_up_fd = calculate_finite_differences(U_up, I_up_mA)
max_R_down_fd, max_U_down_fd = calculate_finite_differences(U_down, I_down_mA)

# Для каждого метода строим график
for i, (method_name, method_func) in enumerate(methods):
    if i >= len(axes) - 1:  # -1 потому что последний график для конечных разностей
        break
        
    ax = axes[i]
    
    # Расчет для повышения тока
    R_up, U_up_full, I_up_full, success_up, U_max_up = calculate_resistance_for_method(
        method_func, U_up, I_up_mA, method_name)
    
    # Расчет для понижения тока
    R_down, U_down_full, I_down_full, success_down, U_max_down = calculate_resistance_for_method(
        method_func, U_down, I_down_mA, method_name)
    
    # Экспериментальные точки
    ax.plot(U_up, I_up_mA, 'bo', markersize=4, alpha=0.7, label='Повышение (эксп.)')
    ax.plot(U_down, I_down_mA, 'ro', markersize=4, alpha=0.7, label='Понижение (эксп.)')
    
    # Аппроксимации
    if success_up:
        ax.plot(U_up_full, I_up_full, 'b-', linewidth=2, label=f'Повышение (аппрокс.)')
    if success_down:
        ax.plot(U_down_full, I_down_full, 'r-', linewidth=2, label=f'Понижение (аппрокс.)')
    
    # Область расчета
    ax.axvline(x=240, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=320, color='gray', linestyle='--', alpha=0.5)
    
    # Заголовок с результатами
    title = method_name
    if success_up and success_down:
        title += f"\nR_диф: ↑{R_up:.1f} кОм, ↓{R_down:.1f} кОм"
    elif success_up:
        title += f"\nR_диф: ↑{R_up:.1f} кОм"
    elif success_down:
        title += f"\nR_диф: ↓{R_down:.1f} кОм"
    else:
        title += "\nНе удалось рассчитать R_диф"
    
    ax.set_title(title, fontsize=10)
    ax.set_xlabel('U_p, В', fontsize=9)
    ax.set_ylabel('I_p, мА', fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(fontsize=8)

# График для метода конечных разностей
ax_fd = axes[-1]
ax_fd.plot(U_up, I_up_mA, 'bo-', markersize=4, alpha=0.7, linewidth=1, label='Повышение (эксп.)')
ax_fd.plot(U_down, I_down_mA, 'ro-', markersize=4, alpha=0.7, linewidth=1, label='Понижение (эксп.)')

# Показываем отрезки с максимальным сопротивлением
if max_R_up_fd is not None:
    # Находим соответствующий отрезок для повышения
    for i in range(len(U_up)-1):
        if 240 <= (U_up[i] + U_up[i+1])/2 <= 320:
            dU = U_up[i+1] - U_up[i]
            dI = I_up_mA[i+1] - I_up_mA[i]
            if abs(dI) > 0.05:
                R_segment = abs(dU / dI)
                if abs(R_segment - max_R_up_fd) < 1:  # Нашли максимальный отрезок
                    ax_fd.plot([U_up[i], U_up[i+1]], [I_up_mA[i], I_up_mA[i+1]], 
                              'g-', linewidth=3, alpha=0.8,
                              label=f'Макс отрезок ↑: {max_R_up_fd:.1f} кОм')
                    break

if max_R_down_fd is not None:
    # Находим соответствующий отрезок для понижения
    for i in range(len(U_down)-1):
        if 240 <= (U_down[i] + U_down[i+1])/2 <= 320:
            dU = U_down[i+1] - U_down[i]
            dI = I_down_mA[i+1] - I_down_mA[i]
            if abs(dI) > 0.05:
                R_segment = abs(dU / dI)
                if abs(R_segment - max_R_down_fd) < 1:  # Нашли максимальный отрезок
                    ax_fd.plot([U_down[i], U_down[i+1]], [I_down_mA[i], I_down_mA[i+1]], 
                              'm-', linewidth=3, alpha=0.8,
                              label=f'Макс отрезок ↓: {max_R_down_fd:.1f} кОм')
                    break

ax_fd.axvline(x=240, color='gray', linestyle='--', alpha=0.5)
ax_fd.axvline(x=320, color='gray', linestyle='--', alpha=0.5)

title_fd = "Метод конечных разностей"
if max_R_up_fd is not None and max_R_down_fd is not None:
    title_fd += f"\nR_диф: ↑{max_R_up_fd:.1f} кОм, ↓{max_R_down_fd:.1f} кОм"
elif max_R_up_fd is not None:
    title_fd += f"\nR_диф: ↑{max_R_up_fd:.1f} кОм"
elif max_R_down_fd is not None:
    title_fd += f"\nR_диф: ↓{max_R_down_fd:.1f} кОм"

ax_fd.set_title(title_fd, fontsize=10)
ax_fd.set_xlabel('U_p, В', fontsize=9)
ax_fd.set_ylabel('I_p, мА', fontsize=9)
ax_fd.grid(True, linestyle='--', alpha=0.3)
ax_fd.legend(fontsize=8)

# Убираем лишние subplots если методов меньше
for i in range(len(methods) + 1, len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.savefig('all_approximation_methods_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# --- СВОДКА РЕЗУЛЬТАТОВ ---
print("\n" + "="*70)
print("СВОДКА РЕЗУЛЬТАТОВ ПО ВСЕМ МЕТОДАМ")
print("="*70)

print("\nМЕТОДЫ АППРОКСИМАЦИИ:")
for method_name, method_func in methods:
    R_up, _, _, success_up, _ = calculate_resistance_for_method(
        method_func, U_up, I_up_mA, method_name)
    R_down, _, _, success_down, _ = calculate_resistance_for_method(
        method_func, U_down, I_down_mA, method_name)
    
    if success_up and success_down:
        print(f"{method_name}: ↑{R_up:.1f} кОм, ↓{R_down:.1f} кОм")
    elif success_up:
        print(f"{method_name}: ↑{R_up:.1f} кОм, ↓не рассчитано")
    elif success_down:
        print(f"{method_name}: ↑не рассчитано, ↓{R_down:.1f} кОм")
    else:
        print(f"{method_name}: не удалось рассчитать")

print(f"\nМЕТОД КОНЕЧНЫХ РАЗНОСТЕЙ:")
if max_R_up_fd is not None and max_R_down_fd is not None:
    print(f"Повышение: {max_R_up_fd:.1f} кОм, Понижение: {max_R_down_fd:.1f} кОм")
    print(f"Среднее: {(max_R_up_fd + max_R_down_fd)/2:.1f} кОм")

print(f"\nРЕКОМЕНДАЦИИ:")
print("1. Выберите метод, который лучше всего следует за экспериментальными точками")
print("2. Учитывайте физическую осмысленность полученного сопротивления")
print("3. Полином 3-й степени часто дает хороший баланс")
print("4. Если методы сильно расходятся, предпочтение отдается конечным разностям")
