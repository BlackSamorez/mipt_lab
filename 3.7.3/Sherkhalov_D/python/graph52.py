import numpy as np
import matplotlib.pyplot as plt

Uo = '27.1 & 27.2 & 26.7 & 26.7 & 27.0 & 27.0 & 26.9 & 27.2 & 27.1 & 27.1 & 27.1 & 27.1 & 26.8 & 26.9 & 26.5'
Uo = np.asarray(list(map(float, Uo.split('&'))))
dUo = 0.1

Un = '25.2 & 24.3 & 23.6 & 23.4 & 22.9 & 22.5 & 22.0 & 21.7 & 21.4 & 21.4 & 21.1 & 20.2 & 19.7 & 19.1 & 18.5'
Un = np.asarray(list(map(float, Un.split('&'))))
dUn = 0.1

phi = '4.62 & 7.52 & 11.5 & 13.74 & 16.81 & 19.86 & 22.94 & 25.96 & 29.04 & 36.66 & 42.79 & 48.93 & 55.01 & 61.13 & 67.30'
phi = np.asarray(list(map(float, phi.split('&'))))
dphi = 0.01

nu = '1 & 3 & 5 & 7 & 9 & 11 & 13 & 15 & 17 & 20 & 24 & 28 & 32 & 36 & 40'
nu = np.asarray(list(map(float, nu.split('&'))))
nu = nu*1000000
dnu = 0.01*1000000

alpha = np.log(Uo/Un)/5010
da = 0
da = da / 5010
kappa = phi/5010
dk = kappa/5010

#print(alpha)
#print(kappa)

y = alpha*kappa
dy = da
x = nu*np.sqrt(nu)
dx = 1.5*np.sqrt(nu)*dnu

plt.xlabel(r'$x_3,\, s^{-\frac{3}{2}}$, ', fontsize=14)
plt.ylabel(r'$y_3,\, cm^{-2}$', fontsize=14)
plt.title(r'$y_3(x_3)$', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)

pol = np.polyfit(x, y, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit = np.polyval(pol, x)
plt.plot(x, yfit, color="firebrick", label=r'МНК $y_3(x_3)$')

plt.legend(loc='best', fontsize=12)
plt.show()