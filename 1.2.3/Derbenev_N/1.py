h = [0, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045, 0.050]
T1 = [3.094, 3.098, 3.116, 3.142, 3.188, 3.226, 3.296, 3.370, 3.444, 3.550, 3.634]
T2 = [3.012, 3.020, 3.040, 3.068, 3.104, 3.164, 3.222, 3.298, 3.382, 3.466, 3.562]
m = 1.336

I0 = 0.00711
k = 0.0004
m0 = 0.9347

I1 = []
I2 = []
h2 = []

for i in range(0, len(h)):
    I1.append(k*(m+m0)*(T1[i]**2) - I0)
    I2.append(k*(m+m0)*(T2[i]**2) - I0)
    h2.append(h[i]**2)
	
import matplotlib
import math
import numpy as np
from statistics import mean
from matplotlib import pyplot as plt

def mnk(x, y):
    xy = []
    xx = []
    yy = []
    for i in range(0, len(x)):
        xy.append(x[i]*y[i])
        xx.append(x[i]**2)
        yy.append(y[i]**2)

    b = (mean(xy)-mean(x)*mean(y))/(mean(xx)-mean(x)**2)
    a = mean(y) - b * mean(x)

    sb = 1/math.sqrt(len(x))*math.sqrt((mean(yy)-mean(y)**2)/(mean(xx)-mean(x)**2)-b**2)
    sa = sb * math.sqrt(mean(xx)-mean(x)**2)

    return a,b,sa,sb

a,b,sa,sb = mnk(h2, I1)
plt.plot([0, 0.05**2], [a, a + b * 0.05**2])
print("I1: ", I1)

print("a =", a)
print("b =", b)
print("sa =", sa)
print("sb =", sb)

a,b,sa,sb = mnk(h2, I2)
plt.plot([0, 0.05**2], [a, a + b * 0.05**2])
print("I2: ", I1)

print("a =", a)
print("b =", b)
print("sa =", sa)
print("sb =", sb)

plt.xlabel("h²")
plt.ylabel("I")


plt.scatter(h2, I1)
plt.scatter(h2, I2)
plt.show()
