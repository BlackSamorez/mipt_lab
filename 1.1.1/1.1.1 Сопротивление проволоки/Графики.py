
import numpy as np
import matplotlib.pyplot as plt
import math

plt.figure(figsize=(12, 6))
x20 =np.array([261.51,	351.76,	269.82,	201.19,	257.51,	329.51,	297.29,	347.21,	242.69,	215.57])
y20 = np.array([545,	735,	565,	420,	535,	690,	620,	725,	505,	450])
plt.errorbar(x20,y20,xerr=0.002*x20+0.02,yerr=3.75,linestyle='',ecolor='red',linewidth=6)
#plt.plot(x20,y20,color='red',label='l = 20 см',linewidth=0.5)
p, v = np.polyfit(x20, y20, deg=1, cov=True)
x=np.arange(min(x20),max(x20),0.01)
plt.plot(x,x*p[0]+p[1],color='red',label='l = 20 см',linewidth=1)
x = 0
y = 0
xy=0
for i in range(len(x20)):
    x+=float(x20[i])**2
    xy+=float(x20[i])*float(y20[i])
    y+=float(y20[i])**2
print(((y/x-xy**2/x**2)/10)**0.5)
print(p[0]*((3.75/max(y20))**2+((0.002*max(x20)+0.02)/max(x20))**2)**0.5)
print(((((y/x-xy**2/x**2)/10)**0.5)**2+(p[0]*((3.75/max(y20))**2+((0.002*max(x20)+0.02)/max(x20))**2)**0.5)**2)**0.5)
print(p[0]*(1+p[0]/250))
print()

x30=np.array([151.06,	179.84,	237.59,	142.59,	225.72,	143.92,	191.53,	198.91,	181.2,	169.85])
y30=np.array([460,	550,	725,	435,	690,	440,	585,	605,	555,	520])
plt.errorbar(x30,y30,xerr=0.002*x20+0.02,yerr=3.75,linestyle='',ecolor='green',linewidth=6)
p, v = np.polyfit(x30, y30, deg=1, cov=True)
x=np.arange(min(x30),max(x30),0.01)
plt.plot(x,x*p[0]+p[1],color='green',label='l = 30 см',linewidth=1)
x = 0
y = 0
xy=0
for i in range(len(x30)):
    x+=float(x30[i])**2
    xy+=float(x30[i])*float(y30[i])
    y+=float(y30[i])**2
print(((y/x-xy**2/x**2)/10)**0.5)
print(p[0]*((3.75/max(y30))**2+((0.002*max(x30)+0.02)/max(x30))**2)**0.5)
print(((((y/x-xy**2/x**2)/10)**0.5)**2+(p[0]*((3.75/max(y30))**2+((0.002*max(x30)+0.02)/max(x30))**2)**0.5)**2)**0.5)
print(p[0]*(1+p[0]/250))
print()

x50=np.array([66.34,	75.67,	88.57,	103.58,	120.84,	143.53,	148.69,	129.59,	105.21,	96.79])
y50=np.array([330,	375,	440,	515,	600,	715,	740,	645,	525,	480])
# plt.errorbar(x, y, xerr=10, yerr=20)
plt.errorbar(x50,y50,xerr=0.002*x20+0.02,yerr=3.75,linestyle='',ecolor='blue',linewidth=6)
p, v = np.polyfit(x50, y50, deg=1, cov=True)
x=np.arange(min(x50),max(x50),0.01)
plt.plot(x,x*p[0]+p[1],color='blue',label='l = 50 см',linewidth=1)
x = 0
y = 0
xy=0
for i in range(len(x50)):
    x+=float(x50[i])**2
    xy+=float(x50[i])*float(y50[i])
    y+=float(y50[i])**2
print(((y/x-xy**2/x**2)/10)**0.5)
print(p[0]*((3.75/max(y50))**2+((0.002*max(x50)+0.02)/max(x50))**2)**0.5)
print(((((y/x-xy**2/x**2)/10)**0.5)**2+(p[0]*((3.75/max(y50))**2+((0.002*max(x50)+0.02)/max(x50))**2)**0.5)**2)**0.5)
print(p[0]*(1+p[0]/250))
# plt.scatter?


plt.xlabel('I, мА')
plt.ylabel('U, мВ')
plt.legend(loc='best', fontsize=12)
plt.savefig('графики.png')

plt.show()