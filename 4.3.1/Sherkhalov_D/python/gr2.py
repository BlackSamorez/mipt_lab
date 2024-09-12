import numpy as np
import matplotlib.pyplot as plt


# $m$ & -5& -4 &-3 & -2 & -1 & 1 & 2 & 3 & 4 &5\\ \hline
# 			$ x_m $, мм  & 0.019 & 0.024 & 0.028 & 0.032 & 0.036 & 0.044 & 0.048 & 0.052 & 0.056 & 0.060\\ \hline

m = '-5 & -4 & -3 & -2 & -1 & 1 & 2 & 3 & 4 & 5'
xm = '0.019 & 0.024 & 0.028 & 0.032 & 0.036 & 0.044 & 0.048 & 0.052 & 0.056 & 0.060'
m = np.asarray(list(map(float, m.split('&'))))
xm = np.asarray(list(map(float, xm.split('&'))))

dxm = 0.01

y = xm
dy = 0
x = m
dx = 0

plt.xlabel(r'm', fontsize=14)
plt.ylabel(r'$x_{min},\, mm$', fontsize=14)
# plt.axhline(y = 0.2, color='firebrick')
# plt.title(r'', fontsize=14)
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

