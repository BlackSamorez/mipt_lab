import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Данные: λ (нм), sin(φ) для +1 порядка, погрешность sin(φ) для +1, 
# sin(φ) для -1 порядка, погрешность sin(φ) для -1
# Порядок +1
lambda_nm = np.array([404.7, 491.6, 546.1, 577.0, 579.1])
sin_p1 = np.array([0.21954350417923, 0.250098370732508, 
                   0.275539487496139, 0.291272709746264, 0.292473701577892])
err_p1 = np.array([2.36492770817898E-05, 2.3470325588353E-05,
                   2.33023212085092E-05, 2.31896095019817E-05, 2.31807253948465E-05])

# Порядок -1
sin_m1 = np.array([0.217192130998778, 0.244042876635468,
                   0.271550101797676, 0.275637385903541, 0.28784342336985])
err_m1 = np.array([2.36620316267939E-05, 2.35077534642042E-05,
                   2.33298234967436E-05, 2.33016408567439E-05, 2.32147573200058E-05])

# Линейная функция для аппроксимации: y = a*x + b
def linear(x, a, b):
    return a * x + b

# Аппроксимация для +1 порядка
popt_p1, pcov_p1 = curve_fit(linear, lambda_nm, sin_p1, sigma=err_p1, absolute_sigma=True)
a_p1, b_p1 = popt_p1
err_a_p1, err_b_p1 = np.sqrt(np.diag(pcov_p1))

# Аппроксимация для -1 порядка
popt_m1, pcov_m1 = curve_fit(linear, lambda_nm, sin_m1, sigma=err_m1, absolute_sigma=True)
a_m1, b_m1 = popt_m1
err_a_m1, err_b_m1 = np.sqrt(np.diag(pcov_m1))

# Создание графика
plt.figure(figsize=(10, 6))

# Точки с погрешностями для +1 порядка
plt.errorbar(lambda_nm, sin_p1, yerr=err_p1, fmt='o', color='blue', 
             capsize=3, label=f'Порядок +1', markersize=5)

# Точки с погрешностями для -1 порядка
plt.errorbar(lambda_nm, sin_m1, yerr=err_m1, fmt='o', color='red', 
             capsize=3, label=f'Порядок -1', markersize=5)

# Линии аппроксимации
x_fit = np.linspace(400, 600, 100)
plt.plot(x_fit, linear(x_fit, a_p1, b_p1), 'b--', 
         label=f'+1: a = {a_p1*1000000:.2f} ± {err_a_p1*1000000:.2f} мм⁻¹')
plt.plot(x_fit, linear(x_fit, a_m1, b_m1), 'r--', 
         label=f'-1: a = {a_m1*1000000:.2f} ± {err_a_m1*1000000:.2f} мм⁻¹')

# Оформление
plt.xlabel('Длина волны λ, нм')
plt.ylabel('sin(φ)')
plt.title('Зависимость sin(φ) от длины волны для порядков +1 и -1')
plt.grid(True, alpha=0.3)
plt.legend()

# Сохранение
plt.savefig('sin_vs_lambda_fit.png', dpi=300, bbox_inches='tight')
print("График сохранён в файл 'sin_vs_lambda.png'")

# Вывод результатов
print("\n=== Результаты аппроксимации ===")
print(f"Порядок +1: a = {a_p1*1000000:.2f} ± {err_a_p1*1000000:.5f} мм⁻¹, b = {b_p1:.6f} ± {err_b_p1:.6f}")
print(f"Порядок -1: a = {a_m1*1000000:.2f} ± {err_a_m1*1000000:.5f} мм⁻¹, b = {b_m1:.6f} ± {err_b_m1:.6f}")
print(f"\nПериод решётки d (из +1): 1/a = {1/a_p1:.3f} нм = {(1/a_p1)/1000:.3f} ± {(err_a_p1/a_p1/a_p1)/1000:.3f} мкм")
print(f"Период решётки d (из -1): 1/|a| = {1/abs(a_m1):.3f} нм = {(1/a_m1)/1000:.3f} ± {(err_a_m1/a_m1/a_m1)/1000:.3f} мкм")
