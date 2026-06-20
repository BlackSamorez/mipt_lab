import numpy as np
import matplotlib.pyplot as plt

# === ПАРАМЕТРЫ ===
f_mm = 110.0         # фокусное расстояние, мм
lam_A = 5461.0       # длина волны зелёной линии, Å
sigma_d = 0.27       # погрешность измерения диаметра, мм

# === ДАННЫЕ: 7 колец зелёной линии ===
i = np.arange(1, 8)  # номера колец: 1..7
d = np.array([12.67, 20.38, 25.79, 30.23, 34.15, 37.65, 40.91])  # мм

# Вычисляем d² и погрешности
d2 = d**2
sigma_d2 = 2 * d * sigma_d

# === ВЕСА ДЛЯ РЕГРЕССИИ ===
weights = np.ones_like(d2) / sigma_d2

# Линейная регрессия: d² = k * i
p, cov = np.polyfit(i, d2, deg=1, w=weights, cov='unscaled')
k, b = p
dk = np.sqrt(cov[0, 0])

# === РАСЧЁТ БАЗЫ L ===
# L = λ / (4 * f² * k)  [в мм, если f в мм, λ в Å → переводим]
# 1 мм = 10⁷ Å → L (мм) = (λ (Å) * 10⁻⁷) / (4 * (f (мм) * 10⁻³)² * k (мм²))
# Упрощённо: L (мм) = (λ * 10) / (4 * f² * k)
L_mm = (lam_A * 10.0) / (4.0 * f_mm**2 * k)
dL_mm = L_mm * (dk / k)

# === ПРОДЛЕННАЯ ПРЯМАЯ ===
i_line = np.linspace(0, 8, 100)
d2_line = k * i_line + b

# === ГРАФИК ===
plt.figure(figsize=(8, 6))
plt.errorbar(i, d2, yerr=sigma_d2, fmt='o', capsize=4, label='Эксперимент')
plt.plot(i_line, d2_line, 'r--', label=f'Аппроксимация\nk = {k:.2f} ± {dk:.2f} мм²')
plt.xlabel('Номер кольца $i$')
plt.ylabel(r'$d^2$ (мм²)')
plt.title(r'График $d^2 = F(i)$ для зелёной линии ртути ($\lambda = 5461$ Å)')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)
plt.xlim(0, 8)
plt.ylim(0, max(d2)*1.1)
plt.tight_layout()
plt.savefig('Hg_green.png', dpi=300)
plt.show()

# === ВЫВОД ===
print(f"Наклон: k = {k:.3f} ± {dk:.3f} мм²")
print(f"База интерферометра: L = {L_mm:.3f} ± {dL_mm:.3f} мм")
