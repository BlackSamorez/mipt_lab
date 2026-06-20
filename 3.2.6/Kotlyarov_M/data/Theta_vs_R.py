import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Ваши данные
R_plus_R0 = np.array([552.25,	756.25,	992.25,	1482.25,	2162.25,	2862.25,	5700.25
])  # в кОм
inv_theta2 = np.array([0.193451816678823, 0.248143394849879, 0.332353906163154,
                       0.498842640129033, 0.710240077336327, 0.888534014746984, 1.59082251378463])

# Погрешности для 1/theta^2
d_inv_theta2 = np.array([0.0244388154697937, 0.0277156368862966, 0.0324271769463498,
                         0.0290044961574231, 0.0431605241791708, 0.0393915582328418, 0.0710443300669637])

# Функция для линейной аппроксимации: y = k * x + b
def linear_func(x, k, b):
    return k * x + b

# Подгонка параметров k и b с учётом погрешностей (взвешенная регрессия)
# sigma - это погрешности по y (ось Y)
popt, pcov = curve_fit(linear_func, R_plus_R0, inv_theta2, sigma=d_inv_theta2, absolute_sigma=True)

k, b = popt
sigma_k, sigma_b = np.sqrt(np.diag(pcov))

print(f"k = {k:.6f} ± {sigma_k:.6f}")
print(f"b = {b:.6f} ± {sigma_b:.6f}")

# Диапазон для прямой: от 0 до чуть больше максимального R+R0
x_line = np.linspace(0, max(R_plus_R0) * 1.1, 100)
y_line = linear_func(x_line, k, b)

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(x_line, y_line, label=f'1/θ² = ({k:.5f} ± {sigma_k:.5f}) * (R+R₀) + ({b:.5f} ± {sigma_b:.5f})', color='red', linestyle='-', linewidth=1.5)

# Строим точки с погрешностями только по Y
plt.errorbar(R_plus_R0, inv_theta2, yerr=d_inv_theta2, fmt='o', color='blue', label='Экспериментальные точки', zorder=5, capsize=3)

# Настройки графика
plt.xlabel('R + R₀, кОм')
plt.ylabel('1/θ²')
plt.title('Зависимость 1/θ² от (R + R₀)²')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
# plt.xlim(left=0)  # Можно убрать, если прямая с b лучше проходит
# plt.ylim(bottom=0) # Аналогично

# Показать график
plt.tight_layout()
plt.savefig('inv_theta2_vs_R_plus_R0_linear_with_b.png', dpi=300)  # Если нужно сохранить
plt.show()
