import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Ваши данные
l_max = np.array([15.4, 14.4, 13, 10.7, 7, 5.5])  # в см
inv_R_plus_R0 = np.array([0.0246913580246914, 0.0327868852459016,
                          0.0487804878048781, 0.0952380952380952, 0.181818181818182, 0.285714285714286])  # в кОм^-1

# Погрешности
dl_max = 0.1  # для всех l_max

# Функция для линейной аппроксимации: y = k * x + b
def linear_func(x, k, b):
    return k * x + b

# Подгонка параметров k и b с учётом погрешностей (взвешенная регрессия)
# sigma - это погрешности по y (ось Y)
popt, pcov = curve_fit(linear_func, inv_R_plus_R0, l_max, sigma=dl_max, absolute_sigma=True)

k, b = popt
sigma_k, sigma_b = np.sqrt(np.diag(pcov))

print(f"k = {k:.3f} ± {sigma_k:.3f}")
print(f"b = {b:.3f} ± {sigma_b:.3f}")

# Диапазон для прямой: от 0 до чуть больше максимального (R+R0)^-1
x_line = np.linspace(0, max(inv_R_plus_R0) * 1.1, 100)
y_line = linear_func(x_line, k, b)

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(x_line, y_line, label=f'l_max = ({k:.1f} ± {sigma_k:.1f}) * (R+R₀)⁻¹ + ({b:.1f} ± {sigma_b:.1f})', color='red', linestyle='-', linewidth=1.5)

# Строим точки с погрешностями только по Y
plt.errorbar(inv_R_plus_R0, l_max, yerr=dl_max, fmt='o', color='blue', label='Экспериментальные точки', zorder=5, capsize=3)

# Настройки графика
plt.xlabel('(R + R₀)⁻¹, кОм⁻¹')
plt.ylabel('l_max, см')
plt.title('Зависимость l_max от (R + R₀)⁻¹')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
# plt.xlim(left=0)  # Можно убрать, если прямая с b лучше проходит
# plt.ylim(bottom=0) # Аналогично

# Показать график
plt.tight_layout()
plt.savefig('lmax_vs_inv_R_plus_R0.png', dpi=300)  # Если нужно сохранить
plt.show()
