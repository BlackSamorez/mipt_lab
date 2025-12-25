import matplotlib.pyplot as plt
import numpy as np

# Ваши данные
n_data = np.array([12, 10, 8, 6, 4])
M_data = np.array([285.45589086, 227.01610218, 214.091918145, 191.0531553, 179.252813355])

# Аппроксимация M = k * n (линейная регрессия без intercept)
k = np.sum(n_data * M_data) / np.sum(n_data**2)
print(f"k = {k:.3f}")

# Погрешность k
N = len(n_data)
residuals = M_data - k * n_data
chi2 = np.sum(residuals**2)
sigma_k = np.sqrt(chi2 / (np.sum(n_data**2) * (N - 1)))

print(f"σ_k = {sigma_k:.3f}")
print(f"k ± σ_k = {k:.3f} ± {sigma_k:.3f}")

# Диапазон для прямой: от 0 до чуть больше максимального n
n_line = np.linspace(0, max(n_data) * 1.1, 100)
M_line = k * n_line

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(n_line, M_line, label=f'M = ({k:.3f} ± {sigma_k:.3f}) * n', color='red', linestyle='-', linewidth=1.5)
plt.scatter(n_data, M_data, color='blue', s=30, label='Экспериментальные точки', zorder=5)

# Настройки графика
plt.xlabel('n')
plt.ylabel('M, дин*см')
plt.title('Зависимость момента сил от количества шариков')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(left=0)
plt.ylim(bottom=0)

# Показать график
plt.tight_layout()
plt.savefig('M_vs_n.png', dpi=300)
plt.show()
