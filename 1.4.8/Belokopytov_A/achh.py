import numpy as np
import matplotlib.pyplot as plt

#plt.axis([3, 4, 0, 20])

nu = np.array([3.24946, 3.24982, 3.24997, 3.25005, 3.25048, 3.25065, 3.25152])
A=np.array([7, 11, 12.5, 13, 10, 8, 4])

def approx_beta(left, right, omega, cons):
    if(abs(left-right) < 0.000000001): return (left+right)/2
    try1 = (left*3+right)/4
    try2 = (left+right*3)/4
    val1 = cons/np.sqrt((omega**2-nu**2)**2+4*try1**2*nu**2)
    val2 = cons/np.sqrt((omega**2-nu**2)**2+4*try2**2*nu**2)
    err1 = np.mean((val1-nu)**2)
    err2 = np.mean((val2-nu)**2)
    mid = (left+right)/2
    if err1 < err2:
        return approx_beta(left, mid, omega, cons)
    else:
        return approx_beta(mid, right, omega, cons)

def approx_omega(left, right, betal, cons):
    if(abs(left-right) < 0.000000001): return (left+right)/2
    try1 = (left*3+right)/4
    try2 = (left+right*3)/4
    val1 = cons/np.sqrt((try1**2-nu**2)**2+4*betal**2*nu**2)
    val2 = cons/np.sqrt((try2**2-nu**2)**2+4*betal**2*nu**2)
    err1 = np.mean((val1-nu)**2)
    err2 = np.mean((val2-nu)**2)
    mid = (left+right)/2
    if err1 < err2:
        return approx_omega(left, mid, betal, cons)
    else:
        return approx_omega(mid, right, betal, cons)

def approx_const(left, right, betal, omega):
    if(abs(left-right) < 0.000000001): return (left+right)/2
    try1 = (left*3+right)/4
    try2 = (left+right*3)/4
    val1 = try1/np.sqrt((omega**2-nu**2)**2+4*betal**2*nu**2)
    val2 = try2/np.sqrt((omega**2-nu**2)**2+4*betal**2*nu**2)
    err1 = np.mean((val1-nu)**2)
    err2 = np.mean((val2-nu)**2)
    mid = (left+right)/2
    if err1 < err2:
        return approx_const(left, mid, betal, omega)
    else:
        return approx_const(mid, right, betal, omega)

A=np.array([7, 11, 12.5, 13, 10, 8, 4])
nu = np.array([3.24946, 3.24982, 3.24997, 3.25005, 3.25048, 3.25065, 3.25152])

rng = np.arange(3.24500, 3.25500, 0.00001)
#rng = np.arange(3, 4, 0.00001)

bet_temp = 0.00044
cons_temp = 0.0373711

omega = approx_omega(3.2501, 3.25014, bet_temp, cons_temp)
beta = approx_beta(0.00040, 0.00045, omega, cons_temp)
cons = approx_const(0.0373700, 0.0373800, beta, omega)
print("omega:", omega)
print("beta:", beta)
print("const:", cons)
func = cons/np.sqrt((omega**2-rng**2)**2+4*beta*beta*rng**2)

plt.errorbar(nu, A, 0, 0, fmt="bo")
plt.plot(rng, func, color='orange')
plt.show()
