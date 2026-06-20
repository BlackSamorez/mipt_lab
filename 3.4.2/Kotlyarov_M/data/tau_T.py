import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Экспериментальные данные
T = np.array([287.1, 289.05, 291.02, 293.06, 295.04, 297.01, 299.0,
              301.0, 303.06, 305.0, 307.0, 309.0, 311.0, 313.0])
y = np.array([0.0660159459035131, 0.0696507103798537, 0.0763186603728153,
              0.0940507682435429, 0.126349485790949, 0.197434239003477,
              0.290230858331642, 0.368826401582281, 0.45342336362546,
              0.508423207430818, 0.570524414117494, 0.630163810389329,
              0.685329861872589, 0.732488766460717])

# Линейный участок: T >= 295.04 K
linear_mask = T >= 295.04
T_lin = T[linear_mask]
y_lin = y[linear_mask]
N = len(T_lin)

# Линейная регрессия
slope, intercept, r_value, p_value, std_err = linregress(T_lin, y_lin)

# Параметр Вейсса
Theta_p = -intercept / slope

# ---- Оценка погрешности Theta_p ----
# 1. Остатки
y_pred = slope * T_lin + intercept
residuals = y_lin - y_pred
# 2. Оценка дисперсии остатков (несмещённая)
sigma2 = np.sum(residuals**2) / (N - 2)
sigma = np.sqrt(sigma2)

# 3. Среднее T на линейном участке
T_mean = np.mean(T_lin)

# 4. Сумма квадратов отклонений T
Sxx = np.sum((T_lin - T_mean)**2)

# 5. Погрешность Theta_p при y=0 (точка пересечения с осью T)
# Формула: delta_Theta = (sigma / |slope|) * sqrt( 1/N + (T_mean**2) / Sxx )
delta_Theta_p = (sigma / abs(slope)) * np.sqrt(1.0/N + (T_mean**2) / Sxx)

# Точка Кюри — последняя точка, где начинается отклонение (ниже линейного участка)
Theta_K = T[~linear_mask][-1]  # 293.06 K

# Построение графика
T_ext = np.linspace(285, 320, 300)
y_ext = slope * T_ext + intercept

plt.figure(figsize=(10, 7))
plt.plot(T, y, 'bo', markersize=6, label=r'Эксперимент: $1/(\tau^2 - \tau_0^2)$')
plt.plot(T_ext, y_ext, 'r--', linewidth=2, label='Линейная экстраполяция (T ≥ 295 K)')

plt.axvline(Theta_p, color='r', linestyle=':', linewidth=2,
            label=r'$\Theta_p = %.2f \pm %.2f\ \mathrm{K}$' % (Theta_p, delta_Theta_p))
plt.axvline(Theta_K, color='g', linestyle='-.', linewidth=2,
            label=r'$\Theta_K \approx %.2f\ \mathrm{K}$' % Theta_K)

plt.xlabel('Температура $T$, K')
plt.ylabel(r'$1/(\tau^2 - \tau_0^2)$, мкс$^{-2}$')
plt.title('Определение точки Кюри и параметра Вейсса с оценкой погрешности')
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(285, 320)
plt.ylim(0, 0.8)
plt.legend()

# Сохраняем
plt.savefig('curie_point.png', dpi=300, bbox_inches='tight')

# Вывод результатов
print(f"Параметр Вейсса: Θₚ = {Theta_p:.2f} ± {delta_Theta_p:.2f} K")
print(f"Точка Кюри (начало отклонения от линейности): Θₖ ≈ {Theta_K:.2f} K")
print(f"Число точек в линейной регрессии: {N}")
print(f"Коэффициент корреляции R = {r_value:.4f}")

plt.show()
