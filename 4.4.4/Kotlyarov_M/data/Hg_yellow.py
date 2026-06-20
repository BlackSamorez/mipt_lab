import numpy as np
import matplotlib.pyplot as plt

# === ПАРАМЕТРЫ ===
f_mm = 110.0         # фокусное расстояние, мм
lam_A = 5780.0       # средняя длина волны жёлтого дублета, Å
sigma_d = 0.27       # погрешность измерения диаметра, мм

# === ДАННЫЕ: 7 пар колец (пару №2 пропускаем — отрицательная Δd) ===
# Формат: [номер пары, d_внеш, d_внутр]
pairs = [
    (1, 14.39, 10.83),
    (2, 21.61, 19.46),
    (3, 26.95, 25.33),
    (4, 31.41, 30.01),
    (5, 35.36, 34.10),
    (6, 39.00, 37.82),
    (7, 42.36, 41.28)
]

# Извлекаем данные
d_outer = np.array([p[1] for p in pairs])
d_inner = np.array([p[2] for p in pairs])

# Средние и разности
d_avg = (d_outer + d_inner) / 2.0
delta_d = d_outer - d_inner  # > 0 для всех выбранных пар

# Аргумент и зависимая переменная
x = 1.0 / delta_d      # 1/Δd
y = d_avg              # d̄

# === ПОГРЕШНОСТИ ===
sigma_y = sigma_d / np.sqrt(2)
sigma_delta_d = sigma_d * np.sqrt(2)
sigma_x = sigma_delta_d / (delta_d**2)

# === ВЕСА ДЛЯ РЕГРЕССИИ ===
weights = np.ones_like(y) / sigma_y

# Линейная регрессия: y = k * x + b
p, cov = np.polyfit(x, y, deg=1, w=weights, cov='unscaled')
k, b = p
dk = np.sqrt(cov[0, 0])

# === РАСЧЁТ Δλ ===
delta_lambda = (lam_A * k) / (4.0 * f_mm**2)
delta_lambda_err = (lam_A * dk) / (4.0 * f_mm**2)

# === ПРОДЛЕННАЯ ПРЯМАЯ ===
x_line = np.linspace(0, max(x)*1.1, 100)
y_line = k * x_line + b

# === ГРАФИК ===
plt.figure(figsize=(8, 6))
plt.errorbar(x, y, xerr=sigma_x, yerr=sigma_y, fmt='o', capsize=4, label='Эксперимент')
plt.plot(x_line, y_line, 'r--', label=f'Аппроксимация\nk = {k:.2f} ± {dk:.2f} мм²')
plt.xlabel(r'$1 / \Delta d$ (1/мм)')
plt.ylabel(r'$\bar{d}$ (мм)')
plt.title(r'График $\bar{d} = F(1 / \Delta d)$ для жёлтого дублета ртути')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)
plt.xlim(0, max(x)*1.1)
plt.ylim(min(y)*0.9, max(y)*1.1)
plt.tight_layout()
plt.savefig('Hg_yellow.png', dpi=300)
plt.show()

# === ВЫВОД ===
print(f"Использовано пар: {len(pairs)} (пара №2 пропущена)")
print(f"Наклон: k = {k:.3f} ± {dk:.3f} мм²")
print(f"Δλ (Hg) = {delta_lambda:.3f} ± {delta_lambda_err:.3f} Å")
print(f"\nТабличное значение Δλ (Hg) ≈ 10–12 Å")
