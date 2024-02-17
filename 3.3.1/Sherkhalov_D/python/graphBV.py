import numpy as np
import matplotlib.pyplot as plt

v = '70 & 80 & 90 & 100 & 110'
v = np.asarray(list(map(int, v.split('&'))))
dv = 2

b = '4.5 & 4.8 & 5.0 & 5.3 & 5.6'
b = np.asarray(list(map(float, b.split('&'))))
db = 0.1

y = v
dy = dv
x = b**2
dx = 2*b*db

plt.ylabel(r'$V$, В', fontsize=14)
plt.xlabel(r'$B_{кр}$, мТл$^2$', fontsize=14)
plt.title(r'$V$ от $B_{кр}^2$', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)
pol = np.polyfit(x, y, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit = np.polyval(pol, x)
plt.plot(x, yfit, color="firebrick", label=r'МНК $V$ от $B_{кр}^2$')

plt.legend(loc='best', fontsize=12)
plt.show()