import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# === Данные измерений ===
m = np.array([1, 2, 3, 4, 5, 6, 7, 8])                     # номер кольца
D_cm = np.array([5.23333333333333, 7.4, 9.2, 10.7, 11.6, 13, 14.2, 15.1])  # диаметр, см

# Погрешность диаметра (абсолютная, см)
sigma_D = 0.105409255338946

# Вычисляем радиус и квадрат радиуса
r_cm = D_cm / 2
r2_cm2 = r_cm ** 2

# Погрешность радиуса и квадрата радиуса
sigma_r = sigma_D / 2
sigma_r2 = 2 * r_cm * sigma_r

# === Взвешенная линейная регрессия ===
weights = 1 / sigma_r2**2
coeffs, cov = np.polyfit(m, r2_cm2, 1, w=np.sqrt(weights), cov=True)
a, b = coeffs
a_err = np.sqrt(cov[0, 0])
b_err = np.sqrt(cov[1, 1])

print("=== Результаты регрессии ===")
print(f"Коэффициент наклона a = {a:.4f} ± {a_err:.4f} см²")
print(f"Свободный член b = {b:.4f} ± {b_err:.4f} см²")

# === Построение графика с error bars ===
plt.figure(figsize=(8, 6))
plt.errorbar(m, r2_cm2, yerr=sigma_r2, fmt='o', color='blue',
             capsize=3, label='Экспериментальные точки')

# Линия регрессии
x_fit = np.linspace(min(m)-0.5, max(m)+0.5, 100)
y_fit = a * x_fit + b
plt.plot(x_fit, y_fit, 'r-', label=f'Регрессия: a = {a:.3f} ± {a_err:.3f} см²')

plt.xlabel('Номер кольца m')
plt.ylabel('r², см²')
plt.title('Зависимость r² от номера интерференционного кольца')
plt.legend()
plt.grid(True)
plt.savefig('r2_vs_m.png', dpi=300)
plt.show()

# === Расчёт двулучепреломления (no - ne) и его погрешности ===
# Параметры установки (замените на реальные значения!)
lambda_m = 0.63e-6       # длина волны, м
L_m = 0.8                # расстояние от кристалла до экрана, м
no = 2.29                # показатель преломления обыкновенного луча
ell_m = 0.026            # длина кристалла, м

# Перевод наклона из см² в м²
a_m2 = a * 1e-4
a_err_m2 = a_err * 1e-4

# Формула: no - ne = (λ/ℓ) * (no L)² / a
no_minus_ne = (lambda_m / ell_m) * (no * L_m)**2 / a_m2
delta_no_minus_ne = no_minus_ne * (a_err_m2 / a_m2)

print("\n=== Двулучепреломление ===")
print(f"no - ne = {no_minus_ne:.5f} ± {delta_no_minus_ne:.5f}")
