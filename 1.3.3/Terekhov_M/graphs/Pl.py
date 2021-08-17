import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
import math
plt.rcParams.update({'font.size': 22})
name = "Pl"
data = pd.read_csv(name + ".csv", names=["l", "P"])
K = 0.2
data["P1"] = 9.80665 * K * data["P"]
X = data["l"].values
sigma_X = 0.4
Y = data["P"].values
sigma_Y = 0.7
A = np.vstack([X[1:], np.ones(len(X[1:]))]).T
k, b = np.linalg.lstsq(A, Y[1:], rcond=None)[0]
fig = plt.figure(figsize=(12, 7))
ax = fig.gca()
plt.scatter(X, Y, marker=".")
plt.errorbar(X, Y, xerr=sigma_X, yerr=sigma_Y, linestyle="None")
delta_x = (X.max() - X.min()) / len(X)
delta_y = (Y.max() - Y.min()) / len(Y)
ax.set_xlim(X.min() - delta_x/2, X.max() + delta_x/2)
ax.set_ylim((Y.min() - delta_y/2), Y.max() + delta_y/2)
plt.xlabel("$l, мм$")
plt.ylabel("$P, 10^{-3} Па$")
plt.plot(X, (k*X + b), 'r', label='Fitted line')
plt.grid(True)
plt.savefig("./" + name + ".png")
