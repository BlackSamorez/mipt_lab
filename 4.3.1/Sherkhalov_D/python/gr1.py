import numpy as np
import matplotlib.pyplot as plt

# """			$ x_n $, мм  & $ z_n $, мм & $ n $& $ 2\xi_n $, мм& $ \sigma_{2\xi_n} $, мм\\
# 			\hline
# 			536 &	12	&	1   & 0.16  & 0.01
# 			\\ \hline
# 			540	&	8	&	2   & 0.19  & 0.01
# 			\\ \hline
# 			543	&	5	&	3   & 0.18  & 0.01
# 			\\ \hline
# 			545	& 	3	&	4   & 0.16  & 0.01
# 			\\ \hline
# 			546	&	2	&	5   & 0.15  & 0.01"""

n = '1 & 2 & 3 & 4 & 5'
ks = '0.16 & 0.19 & 0.18 & 0.16 & 0.15'
n = np.asarray(list(map(float, n.split('&'))))
ks = np.asarray(list(map(float, ks.split('&'))))

dks = 0.01

y = ks
dy = dks
x = n
dx = 0

plt.xlabel(r'n', fontsize=14)
plt.ylabel(r'$2 \xi_n,\, mm$', fontsize=14)
plt.axhline(y = 0.2, color='firebrick')
# plt.title(r'', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)

# pol = np.polyfit(x, y, deg=1, cov=True)
# print(pol)

# k = pol[0][0]
# b = pol[0][1]
# dk = pol[1][0][0]
# db = pol[1][1][1]

# pol = pol[0]
# yfit = np.polyval(pol, x)
# plt.plot(x, yfit, color="darkgreen", label=r'k = '+str(k)+' $\pm$ '+str(dk)+'\n'+'b = '+str(b)+' $\pm$ '+str(db))

plt.legend(loc='best', fontsize=12)
plt.show()

