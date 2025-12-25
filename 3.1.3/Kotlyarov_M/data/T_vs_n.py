import matplotlib.pyplot as plt
import numpy as np

# Ваши данные
n_data = np.array([12, 10, 8, 6, 4, 3])
T_data = np.array([3.748, 3.158, 2.696, 1.99, 1.35, 1.059])

# Аппроксимация T = k * n (линейная регрессия без intercept)
k = np.sum(n_data * T_data) / np.sum(n_data**2)
print(f"k = {k:.3f}")

# Погрешность k
N = len(n_data)
residuals = T_data - k * n_data
chi2 = np.sum(residuals**2)
sigma_k = np.sqrt(chi2 / (np.sum(n_data**2) * (N - 1)))

print(f"σ_k = {sigma_k:.3f}")
print(f"k ± σ_k = {k:.3f} ± {sigma_k:.3f}")

# Диапазон для прямой: от 0 до чуть больше максимального n
n_line = np.linspace(0, max(n_data) * 1.1, 100)
T_line = k * n_line

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(n_line, T_line, label=f'T = ({k:.3f} ± {sigma_k:.3f}) * n', color='red', linestyle='-', linewidth=1.5)
plt.scatter(n_data, T_data, color='blue', s=30, label='Экспериментальные точки', zorder=5)

# Настройки графика
plt.xlabel('n')
plt.ylabel('T, с')
plt.title('Зависимость периода крутильных колебаний от количества шариков')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(left=0)
plt.ylim(bottom=0)

# Показать график
plt.tight_layout()
plt.savefig('T_vs_n.png', dpi=300)
plt.show()
