import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

dataset_df = pd.read_csv(filepath_or_buffer='data2.1.6.csv', sep=',')

x = np.array(dataset_df['p'])
y1 = abs(np.array(dataset_df['u17']))/40.2/(10**(-6))*10**(-3)
y2 = abs(np.array(dataset_df['u25']))/40.6/(10**(-6))*10**(-3)
y3 = abs(np.array(dataset_df['u35']))/41.6/(10**(-6))*10**(-3)
y4 = abs(np.array(dataset_df['u50']))/42.3/(10**(-6))*10**(-3)

def modded_plot(x, y):
    z = np.linspace(min(x), max(x), 1000)
    k, b = np.polyfit(x, y, deg=1)
    plt.plot(z, k * z + b)
    print(k, b)
    plt.ylabel("μ, К/бар")
    plt.xlabel("T, °С")
    return k

#modded_plot(x, y1)
#modded_plot(x, y2)
#modded_plot(x, y3)
#modded_plot(x, y4)
modded_plot([17, 25, 35, 50], [1.124, 1.053, 0.995, 0.933])

#plt.errorbar(x, y1, xerr=0.1, yerr=0.1, fmt='g.')
#plt.errorbar(x, y2, xerr=0.1, yerr=0.1, fmt='y.')
#plt.errorbar(x, y3, xerr=0.1, yerr=0.1,  fmt='b.')
#plt.errorbar(x, y4, xerr=0.1, yerr=0.1, fmt='r.')
plt.errorbar([17, 25, 35, 50], [1.124, 1.053, 0.995, 0.933], fmt="b.")

plt.grid()
plt.legend()
plt.savefig("mt.png")
plt.show()