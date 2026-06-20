import matplotlib.pyplot as plt
import numpy as np

l = 1
g = 9.789
mct = 870.6
mpr = 72.3
xcm = 0.501

xc_array = np.array([0.470,0.474,0.478,0.479,0.480,0.481,0.481,0.482,0.483,0.485])
a_array = np.array([0.376,0.324,0.281,0.268,0.254,0.245,0.235,0.224,0.212,0.193])
T_array = np.array([1.565,1.539,1.532,1.534,1.535,1.538,1.545,1.553,1.569,1.594])
a_array_teor = np.arange(0.17, 0.4, 0.001)
T_array_teor_easy = 2*np.pi*np.sqrt((l**1/12+a_array_teor**2)/(g*a_array_teor))
T_array_teor = 2*np.pi*np.sqrt((l**1/12+a_array**2)/(g*(1+mpr/mct)*(xc_array-xcm+a_array)))

plt.errorbar(a_array, T_array, 0.093/20, 0.0005, label="Фактические значения T")
plt.plot(a_array, T_array_teor, label="Теоретическая зависимость T(a) с учётом призмы")
plt.plot(a_array_teor, T_array_teor_easy, label="Теоретическая зависимость T(a) без учёта призмы")

def calc_T(use_g, use_a, use_xc):
    return 2*np.pi*np.sqrt((l**1/12+use_a**2)/(use_g*(1+mpr/mct)*(use_xc-xcm+use_a)))

def approx_g(left, right):
    try1 = (3*left+right)/4
    try2 = (left+3*right)/4
    xi1 = np.sum(((calc_T(try1, a_array, xc_array)-T_array)/(0.039/30))**2)
    xi2 = np.sum(((calc_T(try2, a_array, xc_array)-T_array)/(0.039/30))**2)
    if right-left < 0.0001:
        print("Hi", xi1/9, xi2/9)
        return (right+left)/2
    if xi1 < xi2:
        return approx_g(left, (left+right)/2)
    else:
        return approx_g((left+right)/2, right)

def approx_a(left, right):
    try1 = (3*left+right)/4
    try2 = (left+3*right)/4
    val1 = 2*np.pi*np.sqrt((l**1/12+try1**2)/(g*try1))
    val2 = 2*np.pi*np.sqrt((l**1/12+try2**2)/(g*try2))
    if right-left < 0.0001:
        print("T:", val1, val2)
        return (right+left)/2
    if val1 < val2:
        return approx_a(left, (left+right)/2)
    else:
        return approx_a((left+right)/2, right)

app_g = approx_g(9, 15)
app_a = approx_a(0.100, 0.400)
print("g", app_g)
print("a", app_a)

T_array_teor_approx = calc_T(app_g, a_array, xc_array)
plt.plot(a_array, T_array_teor_approx, label="Аппроксимация")

plt.ylabel("T, c")
plt.xlabel("a, м")

plt.legend()
plt.show()
