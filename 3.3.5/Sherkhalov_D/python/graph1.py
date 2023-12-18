import numpy as np
import matplotlib.pyplot as plt

a = '0 & 0.19 & 0.37 & 0.56 & 0.75 & 0.94 & 1.13 & 1.28'
a = np.asarray(list(map(float, a.split('&'))))
da = 0.01

b = '0 & 252 & 455 & 678 & 940 & 1070 & 1150 & 1200'
b = np.asarray(list(map(int, b.split('&'))))
db = '0 & 5 & 10 & 10 & 50 & 50 & 50 & 50'
db = np.asarray(list(map(int, db.split('&'))))

y = b
dy = db
x = a
dx = da

plt.xlabel(r'$I_{m}$, A', fontsize=14)
plt.ylabel(r'$B$, мТл', fontsize=14)
plt.title(r'Зависимость магнитного потока от величины силы тока', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)

pol = np.polyfit(x, y, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit = np.polyval(pol, x)
plt.plot(x, yfit, color="firebrick", label=r'МНК $B(I_{m})$')

plt.legend(loc='best', fontsize=12)
plt.show()