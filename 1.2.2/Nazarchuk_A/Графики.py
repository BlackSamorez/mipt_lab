
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(9, 6))
m_dop = np.array([0, 0, 0, 0, 0, 0, 6.21, 9.07, 45, 62,
                 51.5, 100, 103.55, 8.95, 64.2, 106])
b_0 = np.array([0.188, 0.1814, -0.228, 0.1758, 0.1846, 0.1837, 0.2607,
               0.3008, 0.7118, 0.95, 0.7811, 0.7065, 0.7288, 0.136, 0.4785, 0.7382])
b_err = np.array([0.00077, 0.0093, 0.001, 0.0022, 0.00099, 0.0015, 0.0024,
                 0.0016, 0.0027, 0.002, 0.0074, 0.0019, 0.0023, 0.002, 0.0029, 0.0026])
r = np.array([1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75,
             1.75, 1.75, 1.75, 0.9, 0.9, 0.9, 0.9, 0.9])
m_osn = 17.05
m = (m_dop + m_osn) / 1000
r /= 100


M_N = m * r * (9.81 - b_0 * r)
for i in range(len(b_0)):
    if b_0[i] < 0:
        M_N[i] *= -1
M_N_err = ((b_err/b_0)**2 + 4*(0.05/100/r)**2)**0.5*M_N*1000
p = np.polyfit(M_N*1000, b_0, 1)
x = np.arange(min(M_N*1000), max(M_N*1000), 0.001)

plt.scatter(M_N*1000, b_0, label='Экспериментальные точки')
plt.errorbar(M_N*1000, b_0, yerr=b_err, xerr=M_N_err, linestyle='')
plt.ylabel(r"$\beta_0, {рад}/c^2$")
plt.xlabel(r"$M_T, мН \cdot м$")
plt.plot(x, p[0]*x+p[1], label='Аппроксимация')
plt.grid(True)
plt.legend()




N = len(b_0)
xy_sr = sum(M_N*b_0)/N
x_sr = sum(M_N)/N
y_sr = sum(b_0)/N
x2_sr = sum(M_N**2)/N
y2_sr=sum(b_0**2)/N
p[0] = (xy_sr-x_sr*y_sr)/(x2_sr-x_sr**2)
p[1] = y_sr-p[0]*x_sr
M_0 = -p[1]/p[0] / 1000
p_0_err =1/N**0.5*((y2_sr-y_sr**2)/(x2_sr-x_sr**2)-p[0]**2)**0.5
p_1_err = p_0_err*(x2_sr-x_sr**2)**0.5
M_0_err = ((p_0_err/p[0])**2 + (p_1_err/p[1])**2)**0.5*M_0
print('M_0 =', M_0*1000, 'мН', '$\pm$', M_0_err*1000)
print('I =', 1/p[0], 'Н*м', '$\pm$', p_0_err/p[0]**2)
plt.savefig('beta(M)')
plt.show()


plt.figure(figsize=(7, 5))
mgr = np.array([155.5, 148.9, 151.9, 150.1]) / 1000
R = np.array([[7.2, 7.8, 7.8, 8.3], [11.9, 11.6, 12, 12], [3.1, 3.3, 2.4, 2.6], [4.6, 5.6, 4.6, 4.7], [
             7.2, 7.8, 7.8, 8.3], [11.9, 11.6, 12, 12], [3.1, 3.3, 2.4, 2.6], [4.6, 5.6, 4.6, 4.7]])
R /= 100
m = (m_osn+100) / 1000
b_0 = (np.array([1.587, 1.026, 2.501, 2.081, 0.8113, 0.504, 1.294, 1.071]))
b_err = np.array([0.0072, 0.0036, 0.0053, 0.0085,
                 0.0066, 0.013, 0.0071, 0.001])
r = np.array([1.75, 1.75, 1.75, 1.75, 0.9, 0.9, 0.9, 0.9]) / 100
mr2 = []
mr2_err = []
for i in range(len(R)):
    s = 0
    err = 0
    for j in range(4):
        s += mgr[j]*R[i][j]**2
        err += (0.05/100/R[i][j])**2+(0.1/1000/mgr[j])**2
    mr2.append(s)
    mr2_err.append(err**0.5)
mr2 = np.array(mr2)
I = (m*9.81*r-M_0)/b_0 - m*r**2


mr2_err = m*r**2*((0.1/1000/m)**2+4*(0.05/100/r)**2)**0.5
M_0b_0_err = ((M_0_err/M_0)**2+(b_err/b_0)**2)**0.5*M_0/b_0
mrb_err = ((0.1/1000/m)**2+(b_err/b_0)**2+(0.05/100/r)**2)**0.5*m*r*9.81/b_0
I_err = (mrb_err**2+mr2_err**2+M_0b_0_err**2)**0.5
print(I_err)
b_0 = I
M_N = mr2
N = len(b_0)
xy_sr = sum(M_N*b_0)/N
x_sr = sum(M_N)/N
y_sr = sum(b_0)/N
x2_sr = sum(M_N**2)/N
y2_sr=sum(b_0**2)/N
p[0] = (xy_sr-x_sr*y_sr)/(x2_sr-x_sr**2)
p[1] = y_sr-p[0]*x_sr
M_0 = -p[1]/p[0] / 1000
p_0_err =1/N**0.5*((y2_sr-y_sr**2)/(x2_sr-x_sr**2)-p[0]**2)**0.5
p_1_err = p_0_err*(x2_sr-x_sr**2)**0.5
print(p[1], p_1_err*1000)
# plt.errorbar(mr2, I, xerr=mr2_err, yerr=I_err*1000, linestyle='', linewidth=3, label='Экспериментальные данные')
# plt.scatter(mr2, I)
# x = np.arange(min(mr2), max(mr2), 0.01)
# plt.plot(x, v[0]*x+v[1], label='Аппроксимация')
# plt.xlabel('$\sum_i m_iR_i^2, г\cdot м^2$')
# plt.ylabel('$I,  г\cdot м^2$')
# plt.grid(True)
# plt.legend()


# plt.savefig('I(mr2)')




