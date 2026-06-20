import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib as mpl

# Настройка стиля графиков
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['mathtext.fontset'] = 'cm'

# Экспериментальные данные
I = np.array([0.30000, 1.00000, 1.25000, 1.50000, 1.75000, 
              2.00000, 2.25000, 2.51000, 2.74000, 3.03000])  # Ток, А
B = np.array([0.09722, 0.31944, 0.38889, 0.45833, 0.54167, 
              0.61111, 0.66667, 0.75000, 0.79167, 0.86111])  # Магнитная индукция, Тл

# Линейная модель для калибровки
def linear_model(I, k, b):
    return k * I + b

# Аппроксимация данных линейной функцией
popt, pcov = curve_fit(linear_model, I, B)
k, b = popt
dk, db = np.sqrt(np.diag(pcov))

# Коэффициент детерминации R²
B_pred = linear_model(I, k, b)
ss_res = np.sum((B - B_pred)**2)
ss_tot = np.sum((B - np.mean(B))**2)
r_squared = 1 - (ss_res / ss_tot)

# Создание гладкой кривой для графика
I_smooth = np.linspace(min(I), max(I), 100)
B_smooth = linear_model(I_smooth, k, b)

# Построение графика
plt.figure(figsize=(10, 6))
plt.scatter(I, B, color='red', s=50, zorder=5, label='Экспериментальные точки')
plt.plot(I_smooth, B_smooth, 'b-', linewidth=2, 
         label=f'Аппроксимация: B(I) = ({k:.4f} ± {dk:.4f})·I + ({b:.4f} ± {db:.4f})')

plt.xlabel('Ток I, А', fontsize=14)
plt.ylabel('Магнитная индукция B, Тл', fontsize=14)
plt.title('Градуировочная кривая электромагнита B(I)', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)

# Добавление аннотации с параметрами
textstr = '\n'.join((
    f'k = {k:.4f} ± {dk:.4f} Тл/А',
    f'b = {b:.4f} ± {db:.4f} Тл',
    f'R² = {r_squared:.4f}'))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=props)

plt.tight_layout()

# Сохранение графика
plt.savefig('градуировочная_кривая_B(I).png', dpi=300, bbox_inches='tight')
plt.savefig('градуировочная_кривая_B(I).pdf', bbox_inches='tight')

# Вывод результатов в консоль
print("Результаты аппроксимации:")
print(f"Коэффициент наклона k = {k:.4f} ± {dk:.4f} Тл/А")
print(f"Свободный член b = {b:.4f} ± {db:.4f} Тл")
print(f"Коэффициент детерминации R² = {r_squared:.4f}")
print(f"Относительная погрешность коэффициента k: {dk/k*100:.2f}%")

# Расчет невязок
residuals = B - B_pred
print(f"\nСтатистика невязок:")
print(f"Средняя невязка: {np.mean(residuals):.6f} Тл")
print(f"Стандартное отклонение невязок: {np.std(residuals):.6f} Тл")
print(f"Максимальная невязка: {np.max(np.abs(residuals)):.6f} Тл")

plt.show()
