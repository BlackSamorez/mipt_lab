import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def factorial(array):
    return np.array([math.gamma(val+1) for val in array])

geiger_data = pd.read_csv("exp_data.txt")
print(geiger_data)

np_data = np.array(geiger_data)
sum10 = np.sum(np.reshape(np_data, (-1, 10)), 1)
sum20 = np.sum(np.reshape(np_data, (-1, 20)), 1)
sum40 = np.sum(np.reshape(np_data, (-1, 40)), 1)
print(sum10)
print(sum20)
print(sum40)

fig, ax1 = plt.subplots()

ax2 = ax1.twiny()
ax3 = ax1.twiny()


midn = np.mean(sum10)
print("Среднее значение n10:", midn)
midn20 = np.mean(sum20)
print("Среднее значение n20:", midn20)
midn40 = np.mean(sum40)
print("Среднее значение n40:", midn40)

err = np.sqrt(np.mean((sum10-midn)**2))
print("Среднеквадратичная ошибка:", err)
err = np.sqrt(np.mean((sum20-midn20)**2))
print("Среднеквадратичная ошибка:", err)
err = np.sqrt(np.mean((sum40-midn40)**2))
print("Среднеквадратичная ошибка:", err)

x_values = np.arange(0, 20, 0.1)
puasson = (np.exp(-midn))*(midn**x_values)/(factorial(x_values))

midn = 10.0023
md = 2.3714
gauss = 1/np.sqrt(2*np.pi)/md*np.exp(-((x_values-midn)/2/md)**2)

ax1.plot(x_values, puasson, label="Распределение Пуассона", color='orange')
ax1.plot(x_values, gauss, label="Распределение Гаусса", color='purple')

ax1.hist(sum10, histtype='bar', bins=range(0, 21, 1), density=True, label="10 c")
ax1.set_xticks(range(0, 21, 5))

ax2.hist(sum20, histtype='bar', alpha=0.3, bins=range(0, 41, 1), density=True,
color='yellow', label="20 c")
ax2.set_xticks(range(0, 41, 5))

ax2.tick_params(axis='x', which='major', pad=20)

ax3.hist(sum40, histtype='step', bins=range(0, 81, 1), density=True,
color='magenta', label="40 c")
ax3.set_xticks(range(0, 81, 10))





lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.set_xlabel('Число отсчетов')
ax1.set_ylabel('Доля случаев')

ax1.legend(lines1+lines2+lines3, labels1+labels2+labels3)

plt.show()

hist, nums = np.histogram(sum10, bins=19, density=True)

nums = np.array(range(1, 20))
print(hist, nums)

def puasson_apporox(left, right):
    if abs(left-right) < 0.00001:
        tr = (left+right)/2
        xi2 = 400*np.sum(((np.exp(-tr))*(tr**nums)/(factorial(nums))-hist)**2/((np.exp(-tr))*(tr**nums)/(factorial(nums))))
        print("Hi puasson:", xi2/19)
        return (left+right)/2
        #return (left+right)/2
    try1 = (3*left+right)/4
    try2 = (left+3*right)/4
    #print(try1, try2)
    err1 = np.sqrt(np.mean(((np.exp(-try1))*(try1**nums)/(factorial(nums))-hist)**2))
    err2 = np.sqrt(np.mean(((np.exp(-try2))*(try2**nums)/(factorial(nums))-hist)**2))
    #print("Puasson", err1, err2)
    if err1 < err2:
        return puasson_apporox(left, (left+right)/2);
    else:
        return puasson_apporox((left+right)/2, right);

def gauss_apporox2(left, right, n):
    if abs(left-right) < 0.00001:
        tr = (left+right)/2
        xi2 = 400*np.sum((np.exp(-((nums-n)/(2*tr))**2)*1/np.sqrt(2*np.pi)/tr-hist)**2/(np.exp(-((nums-n)/(2*tr))**2)*1/np.sqrt(2*np.pi)/tr))
        print("Hi gauss:", xi2/18)
        return (left+right)/2
    try1 = (3*left+right)/4
    try2 = (left+3*right)/4
    err1 = 20*np.sum((np.exp(-((nums-n)/(2*try1))**2)*1/np.sqrt(2*np.pi)/try1-hist)**2/(np.exp(-((nums-n)/(2*try1))**2)*1/np.sqrt(2*np.pi)/try1))
    err2 = 20*np.sum((np.exp(-((nums-n)/(2*try2))**2)*1/np.sqrt(2*np.pi)/try2-hist)**2/(np.exp(-((nums-n)/(2*try2))**2)*1/np.sqrt(2*np.pi)/try2))
    #print("Gauss:", err1, err2)
    if err1 < err2:
        return gauss_apporox2(left, (left+right)/2, n);
    else:
        return gauss_apporox2((left+right)/2, right, n);


def gauss_apporox(left, right):
    if abs(left-right) < 0.00001:
        tr = (left+right)/2
        xi2 = 400*np.sum((np.exp(-((nums-tr)/(2*np.sqrt(tr)))**2)*1/np.sqrt(2*np.pi*tr)-hist)**2/(np.exp(-((nums-tr)/(2*np.sqrt(tr)))**2)*1/np.sqrt(2*np.pi*tr)))
        print("Hi gauss:", xi2/18)
        return (left+right)/2, gauss_apporox2(np.sqrt(tr)/2, 3*np.sqrt(tr)/2, tr)
    try1 = (3*left+right)/4
    try2 = (left+3*right)/4
    err1 = 20*np.sum((np.exp(-((nums-try1)/(2*np.sqrt(try1)))**2)*1/np.sqrt(2*np.pi*try1)-hist)**2/(np.exp(-((nums-try1)/(2*np.sqrt(try1)))**2)*1/np.sqrt(2*np.pi*try1)))
    err2 = 20*np.sum((np.exp(-((nums-try2)/(2*np.sqrt(try2)))**2)*1/np.sqrt(2*np.pi*try2)-hist)**2/(np.exp(-((nums-try2)/(2*np.sqrt(try2)))**2)*1/np.sqrt(2*np.pi*try2)))
    #print("Gauss:", err1, err2)
    if err1 < err2:
        return gauss_apporox(left, (left+right)/2);
    else:
        return gauss_apporox((left+right)/2, right);

print(puasson_apporox(5, 15))
print(np.sqrt(puasson_apporox(5, 15)))
print(gauss_apporox(5, 15))
