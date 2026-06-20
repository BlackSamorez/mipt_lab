import numpy as np
import matplotlib.pyplot as plt

# === ДАННЫЕ ===
# Диаметры 6 колец (мм) — из столбца d_кольца
d_all = np.array([9.715, 12.815, 17.56, 18.99, 22.985, 24.425])

# Разделяем на компоненты дублета:
# Нечётные кольца (1,3,5) → λ₁
# Чётные кольца   (2,4,6) → λ₂
d1 = d_all[::2]   # индексы 0,2,4
d2 = d_all[1::2]  # индексы 1,3,5

# Номера пар (1, 2, 3)
i = np.array([1, 2, 3])

# === ПОГРЕШНОСТЬ ОДНОГО КОЛЬЦА ===
sigma_d = 0.52  # мм — дано вами как погрешность положения одного кольца

# Погрешности d^2
sigma_d2_1 = 2 * d1 * sigma_d
sigma_d2_2 = 2 * d2 * sigma_d

# === ЛИНЕЙНАЯ РЕГРЕССИЯ С ВЕСАМИ ===
def weighted_fit(x, y, sigma_y):
    w = 1.0 / sigma_y**2
    p, cov = np.polyfit(x, y, 1, w=np.sqrt(w), cov=True)
    return p, np.sqrt(np.diag(cov))

d2_1 = d1**2
d2_2 = d2**2

(p1, err1) = weighted_fit(i, d2_1, sigma_d2_1)
(p2, err2) = weighted_fit(i, d2_2, sigma_d2_2)

k1, b1 = p1
k2, b2 = p2
dk1, db1 = err1
dk2, db2 = err2

# === ГРАФИКИ ===
plt.figure(figsize=(12, 5))

# λ₁
plt.subplot(1, 2, 1)
plt.errorbar(i, d2_1, yerr=sigma_d2_1, fmt='o', capsize=5, label='λ₁ (нечётные)')
plt.plot(i, k1*i + b1, 'r--', label=f'k = {k1:.2f} ± {dk1:.2f}')
plt.xlabel('Номер пары')
plt.ylabel(r'$d^2$ (мм²)')
plt.title('Компонента λ₁')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()

# λ₂
plt.subplot(1, 2, 2)
plt.errorbar(i, d2_2, yerr=sigma_d2_2, fmt='o', capsize=5, label='λ₂ (чётные)')
plt.plot(i, k2*i + b2, 'r--', label=f'k = {k2:.2f} ± {dk2:.2f}')
plt.xlabel('Номер пары')
plt.ylabel(r'$d^2$ (мм²)')
plt.title('Компонента λ₂')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.savefig('Na_d_vs_i.png', dpi=300)
plt.show()

# === ВЫВОД ===
print(f"λ₁: наклон k₁ = {k1:.3f} ± {dk1:.3f} мм²")
print(f"λ₂: наклон k₂ = {k2:.3f} ± {dk2:.3f} мм²")
