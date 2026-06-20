import matplotlib.pyplot as plt
import numpy as np

# Ваши данные
x_data = np.array([25, 21.9, 19.6, 17.7, 16.2, 14.9, 13.7, 12.6, 11.7, 10.9, 10.1])
I_data = np.array([64.390243902439, 56.1702127659575, 49.811320754717, 44.7457627118644,
                   40.6153846153846, 37.1830985915493, 34.2857142857143, 31.8072289156626,
                   29.6629213483146, 27.7894736842105, 26.1386138613861])

# Погрешности
dx = 0.1  # для всех x
dI = I_data / 66  # для каждого I

# Аппроксимация I = k * x (линейная регрессия без intercept)
# Используем метод наименьших квадратов с весами
weights = 1.0 / (dI**2)  # Веса = 1 / (погрешность)^2
k = np.sum(weights * x_data * I_data) / np.sum(weights * x_data**2)

print(f"k = {k:.3f}")

# Погрешность k
N = len(x_data)
residuals = I_data - k * x_data
chi2 = np.sum(weights * residuals**2)
sigma_k = np.sqrt(1 / (np.sum(weights * x_data**2) * (N - 1)))

print(f"σ_k = {sigma_k:.3f}")
print(f"k ± σ_k = {k:.3f} ± {sigma_k:.3f}")

# Диапазон для прямой: от 0 до чуть больше максимального x
x_line = np.linspace(0, max(x_data) * 1.1, 100)
I_line = k * x_line

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(x_line, I_line, label=f'I = ({k:.3f} ± {sigma_k:.3f}) * x', color='red', linestyle='-', linewidth=1.5)

# Строим точки с погрешностями
plt.errorbar(x_data, I_data, xerr=dx, yerr=dI, fmt='o', color='blue', label='Экспериментальные точки', zorder=5, capsize=3)

# Настройки графика
plt.xlabel('x, см')
plt.ylabel('I, нА')
plt.title('Зависимость тока от координаты')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(left=0)
plt.ylim(bottom=0)

# Показать график
plt.tight_layout()
plt.savefig('I_vs_x.png', dpi=300)  # Если нужно сохранить
plt.show()
