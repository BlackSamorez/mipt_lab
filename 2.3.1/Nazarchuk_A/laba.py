import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_frame = pd.read_csv("Data.csv", sep=',')
data = {}
for i in data_frame.keys():
    data[i] = np.array(data_frame[i])
    for j in range(len(data[i])):
        try:
            data[i][j] = float(data[i][j])
        except:
            print(data[i][j])


def draw_grafic(x, y, xerr, yerr, label):
    if np.mean(xerr) != 0 or np.mean(yerr) != 0:
        yerr = list(yerr)
        if xerr == [0]:
            xerr = [0 for _ in y]
        if yerr == [0]:
            yerr = [0 for _ in y]
        plt.errorbar(x=x, y=y, yerr=yerr, xerr=xerr, label=label)
    else:
        plt.scatter(x, y, label=label)
    su = 0
    si = 0
    sy=0
    for i in range(len(x)):
        su += x[i]**2
        si += x[i]*y[i]
        sy += y[i]**2
    k = si/su
    x = np.arange(min(x)*0.9, max(x)*1.1)
    sigma = 1/len(x)**0.5*(sy/su-k**2)**0.5
    # plt.plot(x, x*k, label='Approximation')
    return k, sigma, max(x)


def find_pressure(time):
    try:
        pres_1 = data['Pressure1'][time_data.index(time)]
        pres_2 = data['Pressure2'][time_data.index(time)]
        return min(pres_1, pres_2)
    except:
        return None


start = [14, 37]
time_data = list([*data['Time']])
V_0 = 0.265
p_0 = 1000

press = []
time1 = (14-start[0])*3600+(57-start[1])*60+1
for i in range(time1, time1+60, 2):
    press.append(find_pressure(i))
p1 = max(press)
V_K =( p_0*V_0/200-V_0)
print(V_K, '+-', V_K*0.05, "объем камеры")
V_m = p_0*V_0/p1-V_0-V_K
print(V_m, '+-', V_m*0.05, " объем магистрали")

press = []
time1 = (15-start[0])*3600+(10-start[1])*60+1
for i in range(time1, time1+60, 2):
    press.append(find_pressure(i))
p1 = min(press)
V_max_1 = p_0*V_0/p1
press = []
time1 = (14-start[0])*3600+(58-start[1])*60+1
for i in range(time1, time1+60, 2):
    press.append(find_pressure(i))
p1 = min(press)
V_max_2 = p_0*V_0/p1
V_T=(V_max_1+V_max_2)/2-V_K-V_m-V_0
print(V_T, '+-', ((abs(V_max_1-V_max_2)/2/V_T)
      ** 2+(0.05)**2)**0.5, " объем ТМН")





def experiment(t, label, koef=1, long=40):
    time1 = (t[0]-start[0])*3600+(t[1]-start[1])*60+t[2]
    press = []
    time = []
    for i in range(time1, time1 + long, 2):
        po = find_pressure(i)
        if po:
            press.append(find_pressure(i))
            time.append(i)
    press = np.array(press)*koef
    press0 = press[0]
    for i in range(len(press)):
        press[i] = np.log(press[i]/press0)
    yerr = press*0.05
    time0 = time[0]
    for i in range(len(time)):
        time[i] -= time0
    k, sigma, x = draw_grafic(time, press, [0], yerr=yerr, label=label)
    return k, sigma, x


# откачка форвакуумным насосом
plt.figure(figsize=(7,7))
k1, sigma1, x1 = experiment([15, 19, 37], 'second experiment')
k2, sigma2, x2 = experiment([15, 3, 29], 'first experiment')
k = -(k1+k2)/2
x = np.arange(0, max(x1, x2))
plt.plot(x, x*(-1)*k,label="Approximation")
plt.xlabel("time, c")
plt.ylabel("ln P")
sigma_k = (sigma1**2/k1**2+0.05**2+sigma2**2/k2**2)**0.5
print(1/k,"+-",1/k*sigma_k, "tau форвакуумный")
print((V_K)*k, '+-', (V_K)*k*(sigma_k**2+0.05**2)**0.5, 'S_0 форвакуумный')
S_0_TM =(V_K)*k
print(1/(1/S_0_TM-1/(5/36)), '+-', 
      1/(1/S_0_TM-1/(5/36))*(sigma_k**2+0.05**2)**0.5, 'U форвакуумного')
