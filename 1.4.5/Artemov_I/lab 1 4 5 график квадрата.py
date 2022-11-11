import numpy as np
import matplotlib.pyplot as plt


def xi2(x,y, y_err):
    #y = a + bx
    N = len(x)
    avx = sum(x/(y_err**2))/sum(1/(y_err**2))
    avy = sum(y/(y_err**2))/sum(1/(y_err**2))
    av2x = sum(x*x/(y_err**2))/sum(1/(y_err**2))
    av2y = sum(y*y/(y_err**2))/sum(1/(y_err**2))
    R_xy = (sum(x*y/(y_err**2))/sum(1/(y_err**2))-avx*avy)
    S_x = av2x - avx**2
    S_y = av2y - avy**2
    b = R_xy/S_x
    a = avy - b * avx
    r = R_xy/(np.sqrt(S_x*S_y))
    delta_b = np.sqrt(1/(N-2)) * np.sqrt(S_y/S_x - b**2)
    delta_a = delta_b * np.sqrt(av2x)
    f = a + b * x
    xi = sum(((y-f)/y_err)**2)
    return a, b, delta_a, delta_b, xi,  r

T = np.array([10.3, 15.1, 19.9, 23.2, 28.0])
u2 = np.array([183.10, 261.0, 341.1, 396.0, 478.7])
delta_u2 = np.array([0.8, 1.0, 0.7, 0.8, 1.3])
a, b, delta_a, delta_b, xi, r = xi2(T, u2, delta_u2)
plt.errorbar(T, u2,  delta_u2, [0]*5, ls='none', fmt='o-', elinewidth=2, markersize=4, color='black', capsize=2)
plt.xlabel(r"$T$, Н")
plt.ylabel(r'$u^2, 10^{2} \cdot м^2/с^2$')
T1 = np.array([9, 10.3, 15.1, 19.9, 23.2, 28.0, 30])
u2_normal = a + b * T1
print(a)
print(b)
print(delta_a)
print(delta_b)
print(r)
print(xi/3)
plt.plot(T1, u2_normal, color='red', linewidth=1, label=r'''$u^2(T) = (11 \pm 2)\cdot 10^2 + (16.61 \pm 0.10) \cdot T$
$r = 0.99994$
$\frac{\chi^2}{d.o.f.} = 2.27$
''')
plt.grid(which='major',
        color = 'k')
plt.legend()
plt.show()