import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as m
import scipy.special

fig1 = plt.figure()

tps = 1193180
T0 = 1.517869454426
sz = 0.005948819506

def elliptic(x):
    print(x)
    a0 = 1/m.sqrt(2-x**2)
    b0 = m.sqrt(2-a0**2)
    while True:
        a1 = (a0+b0)/2
        b1 = m.sqrt(a0*b0)
        if(abs(a0-a1) < 0.001 and abs(b0-b1) < 0.001):
            print(1/m.sqrt(2-x**2)/a1)
            return 1/m.sqrt(2-x**2)/a1
        else:
            a0 = a1
            b0 = b1

data = pd.read_csv("exp6.csv")
dT = data["dT"]/tps
dTs = np.roll(dT, -1);

#ampl = 180/np.pi*2*np.asin(sz/dT/2)
ampl = 180/np.pi*2*np.asin(np.sqrt((sz/dT+sz/dTs)**2/16))

plt.axis((0, 185, 1.0, 4))
plt.grid(visible=True)
plt.errorbar(ampl, data["T"]/tps, 0, 0, fmt="r^")

teor_x = np.arange(0, 179, 1)
teor_y = T0*teor_x #(1+(teor_x/140*np.pi/4)**2+11/12*(teor_x/140*np.pi/4)**4)

plt.xlabel("Амплитуда, градусы");
plt.ylabel("Период колебаний, сек");
plt.yticks(np.arange(1.0, 4.25, 0.25))

for i in range(teor_y.size):
    #teor_y[i] = T0*elliptic(m.sin(float(teor_x[i]/180*m.pi)/2)**2)
    teor_y[i] = T0*2/np.pi*scipy.special.ellipk(m.sin(float(teor_x[i]/180*m.pi)/2)**2)
    print(teor_y[i])

plt.plot(teor_x, teor_y)
plt.savefig("plot6.pdf")

fig2 = plt.figure()

plt.axis((0, 185, -0.05, 0.05))
plt.xlabel("Амплитуда, градусы");
plt.ylabel("Отклоненение между теорией и измерениями, сек");
plt.yticks(np.arange(-0.05, 0.05, 0.01))

ter2_y = T0*2/np.pi*scipy.special.ellipk(np.sin(ampl/180*np.pi/2)**2)
plt.errorbar(ampl, data["T"]/tps-ter2_y, 0, 0, fmt="yo", markersize=1)
plt.savefig("plot6_1.pdf")

print(data)
plt.show()
