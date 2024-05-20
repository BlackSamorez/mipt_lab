import numpy as np
import matplotlib.pyplot as plt
"""		$0$   & $480$  &  $300$ & $180$  \\ \hline
		$20$  & $744$  &  $187$ & $557$  \\ \hline
		$40$  & $1100$ &   $48$ & $1052$  \\ \hline
		$60$  & $1500$ & $-150$ & $1650$  \\ \hline
		$80$  & $1600$ & $-180$ & $1780$  \\ \hline
		$100$ & $1500$ & $-150$ & $1650$  \\ \hline
		$120$ & $1000$ &  $100$ & $900$  \\ \hline
		$140$ & $670$  &  $250$ & $420$  \\ \hline
		$160$ & $450$  &  $305$ & $145$  \\ \hline
		$180$ & $480$  &  $300$ & $180$  \\ \hline
		$200$ & $750$  &  $150$ & $600$  \\ \hline
		$220$ & $1100$ &  $-10$ & $1110$  \\ \hline
		$240$ & $1400$ & $-150$ & $1550$  \\ \hline
		$260$ & $1500$ & $-180$ & $1680$  \\ \hline
		$280$ & $1400$ & $-140$ & $1540$  \\ \hline
		$300$ & $1100$ &   $50$ & $1050$  \\ \hline
		$320$ & $750$  &  $270$ & $480$  \\ \hline
		$340$ & $500$  &  $345$ & $155$  \\ \hline"""
fi = '0 & 20 & 40 & 60 & 80 & 100 & 120 & 140 & 160 & 180 & 200 & 220 & 240 & 260 & 280 & 300 & 320 & 340'
fi = np.asarray(list(map(int, fi.split('&'))))
dfi = 2

i = '180 & 557 & 1052 & 1650 & 1780 & 1650 & 900 & 420 & 145 & 180 &600 & 1110 & 1550 & 1680 & 1540 & 1050 & 480 & 155'
i = np.asarray(list(map(int, i.split('&'))))
di = 50

y = i
dy = di
x = fi
dx = dfi

plt.xlabel(r'$\theta$, $^{\circ}$', fontsize=14)
plt.ylabel(r'$\Delta I$, мкВ', fontsize=14)
plt.title(r'зависимость интенсивности излучения от угла поворота поляроида', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='o', color='black', capsize=3)
plt.plot(x, y, color="firebrick", label=r'$\Delta I(\theta)$')

plt.legend(loc='best', fontsize=12)
plt.show()