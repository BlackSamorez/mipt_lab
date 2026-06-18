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

T2x_array = T_array**2 * (xc_array-xcm+a_array)
a2_array = a_array**2

errT2x = np.sqrt(4*(0.093/20)**2/1.532**2+2**2/480**2)*np.mean(T2x_array)
erra2 = 4*0.0005

optk = (np.mean(T2x_array*a2_array)-np.mean(T2x_array)*np.mean(a2_array))/(np.mean(a2_array**2)-np.mean(a2_array)**2)
optb=np.mean(T2x_array)-optk*np.mean(a2_array)

errk = np.sqrt(1/8*((np.mean(T2x_array**2)-np.mean(T2x_array)**2)/(np.mean(a2_array**2)-np.mean(a2_array)**2)-optk**2))
errb = errk*np.sqrt(np.mean(a2_array**2))

graph_a = np.arange(0.02, 0.16, 0.01)
graph_y = graph_a*optk+optb

plt.errorbar(a2_array, T2x_array, errT2x, erra2, label="Экспериментальные значения", fmt='.')
plt.plot(graph_a, graph_y, label=f"$k=({optk:.3f}\\pm{errk:.3f}), b=({optb:.3f}\\pm{errb:.3f})$")

plt.ylabel("$T^2(x_\\text{ц}-x_\\text{ц.м.}+a)$, $c^2/\\text{м}$")
plt.xlabel("$a^2$, $\\text{м}^2$")

plt.legend()
plt.show()
