import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("data2.csv", sep=' ', decimal=',')
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
#h2 = h*h

#k, b, err = least_squares(h2, I)
#print("k:", k, "b:", b, "err:", err)
#plt.axis((0, 8000, 0, 0.0105))
#h2 = h2*1e6

plt.ylabel("I, $\\text{кг}\\cdot\\text{м}^2$")
plt.xlabel("$h$, мм")

plt.errorbar(h*1000, I, 0, 0, fmt="r^")

line = np.poly1d(np.polyfit(h, data['I'], 2))
print(line)

#plt.legend()

n_arr = np.arange(0, 0.05, 0.0001)
ln = line(n_arr)
plt.plot(n_arr*1000, ln, color="tab:blue")

plt.show()
