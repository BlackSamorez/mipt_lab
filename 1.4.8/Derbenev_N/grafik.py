import matplotlib
import math
import numpy as np
from statistics import mean
from matplotlib import pyplot as plt

cuh = [1,2,3,4,5,6,7,8,9,10,11]
cu = [3.2489, 6.4596,  9.7282, 12.9987, 16.2359, 19.4556, 22.6828, 25.9312, 29.1485, 32.4021, 35.6396]

duh = [1,2,3,4,5,6,7,8,9,10]
du = [4.2274, 8.4898, 12.7445, 16.9726, 21.1814, 25.3987, 29.5944, 33.8376, 38.0211, 42.3422]

sth = [1,2,3,4,5,6,7]
st = [4.1291, 8.2701, 12.3921, 16.5571, 20.6358, 24.7582, 28.8421]

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

plt.xticks(np.arange(0,12,1))

cua,cub,cusa,cusb = mnk(cuh,cu)
dua,dub,dusa,dusb = mnk(duh,du)
sta,stb,stsa,stsb = mnk(sth,st)

print(cua, cub, cusa, cusb)
print(dua, dub, dusa, dusb)
print(sta, stb, stsa, stsb)

plt.scatter(cuh,cu)
plt.scatter(duh,du)
plt.scatter(sth,st)

plt.plot([1, 11], [cua + cub * 1, cua + cub * 11])
plt.plot([1, 10], [dua + dub * 1, dua + dub * 10])
plt.plot([1, 7 ], [sta + stb * 1, sta + stb * 7])

plt.show()
