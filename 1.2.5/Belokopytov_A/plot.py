import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("data.csv", sep=' ', decimal=',')
print(data)

def covar(x, y):
    return np.mean(x*y)-np.mean(x)*np.mean(y)

def least_squares(x, y):
    k = covar(x, y)/covar(x, x)
    b = np.mean(y)-k*np.mean(x)
    err = np.sqrt(1/(np.size(x)-2)*(covar(y,y)/covar(x,x)-k**2))
    return k, b, err


M = data['M']
Omega = data['Omega']

k, b, err = least_squares(M, Omega)
print("k:", k, "b:", b, "err:", err)
plt.axis([0, 0.42, 0, 0.210])

plt.xlabel("M, $\\text{кг}\\cdot\\text{м}^2/\\text{с}^2$")
plt.ylabel("$\\Omega, рад/c$")

plt.errorbar(M, Omega, err, 0, fmt="r^")
#plt.legend()

n_arr = np.array([0, 0.42])
line = n_arr*k+b
plt.plot(n_arr, line, color="tab:blue")

plt.show()
