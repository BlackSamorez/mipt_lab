import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
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

# --- КУБИЧЕСКИЕ СПЛАЙНЫ ПО ВСЕМ ТОЧКАМ ---
def calculate_cubic_spline_resistance(U, I, direction_name, U_min=240, U_max=320):
    """Расчет сопротивления через кубические сплайны по всем точкам"""
    
    # Сортировка по напряжению
    sorted_idx = np.argsort(U)
    U_sorted = U[sorted_idx]
    I_sorted = I[sorted_idx]
    
    # Кубический сплайн по ВСЕМ точкам (без сглаживания)
    cs = CubicSpline(U_sorted, I_sorted)
    
    # Для графика: вся кривая по всем точкам
    U_full = np.linspace(U_sorted.min(), U_sorted.max(), 1000)
    I_full = cs(U_full)
    
    # Для расчета сопротивления: только диапазон 240-320 В
    U_calc = np.linspace(U_min, U_max, 1000)
    I_calc = cs(U_calc)
    
    # Производная dI/dU в диапазоне расчета
    dI_dU = cs.derivative()(U_calc)
    
    # Дифференциальное сопротивление R_диф = dU/dI (в кОм, так как ток в мА)
    R_diff = np.full_like(dI_dU, np.nan)
    valid_mask = (np.abs(dI_dU) > 1e-6)
    R_diff[valid_mask] = 1.0 / dI_dU[valid_mask]
    
    # Берем модуль и фильтруем физические значения (1-200 кОм)
    R_diff_abs = np.abs(R_diff)
    physical_mask = (R_diff_abs > 1) & (R_diff_abs < 200) & valid_mask
    
    if np.any(physical_mask):
        max_R = np.max(R_diff_abs[physical_mask])
        max_R_idx = np.argmax(R_diff_abs[physical_mask])
        max_R_U = U_calc[physical_mask][max_R_idx]
        
        # Находим все значения сопротивления выше 90% от максимума для оценки погрешности
        high_R_mask = R_diff_abs > 0.9 * max_R
        high_R_values = R_diff_abs[high_R_mask]
        error = np.std(high_R_values) if len(high_R_values) > 1 else max_R * 0.1
        
        print(f"{direction_name} (кубический сплайн):")
        print(f"  Максимальное |R_диф| = {max_R:.2f} ± {error:.2f} кОм при U = {max_R_U:.1f} В")
        
        return max_R, error, U_full, I_full
    else:
        print(f"{direction_name}: Не найдено физических значений R_диф в диапазоне 1-200 кОм")
        return None, None, U_full, I_full

# --- МЕТОД КОНЕЧНЫХ РАЗНОСТЕЙ ДЛЯ ПРОВЕРКИ ---
def calculate_finite_differences(U, I, direction_name, U_min=240, U_max=320):
    """Метод конечных разностей для проверки"""
    
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
        
        # Оценка погрешности
        top_5_indices = np.argsort(R_diff)[-5:]
        top_5_values = R_diff[top_5_indices]
        error = np.std(top_5_values)
        
        print(f"{direction_name} (конечные разности):")
        print(f"  Максимальное |R_диф| = {max_R:.2f} ± {error:.2f} кОм при U = {max_R_U:.1f} В")
        
        return max_R, error
    return None, None

# --- ВЫЧИСЛЕНИЯ ---
print("\n" + "="*70)
print("РАСЧЕТ ДИФФЕРЕНЦИАЛЬНОГО СОПРОТИВЛЕНИЯ")
print("Метод: кубические сплайны по всем точкам")
print("Расчет сопротивления: диапазон 240-320 В")
print("="*70)

# Основной метод: кубические сплайны
print("\n--- ОСНОВНОЙ МЕТОД: КУБИЧЕСКИЕ СПЛАЙНЫ ---")
max_R_up_spline, error_up_spline, U_up_full, I_up_full = calculate_cubic_spline_resistance(
    U_up, I_up_mA, "Повышение тока")

max_R_down_spline, error_down_spline, U_down_full, I_down_full = calculate_cubic_spline_resistance(
    U_down, I_down_mA, "Понижение тока")

# Метод проверки: конечные разности
print("\n--- МЕТОД ПРОВЕРКИ: КОНЕЧНЫЕ РАЗНОСТИ ---")
max_R_up_fd, error_up_fd = calculate_finite_differences(U_up, I_up_mA, "Повышение тока")
max_R_down_fd, error_down_fd = calculate_finite_differences(U_down, I_down_mA, "Понижение тока")

# --- ПОСТРОЕНИЕ ГРАФИКА ВАХ ---
plt.figure(figsize=(12, 8))

# Экспериментальные точки
plt.plot(U_up, I_up_mA, 'bo', label='Повышение I_p (эксперимент)', markersize=6, alpha=0.8)
plt.plot(U_down, I_down_mA, 'ro', label='Понижение I_p (эксперимент)', markersize=6, alpha=0.8)

