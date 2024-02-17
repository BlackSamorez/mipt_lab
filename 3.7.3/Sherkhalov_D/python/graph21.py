import numpy as np
import matplotlib.pyplot as plt

a = '3.85 & 7.70 & 11.55 & 15.5 & 19.4 & 23.3 & 27.2 & 31.1'
a = np.asarray(list(map(float, a.split('&'))))
da = 0.1

b = '1    & 2    & 3     & 4    & 5    & 6    & 7    & 8'
b = np.asarray(list(map(int, b.split('&'))))
db = 0

y = a
dy = da
x = b
dx = db

plt.xlabel(r'$n$', fontsize=14)
plt.ylabel(r'$\nu$, МГц', fontsize=14)
plt.title(r'Cинусоидальный сигнал, согласованная линия', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)

pol = np.polyfit(x, y, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit = np.polyval(pol, x)
plt.plot(x, yfit, color="firebrick", label=r'МНК $\nu(n)$')

plt.legend(loc='best', fontsize=12)
plt.show()