plt.legend()
plt.savefig("Форвакуумный")
plt.show()


# # откачка ТМ насосом
plt.figure(figsize=(7,7))
k1, sigma1, x1 = experiment([15, 25, 47], "first experiment", 10**5)
k2, sigma2, x2 = experiment([15, 37, 33], "second experiment", 10**5)
k = -(k1+k2)/2
x = np.arange(0, max(x1, x2))
plt.plot(x, x*(-1)*k,label="Approximation")
sigma_k = (sigma1**2/k1**2+0.05**2+sigma2**2/k2**2)**0.5
print(1/k,"+-",1/k*sigma_k, "tau ТМ")
print((V_K)*k, '+-', (V_K)*k*(sigma_k**2+0.05**2)**0.5, 'S_0 TM')
S_0_TM =(V_K)*k
print(1/(1/S_0_TM-1/60), '+-', 
      1/(1/S_0_TM-1/60)*(sigma_k**2+0.05**2)**0.5, 'U TM')
plt.xlabel("time, c")
plt.ylabel("ln P")
plt.legend()
plt.savefig("ТМН")
plt.show()


# откачка ТМ насосом с диафрагмой
plt.figure(figsize=(7, 7))
# 10 mm
k, sigma, x = experiment([16, 21, 9], "10 mm", 10**5, long=70)
x=np.arange(0, x)
plt.plot(x, k*x, label='Approximation')
print(-k*V_K, '+-', -(V_K)*k*(sigma_k**2+0.05**2)**0.5, 'S_0 TM 10 mm')
print(-1/k, '+-', -1/k*((sigma/k)**2+0.05**2)**0.5, "tau TM 10 mm")
S_0_TM =-(V_K)*k
print(1/(1/S_0_TM-1/60), '+-', 
      1/(1/S_0_TM-1/60)*(sigma_k**2+0.05**2)**0.5, 'U TM 10 mm')
# 3 mm 
k, sigma, x = experiment([16, 56, 23], '3 mm', 10**5, long=100)
x=np.arange(0, x)
plt.plot(x, k*x, label='Approximation')
print(-k*V_K, '+-', -(V_K)*k*(sigma_k**2+0.05**2)**0.5, 'S_0 TM 3 mm')
print(-1/k, '+-', -1/k*((sigma/k)**2+0.05**2)**0.5, "tau TM 3 mm")
S_0_TM =-(V_K)*k
print(1/(1/S_0_TM-1/60), '+-', 
      1/(1/S_0_TM-1/60)*(sigma_k**2+0.05**2)**0.5, 'U TM 3 mm')

plt.xlabel("time, c")
plt.ylabel("ln P")

plt.legend()
plt.savefig("ТМН+диафрагма")
plt.show()


#k, sigma, x = experiment([15, 40, 1], label="", long=40)
t = [15, 41, 41]
long=70
koef=10**5
time1 = (t[0]-start[0])*3600+(t[1]-start[1])*60+t[2]
press = []
time = []
for i in range(time1, time1 + long, 2):
    po = find_pressure(i)
    
    if po:
        press.append(find_pressure(i))
        time.append(i)
        print(find_pressure(i), i)
press = np.array(press)*koef
press0 = press[0]
yerr = press*0.05
time0 = time[0]
for i in range(len(time)):
    time[i] -= time0
xlabel = "P, $\cdot 10^{-5}$ мбар"
k, sigma, x = draw_grafic(time, press, [0], yerr=yerr,
                          label="")
plt.xlabel('t, c')
plt.ylabel(xlabel)
plt.savefig("Течи")



