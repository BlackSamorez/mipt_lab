import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import warnings

# Отключим предупреждения scipy, если нужно
warnings.filterwarnings("ignore")

# Чтение данных
file_path = 'T_n_vs_I.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Переименование столбцов
df.columns = ['I_p_mA', 'T_e_K', 'sigma_T_e_K', 'n_e_cm3', 'sigma_n_i_cm3']

# Преобразование в числовые типы
df['I_p_mA'] = pd.to_numeric(df['I_p_mA'], errors='coerce')
df['T_e_K'] = pd.to_numeric(df['T_e_K'], errors='coerce')
df['n_e_cm3'] = pd.to_numeric(df['n_e_cm3'], errors='coerce')
df.dropna(subset=['I_p_mA', 'T_e_K', 'n_e_cm3'], inplace=True)

print("Загруженные данные:")
print(df)

# График 1: Te(Ip) — только точки с ошибками
plt.figure(figsize=(8, 6))
plt.errorbar(df['I_p_mA'], df['T_e_K'], yerr=df['sigma_T_e_K'], fmt='o', capsize=5, color='blue', label='Температура электронов')
plt.xlabel('Ток разряда $I_p$, мА', fontsize=12)
plt.ylabel('Температура электронов $T_e$, К', fontsize=12)
plt.title('Зависимость температуры электронов от тока разряда', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('Te_vs_Ip_points.png', dpi=300)
plt.show()

# График 2: ne(Ip) — линейная аппроксимация МНК БЕЗ СВОБОДНОГО ЧЛЕНА (y = kx)

def linear_func_no_intercept(x, a):
    return a * x

x_data = df['I_p_mA'].values
y_data = df['n_e_cm3'].values
sigma_y = df['sigma_n_i_cm3'].values

print("\nДанные для аппроксимации:")
print(f"x_data (I_p_mA): {x_data}")
print(f"y_data (n_e_cm3): {y_data}")
print(f"sigma_y: {sigma_y}")

# Ручной расчет коэффициента k для y = kx (без свободного члена)
# k = Σ(x*y) / Σ(x^2)
k = np.sum(x_data * y_data) / np.sum(x_data**2)

# Расчет ошибки коэффициента
n = len(x_data)
residuals = y_data - k * x_data
mse = np.sum(residuals**2) / (n - 1) if n > 1 else 0
s_xx = np.sum(x_data**2)
k_err = np.sqrt(mse / s_xx) if s_xx > 0 else 0

print(f"\nРезультаты аппроксимации (y = kx):")
print(f"Коэффициент k = {k:.2e} ± {k_err:.2e}")

# Расчет R²
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
print(f"Коэффициент детерминации R² = {r_squared:.4f}")

# Построение графика
plt.figure(figsize=(8, 6))
plt.errorbar(x_data, y_data / 1e10, yerr=sigma_y / 1e10, fmt='s', capsize=5, 
             color='orange', label='Экспериментальные точки')

# Прямая y = kx - начинается из (0,0) и ПРОДЛЕВАЕТСЯ ДАЛЕКО ЗА ПРЕДЕЛЫ ДАННЫХ
x_min = 0  # Начинаем из нуля
x_max = 7  # Продлеваем до 7 мА (за пределы данных)
x_plot = np.linspace(x_min, x_max, 500)
y_plot = k * x_plot / 1e10

# Подпись
label = f'$n_e = ({k/1e10:.2f} \\pm {k_err/1e10:.2f}) I_p \\times 10^{{10}}$ см$^{{-3}}$'

plt.plot(x_plot, y_plot, 'r-', linewidth=2, label=label)

plt.xlabel('Ток разряда $I_p$, мА', fontsize=12)
plt.ylabel('Концентрация электронов $n_e$, 10$^{10}$ см$^{-3}$', fontsize=12)
plt.title('Зависимость концентрации электронов от тока разряда', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.xlim(0, x_max)  # Гарантируем, что ноль будет в левом углу
plt.tight_layout()
plt.savefig('ne_vs_Ip_linear_fit.png', dpi=300)
plt.show()

print("\n✅ Графики сохранены как 'Te_vs_Ip_points.png' и 'ne_vs_Ip_linear_fit.png'")
