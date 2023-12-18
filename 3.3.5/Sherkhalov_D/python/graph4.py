import numpy as np
import matplotlib.pyplot as plt

"""
1 & 0.19 & 0.01 &  190 & 11 & 7 & 140 & 10 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 19 & 380 & 10 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 30 & 600 & 10 \\ \hline
4 & 0.74 & 0.01 &  739 & 15 & 40 & 800 & 10 \\ \hline
5 & 0.93 & 0.01 &  929 & 17 & 47 & 940 & 10 \\ \hline
6 & 1.16 & 0.01 & 1159 & 18 & 51 & 1020 & 10 \\ \hline
7 & 1.25 & 0.01 & 1249 & 19 & 52 & 1040 & 10 \\ \hline
"""

b = '190 & 370 & 559 & 739 & 929 & 1159 & 1249'
b = np.asarray(list(map(float, b.split('&'))))
db = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db = np.asarray(list(map(float, db.split('&'))))

u = '140 & 380 & 600 & 800 & 940 & 1020 & 1040'
u = np.asarray(list(map(float, u.split('&'))))
u = u - 60
du = 10

y = u
dy = 2*du
x = b 
dx = db 

plt.xlabel(r'$В$, мТл', fontsize=14)
plt.ylabel(r'$\varepsilon_x$, нВ', fontsize=14)
plt.title(r'Зависимость ЭДС Холла от величины силы тока в серебре', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)

pol = np.polyfit(x, y, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit = np.polyval(pol, x)
plt.plot(x, yfit, color="firebrick", label=r'МНК $\varepsilon_x(B)$ при $I = 1.00$ А')

plt.legend(loc='best', fontsize=12)
plt.show()