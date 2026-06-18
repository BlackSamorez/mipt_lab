import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def least_squares(x, y):
    coeff = np.mean(x*y) / np.mean(x*x)
    err = 1 / np.sqrt(len(x)) * np.sqrt((y*y).mean() / (x*x).mean() - coeff ** 2)
    return coeff, err

def least_squares_reversed(y, x):
    coeff = np.mean(x*y) / np.mean(x*x)
    err = 1 / np.sqrt(len(x)) * np.sqrt((y*y).mean() / (x*x).mean() - coeff ** 2)
    return coeff, err

cm20_data = pd.read_csv("20cm_data.csv", sep=' ', decimal=',')
cm30_data = pd.read_csv("30cm_data.csv", sep=' ', decimal=',')
cm50_data = pd.read_csv("50cm_data.csv", sep=' ', decimal=',')

print(cm20_data)
print(cm30_data)
print(cm50_data)

err_U = 4.5
err_I = 0.3

k20, err20 = least_squares_reversed(cm20_data['U'], cm20_data['I'])
k30, err30 = least_squares_reversed(cm30_data['U'], cm30_data['I'])
k50, err50 = least_squares_reversed(cm50_data['U'], cm50_data['I'])

print(k20, err20)
print(k30, err30)
print(k50, err50)

k20, err20 = least_squares(cm20_data['U'], cm20_data['I'])
k30, err30 = least_squares(cm30_data['U'], cm30_data['I'])
k50, err50 = least_squares(cm50_data['U'], cm50_data['I'])

plt.axis([0, 800, 0, 250])
plt.minorticks_on()
plt.ylabel("$I$, мА")
plt.xlabel("$U$, мВ")

plt.errorbar(cm20_data['U'], cm20_data['I'], err_I, err_U, fmt='bo', label="$l=20$ см,\n$R=2,0167\\ \\pm\\ 0,0019$ Ом", markersize=4)
plt.errorbar(cm30_data['U'], cm30_data['I'], err_I, err_U, fmt='r^', label="$l=30$ см,\n$R=2,9655\\ \\pm\\ 0,0019$ Ом", markersize=4)
plt.errorbar(cm50_data['U'], cm50_data['I'], err_I, err_U, fmt='cd', label="$l=50$ см,\n$R=4,9765\\ \\pm\\ 0,0018$ Ом", markersize=4)

cm20_data.loc[-1] = [0, 0]
plt.plot(cm20_data['U'], cm20_data['U']*k20, color="tab:blue")
cm30_data.loc[-1] = [0, 0]
plt.plot(cm30_data['U'], cm30_data['U']*k30, color="tab:red")
cm50_data.loc[-1] = [0, 0]
plt.plot(cm50_data['U'], cm50_data['U']*k50, color="tab:cyan")

plt.legend()
plt.show()
