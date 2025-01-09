import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

# Функция для аппроксимации
def model_func(x, C, y0, x0):
    return y0 - C / (x - x0)

# Метод наименьших квадратов для нахождения параметров C, y0, x0
def fit_params(x, y):
    # Начальные предположения для параметров
    x0_guess = np.mean(x)  # Убедимся, что x0 не совпадает с элементами x
    initial_guess = [100000000, 1, x0_guess]

    # Функция для вычисления остатков
    def residuals(params):
        C, y0, x0 = params
        return y - model_func(x, C, y0, x0)

    result = least_squares(residuals, initial_guess)
    return result.x

# Пример входных данных
lamda = '5401 & 5852 & 5945 & 6143 & 6402 & 4047 & 4358 & 4916 & 5461 & 5770 & 5791 & 6234 & 6907'
lamda = np.asarray(list(map(int, lamda.split('&'))))
dl = 1

theta = '1958 & 2216 & 2268 & 2360 & 2460 & 380 & 922 & 1582 & 2000 & 2184 & 2196 & 2400 & 2650'
theta = np.asarray(list(map(int, theta.split('&'))))
dt = 5

y = lamda
dy = dl
x = theta
dx = dt

# Находим параметры
C, y0, x0 = fit_params(x, y)

print(C, y0, x0)

# Генерируем значения для построения аппроксимирующей функции
x_fit = np.linspace(min(x) + 0.1, max(x) - 0.1, 100)
y_fit = model_func(x_fit, C, y0, x0)

# Построение графика
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)
plt.plot(x_fit, y_fit, color="firebrick")
plt.xlabel('$θ$, дел')
plt.ylabel('$\lambda$, Å')
plt.title('Калибровочная аппроксимация')
plt.legend(loc='best', fontsize=12)
plt.grid(True)
# plt.show()

th = np.array([2326, 2250, 1818])
la = y0 - C / (th - x0)

print(la)


