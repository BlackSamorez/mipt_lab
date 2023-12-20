import numpy as np
a = '78 & 77 & 76 & 76 & 75 & 30 &	16 & 8 & 4 & 3 & 2 & 2 & 2 & 1 & 1 & 0 & 0'
a = np.asarray(list(map(int, a.split('&'))))
a = a*4
a = a.astype("str")
a = list(a)
a = ' & '.join(a)
print(a)

m = '35 & 36 & 37 &	38 & 39 & 40 & 41 & 42 & 43 & 44 & 45 & 46 & 47 & 48 & 49 & 50 & 51'
m = np.asarray(list(map(int, m.split('&'))))
m = m*4
b = m*3.5*10**(-2)
m = m.astype("str")
m = list(m)
m = ' & '.join(m)
print(m)
b = b.astype("str")
b = list(b)
b = ' & '.join(b)
print(b)

