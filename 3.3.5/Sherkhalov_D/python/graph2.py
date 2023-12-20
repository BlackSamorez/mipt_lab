import numpy as np
import matplotlib.pyplot as plt

I = np.array([0.20, 0.35, 0.50, 0.65, 0.80, 0.95, 1.10, 1.25])

"""
1 & 0.19 & 0.01 &  190 & 11 & 11 & 440 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 12 & 480 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 14 & 560 & 20 \\ \hline
4 & 0.75 & 0.01 &  749 & 15 & 15 & 600 & 20 \\ \hline
5 & 0.94 & 0.01 &  939 & 17 & 16 & 640 & 20 \\ \hline
6 & 1.13 & 0.01 & 1129 & 18 & 16 & 640 & 20 \\ \hline
7 & 1.28 & 0.01 & 1279 & 19 & 16 & 640 & 20 \\ \hline
"""

b1 = '190 & 370 & 559 & 749 & 939 & 1129 & 1279'
b1 = np.asarray(list(map(int, b1.split('&'))))
db1 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db1 = np.asarray(list(map(int, db1.split('&'))))

u1 = '440 & 480 & 560 & 600 & 640 & 640 & 640'
u1 = np.asarray(list(map(int, u1.split('&'))))
du = 20
u1 = u1 + 11000/25

"""
1 & 0.19 & 0.01 &  190 & 11 & 12 & 480 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 14 & 560 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 16 & 640 & 20 \\ \hline
4 & 0.75 & 0.01 &  749 & 15 & 18 & 720 & 20 \\ \hline
5 & 0.94 & 0.01 &  939 & 17 & 19 & 760 & 20 \\ \hline
6 & 1.13 & 0.01 & 1129 & 18 & 20 & 800 & 20 \\ \hline
7 & 1.26 & 0.01 & 1259 & 19 & 21 & 840 & 20 \\ \hline
"""

b2 = '190 & 370 & 559 & 749 & 939 & 1129 & 1259'
b2 = np.asarray(list(map(int, b2.split('&'))))
db2 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db2 = np.asarray(list(map(int, db2.split('&'))))

u2 = '480 & 560 & 640 & 720 & 760 & 800 & 840'
u2 = np.asarray(list(map(int, u2.split('&'))))
u2 = u2 + 10000/25

"""
1 & 0.19 & 0.01 &  190 & 11 & 14.5 & 580 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 18 & 720 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 21 & 840 & 20 \\ \hline
4 & 0.75 & 0.01 &  749 & 15 & 24 & 960 & 20 \\ \hline
5 & 0.94 & 0.01 &  939 & 17 & 26 & 1040 & 20 \\ \hline
6 & 1.13 & 0.01 & 1129 & 18 & 27 & 1080 & 20 \\ \hline
7 & 1.26 & 0.01 & 1259 & 19 & 28 & 1120 & 20 \\ \hline
"""

b3 = '190 & 370 & 559 & 749 & 939 & 1129 & 1259'
b3 = np.asarray(list(map(int, b3.split('&'))))
db3 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db3 = np.asarray(list(map(int, db3.split('&'))))

u3 = '580 & 720 & 840 & 960 & 1040 & 1080 & 1120'
u3 = np.asarray(list(map(int, u3.split('&'))))
u3 = u3 + 10000/25

"""
1 & 0.19 & 0.01 &  190 & 11 & 15.5 & 620 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 19 & 760 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 24 & 960 & 20 \\ \hline
4 & 0.75 & 0.01 &  749 & 15 & 28 & 1120 & 20 \\ \hline
5 & 0.94 & 0.01 &  939 & 17 & 30 & 1200 & 20 \\ \hline
6 & 1.13 & 0.01 & 1129 & 18 & 32 & 1280 & 20 \\ \hline
7 & 1.26 & 0.01 & 1259 & 19 & 33 & 1320 & 20 \\ \hline
"""

b4 = '190 & 370 & 559 & 749 & 939 & 1129 & 1259'
b4 = np.asarray(list(map(int, b4.split('&'))))
db4 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db4 = np.asarray(list(map(int, db4.split('&'))))

u4 = '620 & 760 & 960 & 1120 & 1200 & 1280 & 1320'
u4 = np.asarray(list(map(int, u4.split('&'))))
u4 = u4 + 11000/25

"""
1 & 0.19 & 0.01 &  190 & 11 & 17 & 680 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 23 & 920 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 28 & 1120 & 20 \\ \hline
4 & 0.75 & 0.01 &  749 & 15 & 32 & 1280 & 20 \\ \hline
5 & 0.94 & 0.01 &  939 & 17 & 36 & 1440 & 20 \\ \hline
6 & 1.16 & 0.01 & 1159 & 18 & 38 & 1520 & 20 \\ \hline
7 & 1.26 & 0.01 & 1259 & 19 & 39 & 1560 & 20 \\ \hline
"""

b5 = '190 & 370 & 559 & 749 & 939 & 1159 & 1259'
b5 = np.asarray(list(map(int, b5.split('&'))))
db5 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db5 = np.asarray(list(map(int, db5.split('&'))))

u5 = '680 & 920 & 1120 & 1280 & 1440 & 1520 & 1560'
u5 = np.asarray(list(map(int, u5.split('&'))))
u5 = u5 + 12000/25

