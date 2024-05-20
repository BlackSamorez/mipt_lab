import numpy as np
import matplotlib.pyplot as plt

"""\textnumero & 
      $R^{\text{up}}_{1}$ мм & 
              $R^{\text{dn}}_{1}$ мм & 
                        $R^{\text{up}}_{2}$ мм & 
                                $R^{\text{dn}}_{2}$ мм &
                                          $D_{1}$ мм &
                                                $D_{2}$ мм &
                                                        $D_{\text{ср}}$ мм \\ \hline
  1 & 160.88 & 147.86 & 162.15 & 146.73 & 13.02 & 15.42 & 14.22 \\ \hline
  2 & 164.45 & 144.58 & 165.22 & 143.78 & 19.87 & 21.44 & 20.66 \\ \hline
  3 & 166.88 & 142.13 & 167.58 & 141.44 & 24.75 & 26.14 & 25.45 \\ \hline
  4 & 168.94 & 140.08 & 169.58 & 139.45 & 28.86 & 30.13 & 29.50 \\ \hline
  5 & 170.81 & 138.27 & 171.39 & 137.74 & 32.54 & 33.65 & 33.10 \\ \hline
  6 & 172.54 & 136.63 & 173.00 & 136.07 & 35.91 & 36.93 & 36.42 \\ \hline"""

D1 = '13.02 & 19.87 & 24.75 & 28.86 & 32.54 & 35.91'
D2 = '15.42 & 21.44 & 26.14 & 30.13 & 33.65 & 36.93'
Ds = '14.22 & 20.66 & 25.45 & 29.50 & 33.10 & 36.42'
D1 = np.asarray(list(map(float, D1.split('&'))))
D2 = np.asarray(list(map(float, D2.split('&'))))
Ds = np.asarray(list(map(float, Ds.split('&'))))
dD = D2 - D1
dd = 0.02

n = '1 & 2 & 3 & 4 & 5 & 6'
n = np.asarray(list(map(int, n.split('&'))))
dn = 0

y = Ds
dy = dd
x = 1/dD
dx = dd/dD**2

plt.xlabel(r'$\dfrac{1}{\Delta D},\, mm^{-1}$', fontsize=14)
plt.ylabel(r'$D_{ср},\, mm$', fontsize=14)
plt.title(r'График для дублета, натриевая лампа', fontsize=14)
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