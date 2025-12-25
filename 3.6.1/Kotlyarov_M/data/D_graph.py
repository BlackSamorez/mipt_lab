# script3_a_ratio_vs_m.py
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Создаем папку для графиков, если её нет
graphics_folder = "../Graphics"
os.makedirs(graphics_folder, exist_ok=True)

# --- 1. Чтение данных из D.xlsx ---
try:
    df = pd.read_excel('D.xlsx', sheet_name='Sheet1', header=None)
    if len(df) < 2:
        print("Ошибка: Не хватает данных в D.xlsx.")
        exit()

    m_series = df.iloc[0, :].dropna()
    a_ratio_series = df.iloc[1, :].dropna()

    m_data = m_series[1:].astype(float).to_numpy()
    a_ratio_data = a_ratio_series[1:].astype(float).to_numpy()

    print("Данные успешно загружены из D.xlsx:")
    print(f"m (%): {m_data}")
    print(f"(a_бок/a_осн)^эксп: {a_ratio_data}")

except FileNotFoundError:
    print("Ошибка: Файл 'D.xlsx' не найден.")
    exit()
except Exception as e:
    print(f"Ошибка при чтении файла D.xlsx: {e}")
    import traceback
    traceback.print_exc()
    exit()

# --- 2. Подготовка данных и погрешностей ---
# Погрешности
a_ratio_err = np.full_like(a_ratio_data, 0.001)
m_err = m_data * 0.01

print(f"\nВычисленные значения и погрешности:")
print(f"m (%): {m_data}")
print(f"Погрешность m (%): {m_err}")
print(f"(a_бок/a_осн)^эксп: {a_ratio_data}")
print(f"Погрешность (a_бок/a_осн)^эксп: {a_ratio_err}")

# --- 3. МНК (линейная регрессия y = a*x, через (0,0)) ---
x_data = m_data
y_data = a_ratio_data

slope = np.sum(x_data * y_data) / np.sum(x_data * x_data)

residuals = y_data - slope * x_data
ss_res = np.sum(residuals**2)
ss_tot = np.sum(y_data**2)
if ss_tot > 0:
    r_squared = 1 - (ss_res / ss_tot)
else:
    r_squared = np.nan

y_err_single = a_ratio_err[0]
if np.sum(x_data**2) > 0:
    std_err_slope = y_err_single * np.sqrt(len(x_data) / np.sum(x_data**2))
else:
    std_err_slope = np.nan

print(f"\nРезультаты МНК (y = a*x, где x=m(%), y=(a_бок/a_осн)^эксп):")
print(f"Наклон (a): {slope:.6f} 1/% (или 1/(100%))")
print(f"Погрешность наклона (σ_a): {std_err_slope:.6f} 1/%")
print(f"Коэффициент детерминации (R^2): {r_squared:.6f}")

# --- 4. Построение графика ---
plt.figure(figsize=(10, 6))

x_max_plot = max(x_data) * 1.2
x_fit = np.linspace(0.0, x_max_plot, 100)
y_fit = slope * x_fit
legend_text = r'$(a_{бок}/a_{осн}) = k \cdot m$'
plt.plot(x_fit, y_fit, 'b-', label=legend_text)

plt.errorbar(x_data, y_data, xerr=m_err, yerr=a_ratio_err, fmt='o',
             ecolor='red', markersize=6, label='Экспериментальные данные')

plt.xlabel(r'$m$, %')
plt.ylabel(r'$(a_{бок}/a_{осн})$')
plt.title('Зависимость отношения амплитуд от глубины модуляции')
plt.legend()
plt.grid(True, alpha=0.5)
plt.xlim(0.0, x_max_plot)
plt.ylim(0.0, max(y_data) * 1.2)
plt.tight_layout()

# Сохранение графика
output_filename = 'a_ratio_vs_m_plot_D.png'
full_output_path = os.path.join(graphics_folder, output_filename)
plt.savefig(full_output_path)
print(f"\nГрафик сохранен в файл: {full_output_path}")

try:
    plt.show()
except:
    pass
