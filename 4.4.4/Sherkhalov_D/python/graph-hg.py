import numpy as np
import matplotlib.pyplot as plt

"""\textnumero & 
      $R^{up}_{ylw}$ мм & 
              $R^{dn}_{ylw}$ мм & 
                        $R^{up}_{grn}$ мм & 
                                $R^{dn}_{grn}$ мм &
                                          $D_{ylw}$ мм &
                                                $D_{grn}$ мм &
                                                        $D_{avg}$ мм \\ \hline
  1 & 177.10 & 169.65 & 179.06 & 167.49 &  7.45 & 11.58 & 14.22 \\ \hline
  2 & 180.83 & 165.70 & 181.90 & 164.62 & 15.13 & 17.29 & 20.66 \\ \hline
  3 & 183.26 & 163.26 & 183.93 & 162.55 & 20.00 & 21.39 & 25.45 \\ \hline
  4 & 185.15 & 161.31 & 185.62 & 160.83 & 23.84 & 24.79 & 29.50 \\ \hline
  5 & 186.74 & 159.70 & 187.04 & 159.33 & 28.04 & 27.71 & 33.10 \\ \hline
  6 & 188.17 & 158.25 & 188.44 & 157.98 & 29.93 & 30.46 & 36.42 \\ \hline"""

Dg = '11.58 & 17.29 & 21.39 & 24.79 & 27.71 & 30.46'
Dy = '7.45 & 15.13 & 20.00 & 23.84 & 27.04 & 29.92'
Dg = np.asarray(list(map(float, Dg.split('&'))))
Dy = np.asarray(list(map(float, Dy.split('&'))))

dd = 0.02

n = '1 & 2 & 3 & 4 & 5 & 6'
n = np.asarray(list(map(int, n.split('&'))))
dn = 0

y = Dy**2
dy = 2*Dy*dd
x = n
dx = 0

plt.xlabel(r'Номер кольца n', fontsize=14)
plt.ylabel(r'$D_n^{2},\, mm^{2}$', fontsize=14)
plt.title(r'График квадрата диаметра жёлтых колец, ртутная лампа', fontsize=14)
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
plt.plot(x, yfit, color="darkgreen", label=r'k = '+str(k)+' $\pm$ '+str(dk)+'\n'+'b = '+str(b)+' $\pm$ '+str(db))

plt.legend(loc='best', fontsize=12)
plt.show()