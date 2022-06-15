
import numpy as np
import matplotlib.pyplot as plt
# # import math

# # plt.figure(figsize=(10, 6))
# # a=np.array([25.20, 20.00, 13.30, 10.40, 7.40, 4.50, 37.20, 44.70, 22.00, 23.30, 23.50, 24.40])
# # t=np.array([1.54, 1.59, 1.75, 1.93, 2.22, 2.80, 1.56, 1.60, 1.56, 1.54, 1.55, 1.54])
# # # plt.errorbar(t,a,xerr=0,yerr=0,linestyle='',ecolor='red',linewidth=6)
# # for i in range(len(a)):
# #     for j in range(i+1,len(a)):
# #         if a[j]<a[i]:
# #             a[i],a[j]=a[j],a[i]
# #             t[i],t[j]=t[j],t[i]
# # # 
# # # plt.plot(a,t,'g', label = 'T(a)')
# # i=1.53
# # I=np.array([i for _ in (a)])    
# # # plt.plot(a,I,'b', linestyle='--')
# # # p, v = np.polyfit(x20, y20, deg=1, cov=True)
# # # x=np.arange(min(x20),max(x20),0.01)
# # # plt.plot(x,x*p[0]+p[1],color='red',label=.'l = 20 см',linewidth=1)
# # a/=100
# # # print(a)
# # u = t**2*a/4/math.pi**2
# # v= a**2+1/12
# # plt.errorbar(u,v,xerr=(2*0.1/100+0.5/100/a)*u,yerr=2*0.5/100/a*v,linestyle='')
# # # plt.plot(u,v,'go', label = 'T(a)')
# # p,q=np.polyfit(u,v,deg=1,cov=True)
# # x=np.arange(min(u),max(u),0.01)
# # plt.plot(x,x*p[0]+p[1],color='red',linewidth=1)

# # uerr=sum((2*0.1/100+0.5/100/a))/12
# # verr=sum(2*0.5/100/a)/12
# # sist=uerr+verr
# # A=float(sum(u**2))
# # T=float(sum(v**2))
# # k = float(sum(u*v))/A
# # sigma=(1/12**0.5*(T/A-k**2)**0.5)
# # print((sist**2+sigma**2/k**2)**0.5)
# # print(uerr + verr)

# # # idx = np.argwhere(np.diff(np.sign(f - g))).flatten()

# # # plt.xlabel('a, cм')
# # # plt.ylabel('T, c')
# # # # plt.legend(loc='best', fontsize=12)
# # plt.savefig('u(v).png')

# # plt.show()


# from scipy.optimize import curve_fit #function for fitting data with a curve
# import numpy as np #work with arrays and linear algebra
# import matplotlib.pyplot as plt #plot diagrams
# #Fitting function with its argument a and two parameters
# def fit_func(a, Tmin, a0):
#     return Tmin*np.sqrt((np.square(a)+a0**2)/2/a/a0)


# # Data
# z = np.linspace(1, 50, 10000)
# a = [25.20, 20.00, 13.30, 10.40, 7.40, 4.50, 37.20, 44.70, 22.00, 23.30, 23.50, 24.40]
# T = [1.54, 1.59, 1.75, 1.93, 2.22, 2.80, 1.56, 1.60, 1.56, 1.54, 1.55, 1.54]
# # Fitting procedure returning params values and covariation matrix.
# #Consumes fitting function, data and initial parameters values
# params, cov = curve_fit(fit_func, a, T, p0 = [30, 1.5])
# #create figure where to draw plots
# plt.figure(figsize=(8,5))
# #define titles and axis limits
# plt.title("Зависимость периода колебаний от расстояния до центра масс")
# a = np.array(a)
# T = np.array(T)
# plt.errorbar(a,T,xerr=0.5, yerr=0.5/100*T,label='T(a)',color='green', linestyle='', linewidth=5)
# plt.ylabel("T, s")
# plt.xlabel("a, cm")
# plt.ylim(1.0, 4.0) #limit on T axis
# #plot fitting function
# plt.plot(z, fit_func(z, params[0], params[1]))
# #print parameter values and their errors
# # print("T_min ="+ str(round(params[0], 3))+ "+-"+
# # str(round(np.sqrt(cov[0][0]), 3))+" s")
# # print("a_0 = "+str(round(params[1], 3))+"+-"+
# # str(round(np.sqrt(cov[1][1]), 3))+" cm")
# #show figure while running script interactively




# #save figure
# plt.savefig("T(a)+fun.png")
# plt.show()





m=np.array([57, 92, 92, 92, 92, 92, 116, 142, 180, 219, 273, 341, 74])
om = np.array([0.034522996, 0.057119866, 0.056605273, 0.056861405, 0.057643902, 0.056861405, 0.072220521, 0.087672353, 0.112199738, 0.135413476, 0.169054313, 0.212989332, 0.046370371])
plt.scatter(om*1000, m)
plt.show()