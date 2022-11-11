import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def xi2(x,y, y_err):
    #y = a + bx
    N = len(x)
    avx = sum(x/y_err)/N
    avy = sum(y/y_err)/N
    av2x = sum(x*x/y_err)/N
    av2y = sum(y*y/y_err)/N
    R_xy = (sum(x*y/y_err)/N-avx*avy)
    S_x = av2x - avx**2
    S_y = av2y - avy**2
    b = R_xy/S_x
    a = avy - b * avx
    r = R_xy/(S_x*S_y)
    delta_b = np.sqrt(1/(N-2)) * np.sqrt(S_y/S_x - b**2)
    delta_a = delta_b * np.sqrt(av2x)
    f = a + b * x
    xi = sum(((y-f)/y_err)**2)
    return a, b, delta_a, delta_b, xi, r


df = pd.read_csv("lab 1 4 5.csv", encoding="utf-8", sep=";")
n = df.iloc[:, [0]]
nu_1 = df.iloc[:, [1]]
nu_1_list = np.array((nu_1["nu"]))

x = np.array(range(1, 11))
print(x)
plt.plot(x, nu_1_list, color="black", marker='o', ls="none", markersize= 4.5)
plt.xlabel("n")
plt.ylabel(r"$\nu_n(n), Гц$")
print(x)
print(nu_1_list)
res = xi2(x, nu_1_list, np.array([1]*10))
plt.plot([0, 11], [res[0], res[0] + res[1]*11], color="black", label=r"$\nu_n = (-7.2 \pm 1.9) + (138.1 \pm 0.3) \cdot n$", linewidth=0.8)
print(res)


nu_1 = df.iloc[:, [2]]
nu_1_list = np.array((nu_1["nu.1"]))

x = np.array(range(1, 11))
print(x)
plt.plot(x, nu_1_list, color="red", marker='o', ls="none", markersize= 4.5)
plt.xlabel("n")
plt.ylabel(r"$\nu_n(n), Гц$")
print(x)
print(nu_1_list)
res = xi2(x, nu_1_list, np.array([1]*10))
plt.plot([0, 11], [res[0], res[0] + res[1]*11], color="red", label=r"$\nu_n = (-6.0 \pm 1.8) + (164.9 \pm 0.3) \cdot n$",linewidth=0.8)
print(res)


nu_1 = df.iloc[:, [3]]
nu_1_list = np.array((nu_1["nu.2"]))

x = np.array(range(1, 11))
print(x)
plt.plot(x, nu_1_list, color="grey", marker='o', ls="none", markersize= 4.5)
plt.xlabel("n")
plt.ylabel(r"$\nu_n(n), Гц$")
print(x)
print(nu_1_list)
res = xi2(x, nu_1_list, np.array([1]*10))
plt.plot([0, 11], [res[0], res[0] + res[1]*11], color="grey", label=r"$\nu_n = (-2.5 \pm 0.7) + (188.48 \pm 0.11) \cdot n$",linewidth=0.8)
print(res)


nu_1 = df.iloc[:, [4]]
nu_1_list = np.array((nu_1["nu.3"]))

x = np.array(range(1, 11))
print(x)
plt.plot(x, nu_1_list, color="green", marker='o', ls="none", markersize= 4.5)
plt.xlabel("n")
plt.ylabel(r"$\nu_n(n), Гц$")
print(x)
print(nu_1_list)
res = xi2(x, nu_1_list, np.array([1]*10))
plt.plot([0, 11], [res[0], res[0] + res[1]*11], color="green", label=r"$\nu_n = (-2.1 \pm 0.8) + (203.08 \pm 0.13) \cdot n$",linewidth=0.8)
print(res)


nu_1 = df.iloc[:, [5]]
nu_1_list = np.array((nu_1["nu.4"]))

x = np.array(range(1, 11))
print(x)
plt.plot(x, nu_1_list, color="darkblue", marker='o', ls="none", markersize= 4.5)
plt.xlabel("n")
plt.ylabel(r"$\nu_n(n), Гц$")
print(x)
print(nu_1_list)
res = xi2(x, nu_1_list, np.array([1]*10))
plt.plot([0, 11], [res[0], res[0] + res[1]*11], color="darkblue", label=r"$\nu_n = (-2.1 \pm 1.0) + (223.29 \pm 0.16) \cdot n$",linewidth=0.8)
print(res)


plt.legend()
plt.grid(which='major',
        color = 'k')
plt.show()
