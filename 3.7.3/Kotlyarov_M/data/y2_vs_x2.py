import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Данные
X2 = np.array([1.0000000, 1.8708287, 2.4494897, 2.9154759, 3.3166248, 
               3.6742346, 4.0000000, 4.3011626, 4.5825757, 4.8476799, 
               5.0990195, 5.3385391, 5.5677644, 5.7879185, 6.0000000, 
               6.2048368])  # МГц^1/2

a = np.array([1.51152806983541E-05, 2.01969747568964E-05, 2.51657876947467E-05, 
              3.51409754907902E-05, 4.20688823764864E-05, 4.54195995646128E-05, 
              4.63675452183319E-05, 5.28643507786485E-05, 5.88578159357852E-05, 
              6.06931983620779E-05, 6.09884450895413E-05, 6.65631998088402E-05, 
              6.98565845077279E-05, 7.29256293425499E-05, 7.49218546892236E-05, 
              7.98698774590977E-05])  # см^-1

sigma_a = np.array([5.353E-06, 5.510E-06, 5.587E-06, 5.752E-06, 5.774E-06, 
                    5.834E-06, 5.938E-06, 5.972E-06, 6.013E-06, 6.116E-06, 
                    6.233E-06, 6.314E-06, 6.399E-06, 6.490E-06, 6.634E-06, 
                    6.800E-06])  # погрешности a, см^-1

# Взвешенная линейная регрессия (без свободного члена)
def weighted_linear_fit_no_intercept(x, y, dy):
    """Взвешенная линейная регрессия y = k*x"""
    weights = 1.0 / (dy**2)
    k = np.sum(weights * x * y) / np.sum(weights * x**2)
    
    # Погрешность коэффициента
    sigma_k = 1.0 / np.sqrt(np.sum(weights * x**2))
    
    return k, sigma_k

# Аппроксимация
k, sigma_k = weighted_linear_fit_no_intercept(X2, a, sigma_a)

# Создание точек для линии регрессии
X2_line = np.linspace(0.8, 6.5, 100)
a_line = k * X2_line

# Построение графика
plt.figure(figsize=(10, 6))

# Экспериментальные точки с погрешностями
plt.errorbar(X2, a, yerr=sigma_a, fmt='bo', markersize=5, 
             capsize=3, capthick=1, label='Экспериментальные точки')

# Линия регрессии
plt.plot(X2_line, a_line, 'r-', linewidth=2, 
         label=f'Линейная аппроксимация: α = ({k:.2e} ± {sigma_k:.2e})·√ν')

# Настройки графика
plt.xlabel('√ν, МГц$^{1/2}$', fontsize=12)
plt.ylabel('α, см$^{-1}$', fontsize=12)
plt.title('Зависимость коэффициента затухания α от корня частоты √ν', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xlim(0.8, 6.5)

# Уравнение на графике
equation_text = f'α = ({k:.2e} ± {sigma_k:.2e})·√ν'
plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.legend(fontsize=10)
plt.tight_layout()

# Сохранение графика
filename = 'alpha_vs_sqrt_nu.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"График сохранен как {filename}")

plt.show()

# Вывод параметров в консоль
print("\n" + "="*50)
print("ПАРАМЕТРЫ ЛИНЕЙНОЙ АППРОКСИМАЦИИ α = k·√ν")
print("="*50)
print(f"Коэффициент k = {k:.2e} ± {sigma_k:.2e} см⁻¹/МГц¹ᐧ²")

# Расчет удельной проводимости σ
# Из уравнения (39): α = (4/(√σ·d)) * C_x * (V_φ/c) * √ν
# где d = 0.137 см (радиус центральной жилы)
# C_x и V_φ известны из предыдущих расчетов

# Для примера, если C_x = 2.99e-9 см, V_φ/c = 0.67 (из предыдущих расчетов)
d = 0.137  # см
C_x = 2.99e-9  # см
V_phi_c = 0.67  # относительная фазовая скорость

sigma = (4 * C_x * V_phi_c / (d * k))**2
print(f"\nУдельная проводимость σ ≈ {sigma:.2e} с⁻¹")

# Статистика качества аппроксимации
residuals = a - k * X2
chi2 = np.sum((residuals / sigma_a)**2)
dof = len(X2) - 1  # степени свободы (один параметр)
chi2_reduced = chi2 / dof

print(f"\nСтатистика качества аппроксимации:")
print(f"χ² = {chi2:.2f}")
print(f"Число степеней свободы = {dof}")
print(f"χ²/ν = {chi2_reduced:.2f}")
