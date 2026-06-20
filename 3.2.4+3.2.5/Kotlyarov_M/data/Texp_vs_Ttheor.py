# script2_Texp_vs_Ttheor_manual_cross_v2.py
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import os

# Создаем папку для графиков, если её нет
graphics_folder = "../Graphics"
os.makedirs(graphics_folder, exist_ok=True)

# --- 1. Чтение данных из C_T.xlsx ---
try:
    df = pd.read_excel('C_T.xlsx', sheet_name='Sheet1', header=None)
    if len(df) < 3:
        print("Ошибка: Не хватает данных в C_T.xlsx.")
        exit()

    # Пропускаем первую ячейку в каждой строке (текстовый заголовок)
    C_series = df.iloc[0, 1:].dropna()
    T_exp_series = df.iloc[1, 1:].dropna()  # T_эксп — строка 1
    T_theor_series = df.iloc[2, 1:].dropna()  # T_теор — строка 2

    C_data = C_series.astype(float).to_numpy()  # С в нФ
    T_exp_data = T_exp_series.astype(float).to_numpy()  # T_эксп в мкс
    T_theor_data = T_theor_series.astype(float).to_numpy()  # T_теор в мкс

    print("Данные успешно загружены из C_T.xlsx:")
    print(f"C (нФ): {C_data}")
    print(f"T_эксп (мкс): {T_exp_data}")
    print(f"T_теор (мкс): {T_theor_data}")

except FileNotFoundError:
    print("Ошибка: Файл 'C_T.xlsx' не найден.")
    exit()
except Exception as e:
    print(f"Ошибка при чтении файла C_T.xlsx: {e}")
    import traceback
    traceback.print_exc()
    exit()

# --- 2. Подготовка данных и погрешностей ---
# Погрешности (новые значения)
T_exp_err = 0.01 * T_exp_data  # 1% от T_эксп
T_theor_err = 0.0015 * T_theor_data  # 0.15% от T_теор

print(f"\nВычисленные значения и погрешности:")
print(f"T_эксп (мкс): {T_exp_data}")
print(f"Погрешность T_эксп (мкс): {T_exp_err}")
print(f"T_теор (мкс): {T_theor_data}")
print(f"Погрешность T_теор (мкс): {T_theor_err}")

# --- 3. МНК (линейная регрессия y = k*x, через (0,0)) ---
x_data = T_theor_data  # T_теор — ось X
y_data = T_exp_data    # T_эксп — ось Y

# Наклон k = (sum(x*y)) / (sum(x^2))
k = np.sum(x_data * y_data) / np.sum(x_data * x_data)

# Оценка погрешности наклона
residuals = y_data - k * x_data
ss_res = np.sum(residuals**2)
n = len(x_data)
if n > 1 and np.sum(x_data**2) > 0:
    std_err_k = np.sqrt(ss_res / (n - 1)) / np.sqrt(np.sum(x_data**2))
else:
    std_err_k = np.nan

# Коэффициент детерминации R^2
ss_tot = np.sum(y_data**2)
r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else np.nan

print(f"\nРезультаты МНК (y = k*x, где x=T_теор, y=T_эксп):")
print(f"Наклон (k): {k:.6f}")
print(f"Погрешность наклона (σ_k): {std_err_k:.6f}")
print(f"Коэффициент детерминации (R^2): {r_squared:.6f}")

# --- 4. Построение графика ---
plt.figure(figsize=(10, 6))

# Линия МНК: y = k*x (начинается с (0,0))
x_max_plot = max(x_data) * 1.2
x_fit = np.linspace(0.0, x_max_plot, 100)
y_fit = k * x_fit
legend_text = r'$T_{\text{эксп}} = k \cdot T_{\text{теор}}$'
plt.plot(x_fit, y_fit, 'b-', linewidth=2, label=legend_text)

# --- Нанесение точек как крестиков вручную ---
# 1. Рисуем линии погрешностей (как раньше)
# Вертикальные
plt.errorbar(x_data, y_data - T_exp_err, yerr=[T_exp_err, T_exp_err], fmt='none', ecolor='red', linewidth=1.0)
# Горизонтальные
plt.errorbar(x_data - T_theor_err, y_data, xerr=[T_theor_err, T_theor_err], fmt='none', ecolor='red', linewidth=1.0)

# 2. Рисуем чистые крестики (только линии) поверх линий погрешностей
# Используем plt.plot с маркером '+'
# markersize - размер крестика
# markeredgewidth - толщина линии крестика
# color - цвет крестика
plt.plot(x_data, y_data, marker='+', markersize=10, markeredgewidth=2, color='red', linestyle='none', label='Экспериментальные данные')

# Оформление графика
plt.xlabel(r'$T_{\text{теор}}, мкс$')
plt.ylabel(r'$T_{\text{эксп}}, мкс$')
plt.title('Зависимость экспериментального периода от теоретического')
plt.legend()
plt.grid(True, alpha=0.5)
plt.xlim(0.0, x_max_plot)
plt.ylim(0.0, max(y_data) * 1.2)
plt.tight_layout()

# Сохранение графика
output_filename = 'Texp_vs_Ttheor_plot.png'
full_output_path = os.path.join(graphics_folder, output_filename)
plt.savefig(full_output_path)
print(f"\nГрафик сохранен в файл: {full_output_path}")

try:
    plt.show()
except:
    pass
