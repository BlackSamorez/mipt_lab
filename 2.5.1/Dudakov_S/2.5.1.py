import numpy as np
import pandas as pd
import matplotlib 
from matplotlib import pyplot as plt

dataset_df = pd.read_csv(filepath_or_buffer='2.5.1_data.csv', sep=',')

x = np.array(dataset_df['t'])
y1 = np.array(dataset_df['s'])
y2 = x * 0.155
y3 = y1 + 0.155*x

def modded_plot(x, y, label):
    z = np.linspace(min(x), max(x), 1000)
    k, b = np.polyfit(x, y, deg=1)
    plt.plot(z, k * z + b, label=label)
    print(k, b)
    plt.xlabel("T, °С")

modded_plot(x, y1, "σ(T)")
modded_plot(x, y2, "q(T)")
modded_plot(x, y3, "U/П(T)")

plt.errorbar(dataset_df['t'], dataset_df['s'], yerr=dataset_df['ds'], fmt='g.')
plt.errorbar(dataset_df['t'], dataset_df['q'], yerr=dataset_df['dq'], fmt='g.')
plt.errorbar(dataset_df['t'], dataset_df['u'], yerr=dataset_df['du'],fmt='g.')

plt.grid()
plt.legend()
plt.savefig("all.png")
plt.show()