"""
1 & 0.19 & 0.01 &  190 & 11 & 19 & 760 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 25 & 1000 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 32 & 1280 & 20 \\ \hline
4 & 0.74 & 0.01 &  739 & 15 & 38 & 1520 & 20 \\ \hline
5 & 0.94 & 0.01 &  939 & 17 & 42 & 1680 & 20 \\ \hline
6 & 1.16 & 0.01 & 1159 & 18 & 45 & 1800 & 20 \\ \hline
7 & 1.25 & 0.01 & 1249 & 19 & 46 & 1840 & 20 \\ \hline
"""

b6 = '190 & 370 & 559 & 739 & 939 & 1159 & 1249'
b6 = np.asarray(list(map(int, b6.split('&'))))
db6 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db6 = np.asarray(list(map(int, db6.split('&'))))

u6 = '760 & 1000 & 1280 & 1520 & 1680 & 1800 & 1840'
u6 = np.asarray(list(map(int, u6.split('&'))))
u6 = u6 + 13000/25

"""
1 & 0.19 & 0.01 &  190 & 11 & 21 & 840 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 28 & 1120 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 36 & 1440 & 20 \\ \hline
4 & 0.74 & 0.01 &  739 & 15 & 43 & 1720 & 20 \\ \hline
5 & 0.94 & 0.01 &  939 & 17 & 47 & 1880 & 20 \\ \hline
6 & 1.16 & 0.01 & 1159 & 18 & 50 & 2000 & 20 \\ \hline
7 & 1.25 & 0.01 & 1249 & 19 & 51 & 2040 & 20 \\ \hline
"""

b7 = '190 & 370 & 559 & 739 & 939 & 1159 & 1249'
b7 = np.asarray(list(map(int, b7.split('&'))))
db7 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db7 = np.asarray(list(map(int, db7.split('&'))))

u7 = '840 & 1120 & 1440 & 1720 & 1880 & 2000 & 2040'
u7 = np.asarray(list(map(int, u7.split('&'))))
u7 = u7 + 14000/25

"""
1 & 0.19 & 0.01 &  190 & 11 & 23 & 920 & 20 \\ \hline
2 & 0.37 & 0.01 &  370 & 13 & 32 & 1280 & 20 \\ \hline
3 & 0.56 & 0.01 &  559 & 14 & 41 & 1640 & 20 \\ \hline
4 & 0.75 & 0.01 &  749 & 15 & 49 & 1960 & 20 \\ \hline
5 & 0.93 & 0.01 &  929 & 17 & 53 & 2120 & 20 \\ \hline
6 & 1.14 & 0.01 & 1139 & 18 & 57 & 2280 & 20 \\ \hline
7 & 1.24 & 0.01 & 1239 & 19 & 58 & 2320 & 20 \\ \hline
"""

b8 = '190 & 370 & 559 & 749 & 929 & 1139 & 1239'
b8 = np.asarray(list(map(int, b8.split('&'))))
db8 = '11 & 13 & 14 & 15 & 17 & 18 & 19'
db8 = np.asarray(list(map(int, db8.split('&'))))

u8 = '920 & 1280 & 1640 & 1960 & 2120 & 2280 & 2320'
u8 = np.asarray(list(map(int, u8.split('&'))))
u8 = u8 + 15000/25


plt.xlabel(r'$В$, мТл', fontsize=14)
plt.ylabel(r'$\varepsilon_x$, нВ', fontsize=14)
plt.title(r'Зависимость ЭДС Холла от величины силы тока в меди', fontsize=14)
plt.grid(True)

plt.errorbar(b1, u1, xerr=db1, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b1, u1, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit1 = np.polyval(pol, b1)
plt.plot(b1, yfit1, color="firebrick", label=r'МНК $\varepsilon_x(B)$ при $I = 0.20$ А')

plt.errorbar(b2, u2, xerr=db2, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b2, u2, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit2 = np.polyval(pol, b2)
plt.plot(b2, yfit2, color="darkorange", label=r'МНК $\varepsilon_x(B)$ при $I = 0.35$ А')

plt.errorbar(b3, u3, xerr=db3, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b3, u3, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit3 = np.polyval(pol, b3)
plt.plot(b3, yfit3, color="goldenrod", label=r'МНК $\varepsilon_x(B)$ при $I = 0.50$ А')

plt.errorbar(b4, u4, xerr=db4, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b4, u4, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit4 = np.polyval(pol, b4)
plt.plot(b4, yfit4, color="darkgreen", label=r'МНК $\varepsilon_x(B)$ при $I = 0.65$ А')

plt.errorbar(b5, u5, xerr=db5, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b5, u5, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit5 = np.polyval(pol, b5)
plt.plot(b5, yfit5, color="c", label=r'МНК $\varepsilon_x(B)$ при $I = 0.80$ А')

plt.errorbar(b6, u6, xerr=db6, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b6, u6, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit6 = np.polyval(pol, b6)
plt.plot(b6, yfit6, color="dodgerblue", label=r'МНК $\varepsilon_x(B)$ при $I = 0.95$ А')

plt.errorbar(b7, u7, xerr=db7, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b7, u7, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit7 = np.polyval(pol, b7)
plt.plot(b7, yfit7, color="navy", label=r'МНК $\varepsilon_x(B)$ при $I = 1.10$ А')

plt.errorbar(b8, u8, xerr=db8, yerr=2*du, fmt='o', color='black', capsize=3)
pol = np.polyfit(b8, u8, deg=1, cov=True)
print(pol)
pol = pol[0]
yfit8 = np.polyval(pol, b8)
plt.plot(b8, yfit8, color="darkmagenta", label=r'МНК $\varepsilon_x(B)$ при $I = 1.25$ А')


plt.legend(loc='best', fontsize=12)
plt.show()