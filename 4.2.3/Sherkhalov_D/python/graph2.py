import numpy as np
import matplotlib.pyplot as plt

"""$P$, кПа & $0$ & $-1$ & $-2$ & $-3$ & $-4$ & $-5$ & $-6$ & $-7$ \\ \hline
        $z$ & 319 & 332 & 346 & 360 & 369 & 388 & 400 & 412 \\ \hline   
    \end{tabular}
    \begin{tabular}{|*{10}{l|}} \hline
        $P$, кПа & $1$ & $2$ & $3$ & $4$ & $5$ & $6$ & $7$ & $8$ \\ \hline
        $z$ & 304 & 296 & 273 & 259 & 246 & 231 & 218 & 203 \\ \hline """
P = '-7 & -6 & -5 & -4 & -3 & -2 & -1 & 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8'
P = np.asarray(list(map(int, P.split('&'))))
dP = 0.1

z = '412 & 400 & 388 & 369 & 360 & 346 & 332 & 319 & 304 & 296 & 273 & 259 & 246 & 231 & 218 & 203'
z = np.asarray(list(map(int, z.split('&'))))
dz = 1

y = z
dy = dz
x = -P
dx = dP

plt.xlabel(r'P, кПа', fontsize=14)
plt.ylabel(r'$z$', fontsize=14)
plt.title(r'Зависимость показаний микрометра от давления', fontsize=14)
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
# plt.savefig("graph2.png")
# plt.clf()
