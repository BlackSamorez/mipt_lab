import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Данные в СГС
X1 = np.array([39.478, 483.611, 1421.223, 2852.316, 4776.889, 
               10106.475, 13511.488, 21801.956, 26687.410, 
               32066.345, 37938.759, 44304.654, 51164.029, 
               58516.884]) * 1e12  # (рад/с)^2

Y1 = np.array([9.7972e-08, 1.2217e-06, 3.5533e-06, 7.1442e-06, 1.1901e-05, 
               2.5057e-05, 3.3451e-05, 5.3783e-05, 6.6048e-05, 7.9388e-05, 
               9.3772e-05, 1.0933e-04, 1.2605e-04, 1.4424e-04])  # см^-2

dY1 = np.array([1.57e-09, 1.92e-08, 5.63e-08, 1.13e-07, 1.89e-07, 
                3.98e-07, 5.32e-07, 8.57e-07, 1.05e-06, 1.26e-06, 
                1.49e-06, 1.74e-06, 2.01e-06, 2.30e-06])  # погрешности Y1, см^-2

# Взвешенная линейная регрессия в СГС
def weighted_linear_fit(x, y, dy):
    """Взвешенная линейная регрессия y = a + b*x"""
    weights = 1.0 / (dy**2)
    sum_w = np.sum(weights)
    sum_wx = np.sum(weights * x)
    sum_wy = np.sum(weights * y)
    sum_wx2 = np.sum(weights * x**2)
    sum_wxy = np.sum(weights * x * y)
    
    delta = sum_w * sum_wx2 - sum_wx**2
    
    b = (sum_w * sum_wxy - sum_wx * sum_wy) / delta
    a = (sum_wx2 * sum_wy - sum_wx * sum_wxy) / delta
    
    # Погрешности коэффициентов
    sigma_b = np.sqrt(sum_w / delta)
    sigma_a = np.sqrt(sum_wx2 / delta)
    
    return a, b, sigma_a, sigma_b

# Аппроксимация
a, b, sigma_a, sigma_b = weighted_linear_fit(X1, Y1, dY1)

# Создание точек для линии регрессии
X1_line = np.linspace(min(X1), max(X1), 100)
Y1_line = b * X1_line + a

# Построение графика
plt.figure(figsize=(12, 8))

# Экспериментальные точки с погрешностями
plt.errorbar(X1, Y1, yerr=dY1, fmt='bo', markersize=5, 
             capsize=3, capthick=1, label='Экспериментальные точки')

# Линия регрессии
plt.plot(X1_line, Y1_line, 'r-', linewidth=2, 
         label=f'Линейная аппроксимация')

# Настройки графика
plt.xlabel('X₁, $10^{12}$ (рад/с)$^2$', fontsize=12)
plt.ylabel('Y₁, см$^{-2}$', fontsize=12)
plt.title(r'Зависимость $Y₁=k^2-\alpha^2$ от $X₁=\omega^2$', fontsize=14)
plt.grid(True, alpha=0.3)

# Уравнение на графике
equation_text = f'y = ({b:.2e} ± {sigma_b:.2e})x + ({a:.2e} ± {sigma_a:.2e})'
plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.legend(fontsize=10)
plt.tight_layout()

# Сохранение графика
filename = 'Y1_vs_X1_CGS.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"График сохранен как {filename}")

plt.show()

# Вывод параметров в консоль
print("\n" + "="*60)
print("ПАРАМЕТРЫ ЛИНЕЙНОЙ АППРОКСИМАЦИИ (взвешенной МНК, СГС)")
print("="*60)
print(f"Наклон b = {b:.2e} ± {sigma_b:.2e} см⁻²/(рад/с)²")
print(f"Свободный член a = {a:.2e} ± {sigma_a:.2e} см⁻²")

# Расчет произведения L_x * C_x в СГС
# Из уравнения (30): y1 = (L_x * C_x / c²) * x1
c = 3e10  # скорость света в СГС, см/с
LxCx = b * c**2
dLxCx = sigma_b * c**2  # погрешность произведения

print(f"\nПроизведение L_x * C_x = {LxCx:.6e} ± {dLxCx:.6e} с²/см²")

# Дополнительная статистика
residuals = Y1 - (b * X1 + a)
chi2 = np.sum((residuals / dY1)**2)
dof = len(X1) - 2  # степени свободы
chi2_reduced = chi2 / dof

print(f"\nСтатистика качества аппроксимации:")
print(f"χ² = {chi2:.2f}")
print(f"Число степеней свободы = {dof}")
print(f"χ²/ν = {chi2_reduced:.2f}")

# Обычная линейная регрессия для сравнения
slope_ordinary, intercept_ordinary, r_value, p_value, std_err_ordinary = stats.linregress(X1, Y1)
print(f"\nДля сравнения - обычная МНК (без весов):")
print(f"Наклон = {slope_ordinary:.2e} ± {std_err_ordinary:.2e} см⁻²/(рад/с)²")
print(f"R² = {r_value**2:.6f}")
