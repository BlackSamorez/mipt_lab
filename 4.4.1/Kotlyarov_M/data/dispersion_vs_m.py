import numpy as np
import matplotlib.pyplot as plt

# Параметры
d_nm = 2000
lambda_nm = 578.05
rad_to_arcsec = 206265
nm_to_angstrom = 10

# Экспериментальные данные
exp_data = {
    1:  {'D': 259 / 21,   'err': 5 / 21},
    -1: {'D': 243 / 21,   'err': 5 / 21},
    2:  {'D': 566 / 21,   'err': 5 / 21},
    -2: {'D': 548 / 21,   'err': 5 / 21}
}

# Теоретическая кривая
m_cont = np.linspace(-3, 3, 500)
D_cont = []
for m in m_cont:
    abs_m = abs(m)
    sin_phi = abs_m * lambda_nm / d_nm
    if sin_phi <= 1:
        cos_phi = np.sqrt(1 - sin_phi**2)
        D = (abs_m * rad_to_arcsec) / (d_nm * cos_phi * nm_to_angstrom)
    else:
        D = np.nan
    D_cont.append(D)

# Целые порядки
m_int = np.array([-3, -2, -1, 1, 2, 3])
D_int = []
for m in m_int:
    abs_m = abs(m)
    sin_phi = abs_m * lambda_nm / d_nm
    if sin_phi <= 1:
        cos_phi = np.sqrt(1 - sin_phi**2)
        D = (abs_m * rad_to_arcsec) / (d_nm * cos_phi * nm_to_angstrom)
    else:
        D = np.nan
    D_int.append(D)

# Вывод таблицы
print("Сравнение теоретических и экспериментальных значений дисперсии:")
print("-" * 65)
print(f"{'Порядок':^8} | {'Теория (угл.сек/Å)':^18} | {'Эксперимент (угл.сек/Å)':^22} | {'Отклонение':^12}")
print("-" * 65)

for i, m in enumerate(m_int):
    if m in exp_data:  # ← исправлено
        D_theor = D_int[i]
        D_exp = exp_data[m]['D']
        deviation = D_exp - D_theor
        print(f"{m:^8} | {D_theor:^18.3f} | {D_exp:^22.3f} | {deviation:^+12.3f}")
    else:
        D_theor = D_int[i]
        print(f"{m:^8} | {D_theor:^18.3f} | {'нет данных':^22} | {'—':^12}")

print("-" * 65)

# График
plt.figure(figsize=(10, 6))

# Теория
plt.plot(m_cont, D_cont, 'b-', linewidth=1.5, label='Теоретическая кривая')
plt.plot(m_int, D_int, 'bo', markersize=4, label='Теория (целые m)', zorder=3)

# Экспериментальные точки с погрешностями по D
m_exp = list(exp_data.keys())
D_exp = [exp_data[m]['D'] for m in m_exp]
err_exp = [exp_data[m]['err'] for m in m_exp]

# Погрешности ТОЛЬКО по Y (D), без засечек
for m, d, e in zip(m_exp, D_exp, err_exp):
    # Вертикальная линия (погрешность по D)
    plt.plot([m, m], [d - e, d + e], 'r-', linewidth=1.5, zorder=4)
    # Точка
    plt.plot(m, d, 'ro', markersize=3, zorder=5)

plt.xlabel('Порядок спектра m')
plt.ylabel('Угловая дисперсия D, угл. сек/Å')
plt.title('Зависимость угловой дисперсии от порядка спектра\n(λ = 578 нм, d = 2 мкм)')
plt.grid(True, alpha=0.3)
plt.xticks(range(-3, 4))
plt.xlim(-3.5, 3.5)
plt.ylim(bottom=0)

# Легенда
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='b', lw=1.5, label='Теоретическая кривая'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='b', markersize=6, label='Теория (целые m)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=4, label='Эксперимент'),
    Line2D([0], [0], color='r', lw=1.5, label='Погрешность D')
]
plt.legend(handles=legend_elements, loc='upper left')

plt.tight_layout()
plt.savefig('dispersion_vs_m.png', dpi=300)
plt.show()
