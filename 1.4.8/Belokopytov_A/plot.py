import matplotlib.pyplot as plt
import numpy as np

def covar(x, y):
    return np.mean(x*y)-np.mean(x)*np.mean(y)

def least_squares(x, y):
    k = covar(x, y)/covar(x, x)
    b = np.mean(y)-k*np.mean(x)
    err = np.sqrt(1/(np.size(x)-2)*(covar(y,y)/covar(x,x)-k**2))
    return k, b, err


n_arr = np.array([1, 2, 3, 4, 5])
n_arr3 = np.array([1, 2, 3, 4, 5, 6])

med_arr = np.array([3.25036, 6.52380, 9.77440, 13.0104, 16.2111, 19.5236])
stal_arr = np.array([4.13445, 8.26542, 12.4090, 16.5400, 20.6663])
dural_arr = np.array([4.23545, 8.48988, 12.7159, 16.9546, 21.1703])
stal2_arr = np.array([6.44012, 12.8794, 19.3221, 25.7673, 32.1998])

med_k, med_b, med_err = least_squares(n_arr3, med_arr)
stal_k, stal_b, stal_err = least_squares(n_arr, stal_arr)
dural_k, dural_b, dural_err = least_squares(n_arr, dural_arr)
stal2_k, stal2_b, stal2_err = least_squares(n_arr, stal2_arr)

print("med:", med_k, med_b, med_err)
print("stal:", stal_k, stal_b, stal_err)
print("dural:", dural_k, dural_b, dural_err)
print("stal2:", stal2_k, stal2_b, stal2_err)

plt.axis([0, 7, 0, 35])
plt.ylabel("$\\nu$, кГц")
n_arr2 = np.array([0, 7])
med_line = n_arr2*med_k+med_b
stal_line = n_arr2*stal_k+stal_b
dural_line = n_arr2*dural_k+dural_b
stal2_line = n_arr2*stal2_k+stal2_b

plt.errorbar(n_arr3, med_arr, med_err, 0, label=f"Медь, k={med_k:.3f}, b={med_b:.3f}, err={med_err:.3f}", fmt="bo", markersize=5)
plt.errorbar(n_arr, stal_arr, stal_err, 0, label=f"Сталь (большой стержень), k={stal_k:.3f}, b={stal_b:.3f}, err={stal_err:.3f}", fmt="r^", markersize=5)
plt.errorbar(n_arr, dural_arr, dural_err, 0, label=f"Дюралюминий, k={dural_k:.3f}, b={dural_b:.3f}, err={dural_err:.3f}", fmt="cd", markersize=5)
plt.errorbar(n_arr, stal2_arr, stal2_err, 0, label=f"Сталь (маленький стержень), k={stal2_k:.3f}, b={stal2_b:.3f}, err={stal2_err:.3f}", fmt="mv", markersize=5)
plt.legend()

plt.plot(n_arr2, med_line, color="tab:blue")
plt.plot(n_arr2, stal_line, color="tab:red")
plt.plot(n_arr2, dural_line, color="tab:cyan")
plt.plot(n_arr2, stal2_line, color="tab:purple")

plt.show()
