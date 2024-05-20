import numpy as np
import matplotlib.pyplot as plt

"""$N$ полосы & $0$ & $1$ & $2$ & $3$ & $4$ & $5$ & $6$ & $7$ & $8$ & $9$ & $10$ \\ \hline
$z_m$ & 324 & 356 & 388 & 420 & 452 & 484 & 516 & 548 & 580 & 612 & 644 \\ \hline"""

N = '0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10'
N = np.asarray(list(map(int, N.split('&'))))
dN = 0

z = '324 & 356 & 388 & 420 & 452 & 484 & 516 & 548 & 580 & 612 & 644'
z = np.asarray(list(map(int, z.split('&'))))
dz = 1

y = z
dy = dz
x = N
dx = dN

plt.xlabel(r'Номер полосы', fontsize=14)
plt.ylabel(r'$z_m$', fontsize=14)
plt.title(r'График калибровки компенсатора', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)

pol = np.polyfit(x, y, deg=1, cov=True)
print(pol)

k = pol[0][0]
b = pol[0][1]
dk = pol[1][0][0]
db = pol[1][1][1]

pol = pol[0]
yfit = np.polyval(pol, x)
plt.plot(x, yfit, color="firebrick", label=r'k = '+str(k)+' $\pm$ '+str(dk)+'\n'+'b = '+str(b)+' $\pm$ '+str(db))

plt.legend(loc='best', fontsize=12)
plt.show()