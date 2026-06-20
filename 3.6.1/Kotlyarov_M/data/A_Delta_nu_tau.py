# script1_Delta_nu_vs_1_tau.py
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

# --- 1. Чтение данных из A.xlsx ---
try:
    df = pd.read_excel('A.xlsx', sheet_name='Sheet1', header=None)
    if len(df) < 2:
        print("Ошибка: Не хватает данных в A.xlsx.")
        exit()

    tau_series = df.iloc[0, :].dropna()
    delta_nu_series = df.iloc[1, :].dropna()

    tau_data = tau_series[1:].astype(float).to_numpy()
    delta_nu_data = delta_nu_series[1:].astype(float).to_numpy()

    print("Данные успешно загружены из A.xlsx:")
    print(f"tau (мкс): {tau_data}")
    print(f"delta_nu (кГц): {delta_nu_data}")

except FileNotFoundError:
    print("Ошибка: Файл 'A.xlsx' не найден.")
    exit()
except Exception as e:
    print(f"Ошибка при чтении файла A.xlsx: {e}")
    import traceback
    traceback.print_exc()
    exit()

# --- 2. Подготовка данных и погрешностей ---
inv_tau_data = 1.0 / tau_data  # 1/tau (в 1/мкс)
delta_nu_err = np.full_like(delta_nu_data, 0.001)  # Погрешность \Delta \nu: 0.001 кГц
tau_err_constant = 0.5  # мкс, постоянная погрешность tau
inv_tau_err = (1.0 / (tau_data**2)) * tau_err_constant  # Погрешность 1/tau

print(f"\nВычисленные значения и погрешности:")
print(f"1/tau (1/мкс): {inv_tau_data}")
print(f"Погрешность 1/tau (1/мкс): {inv_tau_err}")
print(f"Погрешность \\Delta\\nu (кГц): {delta_nu_err}")

# --- 3. МНК (линейная регрессия y = a*x, через (0,0)) ---
# Зависимость: \Delta \nu = a * (1/tau)
x_data = inv_tau_data
y_data = delta_nu_data

# Для линейной регрессии через 0,0 наклон a = (x*y).sum() / (x*x).sum()
slope = np.sum(x_data * y_data) / np.sum(x_data * x_data)

# Простая оценка погрешности наклона (взвешенная линейная регрессия через 0 требует более сложного подхода)
# Используем стандартную формулу для погрешности наклона при фиксированном нуле
# sigma_a^2 = (sum(y_err^2)) / (sum(x^2)) приближение
# Более точная оценка: sigma_a^2 = sum( (y_i - a*x_i)^2 / y_err_i^2 ) / ( (sum(x_i^2 / y_err_i^2))^2 )
# Но для простоты используем базовую формулу, предполагая, что погрешности y примерно равны
residuals = y_data - slope * x_data
ss_res = np.sum(residuals**2)
ss_tot = np.sum(y_data**2) # Т.к. y_mean=0 для y=ax через 0
if ss_tot > 0:
    r_squared = 1 - (ss_res / ss_tot)
else:
    r_squared = np.nan

# Оценка стандартной ошибки наклона (простая)
# Предполагаем, что погрешности y одинаковы и равны delta_nu_err[0]
y_err_single = delta_nu_err[0]
if np.sum(x_data**2) > 0:
    std_err_slope = y_err_single * np.sqrt(len(x_data) / np.sum(x_data**2))
else:
    std_err_slope = np.nan

print(f"\nРезультаты МНК (y = a*x, где x=1/tau, y=\\Delta\\nu):")
print(f"Наклон (a): {slope:.6f} кГц*мкс")
print(f"Погрешность наклона (σ_a): {std_err_slope:.6f} кГц*мкс")
print(f"Коэффициент детерминации (R^2): {r_squared:.6f}")

# --- 4. Построение графика ---
plt.figure(figsize=(10, 6))

# Построение линии МНК (y = a*x, начинается с (0,0))
x_max_plot = max(x_data) * 1.2
x_fit = np.linspace(0.0, x_max_plot, 100)
y_fit = slope * x_fit
legend_text = r'$\Delta\nu = k \cdot (1/\tau)$'
plt.plot(x_fit, y_fit, 'b-', label=legend_text)

# Нанесение точек с погрешностями
plt.errorbar(x_data, y_data, xerr=inv_tau_err, yerr=delta_nu_err, fmt='o',
             ecolor='red', markersize=6, label='Экспериментальные данные')

# Оформление графика
plt.xlabel(r'$1/\tau$, 1/мкс')
plt.ylabel(r'$\Delta\nu$, кГц')
plt.title('Зависимость ширины спектра от длительности импульса')
plt.legend()
plt.grid(True, alpha=0.5)
plt.xlim(0.0, x_max_plot)
plt.ylim(0.0, max(y_data) * 1.2)
plt.tight_layout()

# Сохранение графика
output_filename = 'Delta_nu_vs_inv_tau_plot_A.png'
full_output_path = os.path.join(graphics_folder, output_filename)
plt.savefig(full_output_path)
print(f"\nГрафик сохранен в файл: {full_output_path}")

try:
    plt.show()
except:
    pass
