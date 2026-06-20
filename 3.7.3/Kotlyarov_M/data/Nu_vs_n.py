import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Данные
n = np.array([1, 2, 3, 4, 5, 6, 7])

# Резонансные частоты для разных случаев
nu_sin_nagr = np.array([3.94, 7.9, 11.91, 15.89, 19.88, 23.89, 27.87])  # синус с нагрузкой
nu_sin_bez_nagr = np.array([3.8, 8.02, 12.05, 16.01, 20.01, 23.99, 27.95])  # синус без нагрузки
nu_pr_nagr = np.array([3.97, 7.95, 11.94, 15.92, 19.91, 23.88, 27.84])  # прямоугольные с нагрузкой
nu_pr_bez_nagr = np.array([3.98, 7.94, 11.9, 15.87, 19.85, 23.82, 27.77])  # прямоугольные без нагрузки

# Оценка погрешности частоты
dnu = 0.01

# Функция для линейной аппроксимации с погрешностями
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

# Аппроксимация для каждого случая
a_sin_nagr, b_sin_nagr, da_sin_nagr, db_sin_nagr = weighted_linear_fit(n, nu_sin_nagr, np.full_like(nu_sin_nagr, dnu))
a_sin_bez_nagr, b_sin_bez_nagr, da_sin_bez_nagr, db_sin_bez_nagr = weighted_linear_fit(n, nu_sin_bez_nagr, np.full_like(nu_sin_bez_nagr, dnu))
a_pr_nagr, b_pr_nagr, da_pr_nagr, db_pr_nagr = weighted_linear_fit(n, nu_pr_nagr, np.full_like(nu_pr_nagr, dnu))
a_pr_bez_nagr, b_pr_bez_nagr, da_pr_bez_nagr, db_pr_bez_nagr = weighted_linear_fit(n, nu_pr_bez_nagr, np.full_like(nu_pr_bez_nagr, dnu))

# Создание точек для линий тренда
n_line = np.linspace(0.5, 7.5, 100)
line_sin_nagr = b_sin_nagr * n_line + a_sin_nagr
line_sin_bez_nagr = b_sin_bez_nagr * n_line + a_sin_bez_nagr
line_pr_nagr = b_pr_nagr * n_line + a_pr_nagr
line_pr_bez_nagr = b_pr_bez_nagr * n_line + a_pr_bez_nagr

# Создание полотна с 4 подграфиками
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Зависимость резонансной частоты от номера резонанса', fontsize=16, fontweight='bold')

# Цвета и метки
colors = ['blue', 'red', 'green', 'purple']
labels = ['Синус с нагрузкой', 'Синус без нагрузки', 
          'Прямоугольные с нагрузкой', 'Прямоугольные без нагрузки']
data_list = [nu_sin_nagr, nu_sin_bez_nagr, nu_pr_nagr, nu_pr_bez_nagr]
coeffs_list = [(a_sin_nagr, b_sin_nagr, da_sin_nagr, db_sin_nagr),
               (a_sin_bez_nagr, b_sin_bez_nagr, da_sin_bez_nagr, db_sin_bez_nagr),
               (a_pr_nagr, b_pr_nagr, da_pr_nagr, db_pr_nagr),
               (a_pr_bez_nagr, b_pr_bez_nagr, da_pr_bez_nagr, db_pr_bez_nagr)]
lines_list = [line_sin_nagr, line_sin_bez_nagr, line_pr_nagr, line_pr_bez_nagr]

# Построение каждого графика
for i, (ax, color, label, data, coeffs, line) in enumerate(zip(axs.flat, colors, labels, data_list, coeffs_list, lines_list)):
    a, b, da, db = coeffs
    
    # Только точки данных с погрешностями (БЕЗ соединения линиями)
    ax.errorbar(n, data, yerr=dnu, fmt='o', color=color, 
               markersize=6, capsize=4, capthick=1, label='Экспериментальные точки')
    
    # Линия тренда (аппроксимация)
    ax.plot(n_line, line, '-', color=color, alpha=0.7, linewidth=2, label='Линейная аппроксимация')
    
    # Настройки подграфика
    ax.set_xlabel('Номер резонанса n', fontsize=11)
    ax.set_ylabel('Резонансная частота ν, МГц', fontsize=11)
    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.5, 7.5)
    
    # Уравнение регрессии на графике
    equation = f'ν = ({b:.3f} ± {db:.3f})n + ({a:.3f} ± {da:.3f})'
    ax.text(0.05, 0.95, equation, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()

# Сохранение графика
filename = 'nu_vs_n_4panels.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"График сохранен как {filename}")

plt.show()

# Вывод параметров в консоль
print("\n" + "="*70)
print("ПАРАМЕТРЫ ЛИНЕЙНОЙ АППРОКСИМАЦИИ ν = a + b·n")
print("="*70)

cases = ['Синус с нагрузкой', 'Синус без нагрузки', 
         'Прямоугольные с нагрузкой', 'Прямоугольные без нагрузки']
all_coeffs = [(a_sin_nagr, b_sin_nagr, da_sin_nagr, db_sin_nagr),
              (a_sin_bez_nagr, b_sin_bez_nagr, da_sin_bez_nagr, db_sin_bez_nagr),
              (a_pr_nagr, b_pr_nagr, da_pr_nagr, db_pr_nagr),
              (a_pr_bez_nagr, b_pr_bez_nagr, da_pr_bez_nagr, db_pr_bez_nagr)]
all_data = [nu_sin_nagr, nu_sin_bez_nagr, nu_pr_nagr, nu_pr_bez_nagr]

for case, coeffs, data in zip(cases, all_coeffs, all_data):
    a, b, da, db = coeffs
    r_squared = stats.linregress(n, data).rvalue**2
    print(f"\n{case}:")
    print(f"  Наклон b = {b:.4f} ± {db:.4f} МГц")
    print(f"  Свободный член a = {a:.4f} ± {da:.4f} МГц")
    print(f"  Коэффициент детерминации R² = {r_squared:.6f}")
