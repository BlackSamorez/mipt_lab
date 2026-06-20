import numpy as np
import matplotlib.pyplot as plt

# === ПАРАМЕТРЫ ===
f_mm = 94.0          # фокусное расстояние линзы, мм
lam_A = 5893.0       # средняя длина волны натрия, Å
sigma_d = 0.52       # погрешность измерения диаметра одного кольца, мм

# === ДАННЫЕ: 6 колец → 3 пары ===
d_all = np.array([9.715, 12.815, 17.56, 18.99, 22.985, 24.425])  # мм

# Группируем в пары: (1,2), (3,4), (5,6)
d1 = d_all[::2]   # λ₁: кольца 1,3,5
d2 = d_all[1::2]  # λ₂: кольца 2,4,6

# Средние и разности
d_avg = (d1 + d2) / 2.0
delta_d = d2 - d1  # > 0

# Аргумент и зависимая переменная
x = 1.0 / delta_d      # 1/Δd
y = d_avg              # d̄

# === ПОГРЕШНОСТИ ===
sigma_y = sigma_d / np.sqrt(2)               # погрешность d̄
sigma_delta_d = sigma_d * np.sqrt(2)         # погрешность Δd
sigma_x = sigma_delta_d / (delta_d**2)       # погрешность 1/Δd

# === ВЕСА ДЛЯ np.polyfit: w_i = 1 / sigma_y_i ===
# Создаём 1D массив весов той же длины, что и x/y
weights = np.ones_like(y) / sigma_y  # shape (3,), dtype float

# === ЛИНЕЙНАЯ РЕГРЕССИЯ ===
# Важно: cov='unscaled' требуется в новых версиях NumPy при использовании весов
p, cov = np.polyfit(x, y, deg=1, w=weights, cov='unscaled')
k, b = p
dk = np.sqrt(cov[0, 0])
db = np.sqrt(cov[1, 1])

# === РАСЧЁТ Δλ ===
delta_lambda = (lam_A * k) / (4 * f_mm**2)
delta_lambda_err = (lam_A * dk) / (4 * f_mm**2)

# === ПРОДЛЕННАЯ ПРЯМАЯ ===
x_line = np.linspace(0, 1.0, 100)
y_line = k * x_line + b

# === ГРАФИК ===
plt.figure(figsize=(8, 6))
plt.errorbar(x, y, xerr=sigma_x, yerr=sigma_y, fmt='o', capsize=4, label='Эксперимент')
plt.plot(x_line, y_line, 'r--', label=f'Аппроксимация\nk = {k:.2f} ± {dk:.2f} мм²')
plt.xlabel(r'$1 / \Delta d$ (1/мм)')
plt.ylabel(r'$\bar{d}$ (мм)')
plt.title(r'График $\bar{d} = F(1 / \Delta d)$ для дублета натрия')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)
plt.xlim(0, 1.0)
plt.ylim(10, 25)
plt.tight_layout()
plt.savefig('Na_d_delta_d.png', dpi=300)
plt.show()

# === ВЫВОД ===
print(f"Наклон: k = {k:.3f} ± {dk:.3f} мм²")
print(f"Δλ (Na) = {delta_lambda:.3f} ± {delta_lambda_err:.3f} Å")
