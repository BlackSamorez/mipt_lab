import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Данные
X3 = np.array([1.000, 6.548, 14.697, 24.782, 36.483, 64.000, 79.572, 
               113.920, 132.575, 152.148, 172.601, 193.895, 216.000, 
               238.886])  # МГц^3/2

Y3 = np.array([4.737E-09, 2.233E-08, 4.744E-08, 9.394E-08, 1.451E-07,
               2.321E-07, 3.058E-07, 4.451E-07, 4.957E-07, 5.931E-07, 
               6.765E-07, 7.625E-07, 8.412E-07, 9.593E-07])  # см^-2

sigma_Y3 = np.array([1.678E-09, 6.093E-09, 1.054E-08, 1.539E-08, 1.995E-08, 
                     2.978E-08, 3.462E-08, 4.499E-08, 5.081E-08, 5.646E-08,
                     6.220E-08, 6.814E-08, 7.478E-08, 8.203E-08])  # погрешности Y3, см^-2

# Взвешенная линейная регрессия (без свободного члена)
def weighted_linear_fit_no_intercept(x, y, dy):
    """Взвешенная линейная регрессия y = k*x"""
    weights = 1.0 / (dy**2)
    k = np.sum(weights * x * y) / np.sum(weights * x**2)
    
    # Погрешность коэффициента
    sigma_k = 1.0 / np.sqrt(np.sum(weights * x**2))
    
    return k, sigma_k

# Аппроксимация
k, sigma_k = weighted_linear_fit_no_intercept(X3, Y3, sigma_Y3)

# Создание точек для линии регрессии
X3_line = np.linspace(0, 250, 100)
Y3_line = k * X3_line

# Построение графика
plt.figure(figsize=(10, 6))

# Экспериментальные точки с погрешностями
plt.errorbar(X3, Y3, yerr=sigma_Y3, fmt='bo', markersize=5, 
             capsize=3, capthick=1, label='Экспериментальные точки')

# Линия регрессии
plt.plot(X3_line, Y3_line, 'r-', linewidth=2, 
         label=f'Линейная аппроксимация: Y₃ = ({k:.2e} ± {sigma_k:.2e})·X₃')

# Настройки графика
plt.xlabel('X₃, МГц$^{3/2}$', fontsize=12)
plt.ylabel('Y₃, см$^{-2}$', fontsize=12)
plt.title('Зависимость Y₃ = α·k от X₃ = ν$^{3/2}$', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xlim(0, 250)

# Уравнение на графике
equation_text = f'Y₃ = ({k:.2e} ± {sigma_k:.2e})·X₃'
plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.legend(fontsize=10)
plt.tight_layout()

# Сохранение графика
filename = 'Y3_vs_X3.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"График сохранен как {filename}")

plt.show()

# Вывод параметров в консоль
print("\n" + "="*50)
print("ПАРАМЕТРЫ ЛИНЕЙНОЙ АППРОКСИМАЦИИ Y₃ = k·X₃")
print("="*50)
print(f"Коэффициент k = {k:.2e} ± {sigma_k:.2e} см⁻²/МГц³ᐧ²")

# Расчет удельной проводимости σ по методу Б
# Из уравнения (48): σ = [4π·C_x / (d·c·k)]²
# где:
# C_x - погонная емкость (из предыдущих расчетов)
# d - диаметр центральной жилы
# c - скорость света
# k - наклон графика

# Параметры (в СГС)
d = 0.137  # см (радиус центральной жилы)
c = 3e10  # см/с
C_x = 2.99e-9  # см (из предыдущих расчетов)

sigma = (4 * np.pi * C_x / (d * c * k))**2
print(f"\nУдельная проводимость σ (метод Б) = {sigma:.2e} с⁻¹")

# Статистика качества аппроксимации
residuals = Y3 - k * X3
chi2 = np.sum((residuals / sigma_Y3)**2)
dof = len(X3) - 1  # степени свободы (один параметр)
chi2_reduced = chi2 / dof

print(f"\nСтатистика качества аппроксимации:")
print(f"χ² = {chi2:.2f}")
print(f"Число степеней свободы = {dof}")
print(f"χ²/ν = {chi2_reduced:.2f}")

# Сравнение с методом А (если известно)
# sigma_A = ...  # из предыдущих расчетов
# print(f"Удельная проводимость σ (метод А) = {sigma_A:.2e} с⁻¹")
# print(f"Относительное расхождение = {abs(sigma-sigma_A)/max(sigma,sigma_A)*100:.1f}%")
