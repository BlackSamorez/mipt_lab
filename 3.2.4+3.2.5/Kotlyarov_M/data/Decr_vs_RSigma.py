# script2_Decr_vs_RSigma_with_errors.py
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

# --- 1. Чтение данных из Decr_R_1.xlsx ---
try:
    df = pd.read_excel('Decr_R_1.xlsx', sheet_name='Sheet1', header=None)
    if len(df) < 4:
        print("Ошибка: Не хватает данных в Decr_R_1.xlsx (нужны 4 строки).")
        exit()

    # Пропускаем первую ячейку в каждой строке (текстовый заголовок)
    R_sigma_series = df.iloc[0, 1:].dropna()   # R_Sigma, Ом
    dR_sigma_series = df.iloc[1, 1:].dropna()  # погрешность R_Sigma
    Theta_series = df.iloc[2, 1:].dropna()     # Theta
    dTheta_series = df.iloc[3, 1:].dropna()    # погрешность Theta

    R_sigma_data = R_sigma_series.astype(float).to_numpy()
    dR_sigma_data = dR_sigma_series.astype(float).to_numpy()
    Theta_data = Theta_series.astype(float).to_numpy()
    dTheta_data = dTheta_series.astype(float).to_numpy()

    print("Данные успешно загружены из Decr_R_1.xlsx:")
    print(f"R_Sigma (Ом): {R_sigma_data}")
    print(f"ΔR_Sigma (Ом): {dR_sigma_data}")
    print(f"Theta: {Theta_data}")
    print(f"ΔTheta: {dTheta_data}")

except FileNotFoundError:
    print("Ошибка: Файл 'Decr_R_1.xlsx' не найден.")
    exit()
except Exception as e:
    print(f"Ошибка при чтении файла Decr_R_1.xlsx: {e}")
    import traceback
    traceback.print_exc()
    exit()

# --- 2. Подготовка данных для графика 1/Theta^2 vs 1/R_Sigma^2 ---
X_data = 1.0 / (R_sigma_data ** 2)  # X = 1/R_Sigma^2
Y_data = 1.0 / (Theta_data ** 2)    # Y = 1/Theta^2

# Погрешности для X и Y (по правилу дифференцирования)
dX = 2 * dR_sigma_data / (R_sigma_data ** 3)      # d(1/R^2)/dR = -2/R^3 → |dX| = 2*dR/R^3
dY = 2 * dTheta_data / (Theta_data ** 3)          # d(1/Θ^2)/dΘ = -2/Θ^3 → |dY| = 2*dΘ/Θ^3

print(f"\nВычисленные значения для графика:")
print(f"X = 1/R_Sigma^2: {X_data}")
print(f"Y = 1/Theta^2: {Y_data}")
print(f"Погрешность X: {dX}")
print(f"Погрешность Y: {dY}")

# --- 3. МНК (линейная регрессия y = k*x, через (0,0)) ---
x_data = X_data  # X = 1/R_Sigma^2 — ось X
y_data = Y_data  # Y = 1/Theta^2 — ось Y

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

# Расчет R_cr
R_cr_exp = 2 * np.pi * np.sqrt(k)  # R_cr = 2π * sqrt(k)
std_err_R_cr = 2 * np.pi * (std_err_k / (2 * np.sqrt(k))) if k > 0 else np.nan

print(f"\nРезультаты МНК (y = k*x, где x=1/R_Sigma^2, y=1/Theta^2):")
print(f"Наклон (k): {k:.6f}")
print(f"Погрешность наклона (σ_k): {std_err_k:.6f}")
print(f"Коэффициент детерминации (R^2): {r_squared:.6f}")
print(f"Экспериментальное R_cr: {R_cr_exp:.2f} Ом")
print(f"Погрешность R_cr: {std_err_R_cr:.2f} Ом")

# --- 4. Построение графика ---
plt.figure(figsize=(10, 6))

# Линия МНК: y = k*x (начинается с (0,0))
x_max_plot = max(x_data) * 1.2
x_fit = np.linspace(0.0, x_max_plot, 100)
y_fit = k * x_fit
legend_text = r'$\frac{1}{\Theta^2} = k \cdot \frac{1}{R_{\Sigma}^2}$'
plt.plot(x_fit, y_fit, 'b-', linewidth=2, label=legend_text)

# Нанесение точек с погрешностями — КРЕСТИКИ!
plt.errorbar(x_data, y_data,
             xerr=dX, yerr=dY,
             fmt='o', ecolor='red', markersize=6,
             capsize=5, capthick=1,
             label='Экспериментальные данные')

# Оформление графика
plt.xlabel(r'$\frac{1}{R_{\Sigma}^2}, \text{Ом}^{-2}$')
plt.ylabel(r'$\frac{1}{\Theta^2}$')
plt.title('Зависимость $1/\\Theta^2$ от $1/R_{\\Sigma}^2$ для определения $R_{cr}$')
plt.legend()
plt.grid(True, alpha=0.5)
plt.xlim(0.0, x_max_plot)
plt.ylim(0.0, max(y_data) * 1.2)
plt.tight_layout()

# Сохранение графика
output_filename = 'Decr_vs_RSigma_plot_with_errors.png'
full_output_path = os.path.join(graphics_folder, output_filename)
plt.savefig(full_output_path)
print(f"\nГрафик сохранен в файл: {full_output_path}")

try:
    plt.show()
except:
    pass