# Аппроксимация кубическими сплайнами
plt.plot(U_up_full, I_up_full, 'b-', linewidth=2, label='Кубический сплайн (повышение)')
plt.plot(U_down_full, I_down_full, 'r-', linewidth=2, label='Кубический сплайн (понижение)')

# Область расчета
plt.axvspan(240, 320, alpha=0.1, color='gray', label='Диапазон расчета R_диф (240-320 В)')

plt.xlabel('Напряжение разряда U_p, В', fontsize=12)
plt.ylabel('Ток разряда I_p, мА', fontsize=12)
plt.title('Вольт-амперная характеристика тлеющего разряда\n(аппроксимация кубическими сплайнами)', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.savefig('VA_characteristic_cubic_spline.png', dpi=300, bbox_inches='tight')
plt.show()

# --- АНАЛИЗ РЕЗУЛЬТАТОВ И ПОГРЕШНОСТЕЙ ---
print("\n" + "="*70)
print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ С ПОГРЕШНОСТЯМИ")
print("="*70)

# Основные результаты (кубические сплайны)
if max_R_up_spline is not None and max_R_down_spline is not None:
    avg_R_spline = (max_R_up_spline + max_R_down_spline) / 2
    avg_error_spline = (error_up_spline + error_down_spline) / 2
    
    print("ОСНОВНОЙ МЕТОД (кубические сплайны):")
    print(f"  Среднее R_диф = {avg_R_spline:.1f} ± {avg_error_spline:.1f} кОм")
    print(f"  Повышение тока: {max_R_up_spline:.1f} ± {error_up_spline:.1f} кОм")
    print(f"  Понижение тока: {max_R_down_spline:.1f} ± {error_down_spline:.1f} кОм")

# Результаты проверки (конечные разности)
if max_R_up_fd is not None and max_R_down_fd is not None:
    avg_R_fd = (max_R_up_fd + max_R_down_fd) / 2
    avg_error_fd = (error_up_fd + error_down_fd) / 2
    
    print("\nМЕТОД ПРОВЕРКИ (конечные разности):")
    print(f"  Среднее R_диф = {avg_R_fd:.1f} ± {avg_error_fd:.1f} кОм")

# Сравнение методов и итоговый результат
if (max_R_up_spline is not None and max_R_down_spline is not None and 
    max_R_up_fd is not None and max_R_down_fd is not None):
    
    discrepancy = abs(avg_R_spline - avg_R_fd) / min(avg_R_spline, avg_R_fd) * 100
    
    print(f"\nСРАВНЕНИЕ МЕТОДОВ:")
    print(f"Кубические сплайны: {avg_R_spline:.1f} ± {avg_error_spline:.1f} кОм")
    print(f"Конечные разности: {avg_R_fd:.1f} ± {avg_error_fd:.1f} кОм")
    print(f"Расхождение: {discrepancy:.1f}%")
    
    if discrepancy < 50:
        # Взвешенное среднее с учетом погрешностей
        w1 = 1 / avg_error_spline**2
        w2 = 1 / avg_error_fd**2
        final_R = (w1 * avg_R_spline + w2 * avg_R_fd) / (w1 + w2)
        final_error = 1 / np.sqrt(w1 + w2)
        
        print(f"\nМетоды согласуются")
        print(f"ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: R_диф_max = {final_R:.1f} ± {final_error:.1f} кОм")
    else:
        print(f"\nБольшое расхождение между методами")
        print(f"Предпочтение основному методу (кубические сплайны)")
        print(f"ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: R_диф_max = {avg_R_spline:.1f} ± {avg_error_spline:.1f} кОм")

elif max_R_up_spline is not None and max_R_down_spline is not None:
    print(f"\nФИНАЛЬНЫЙ РЕЗУЛЬТАТ: R_диф_max = {avg_R_spline:.1f} ± {avg_error_spline:.1f} кОм")
    print("(использован только метод кубических сплайнов)")

# Дополнительный анализ
if max_R_up_spline is not None:
    relative_error = avg_error_spline / avg_R_spline * 100
    print(f"\nДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ:")
    print(f"Относительная погрешность: {relative_error:.1f}%")
    print(f"Точность определения: {100 - relative_error:.1f}%")

print(f"\nФИЗИЧЕСКАЯ ИНТЕРПРЕТАЦИЯ:")
if (max_R_up_spline is not None and max_R_up_spline > 10) or (max_R_down_spline is not None and max_R_down_spline > 10):
    print("Высокие значения сопротивления (десятки кОм) характерны для")
    print("аномального тлеющего разряда с большой длиной разрядного промежутка")
    print("или малым давлением газа в трубке")
else:
    print("Значения сопротивления соответствуют нормальному тлеющему разряду")

print(f"\nРЕКОМЕНДАЦИИ ДЛЯ ОТЧЕТА:")
print("1. Использована аппроксимация кубическими сплайнами по всем экспериментальным точкам")
print("2. Дифференциальное сопротивление рассчитано в диапазоне 240-320 В")
print("3. Проведена проверка методом конечных разностей")
print("4. Указаны погрешности измерений")
print("5. Дана физическая интерпретация результатов")
