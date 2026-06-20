import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

data = pd.read_csv("data.csv", sep=' ', decimal=',')
print(data)

def covar(x, y):
    return np.mean(x*y)-np.mean(x)*np.mean(y)

def least_squares(x, y):
    k = covar(x, y)/covar(x, x)
    b = np.mean(y)-k*np.mean(x)
    err = np.sqrt(1/(np.size(x)-2)*(covar(y,y)/covar(x,x)-k**2))
    return k, b, err


h = data['h']
I = data['I']

h = h/1000
h2 = h*h

k, b, err = least_squares(h2, I)
print("k:", k, "b:", b, "err:", err)
plt.axis((0, 8000, 0, 0.0105))
h2 = h2*1e6

plt.ylabel("I, $\\text{кг}\\cdot\\text{м}^2$")
plt.xlabel("$h^2$, мм")

plt.errorbar(h2, I, 0.0001*2*math.sqrt(2), 0, fmt="r^")
#plt.legend()

n_arr = np.array([0, 8000])
line = n_arr/1e6*k+b
plt.plot(n_arr, line, color="tab:blue")

plt.show()
