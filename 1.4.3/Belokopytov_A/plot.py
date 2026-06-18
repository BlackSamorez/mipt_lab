import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as m

def elliptic(x):
    print(x)
    a0 = 1/m.sqrt(2-x**2)
    b0 = m.sqrt(1-a0**2)
    while True:
        a1 = (a0+b0)/2
        b1 = m.sqrt(a0*b0)
        if(abs(a0-a1) < 0.001 and abs(b0-b1) < 0.001):
            print(1/m.sqrt(2-x**2)/a1)
            return 1/m.sqrt(2-x**2)/a1
        else:
            a0 = a1
            b0 = b1

data = pd.read_csv("exp1_proc.csv", decimal=',')

plt.axis((0, 180, 0, 3))
plt.errorbar(data["A"], data["T"], 0, 0, fmt="r^")

teor_x = np.arange(0, 160, 1)
teor_y = 1.325*teor_x #(1+(teor_x/140*np.pi/4)**2+11/12*(teor_x/140*np.pi/4)**4)

for i in range(teor_y.size):
    teor_y[i] = 1.32525*elliptic(m.sin(float(teor_x[i]/160*m.pi)/2)**2)
    print(teor_y[i])

plt.plot(teor_x, teor_y)

print(data)
plt.show()
