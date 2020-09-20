import csv
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

inp = input()


def reading():
    global U0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,k,i,v

    k = -1
    i = 0
    with open('wer/' + inp + '.txt') as f:
        for line in f:
            k = k+1
    v = [0]*k
    t1=[0]*k
    t2=[0]*k
    t3=[0]*k
    t4=[0]*k
    t5=[0]*k
    t6=[0]*k
    t7=[0]*k
    t8=[0]*k
    t9=[0]*k
    t10=[0]*k
    with open('wer/' + inp + '.txt') as f:
        f.read(90)
        for i in range (k):
            v[i] = float(f.read(2))
            f.read(1)
            t1[i]=t1[i-1]+float(f.read(5))
            f.read(1)
            t2[i]=t2[i-1]+float(f.read(5))
            f.read(1)
            t3[i]=t3[i-1]+float(f.read(5))
            f.read(1)
            t4[i]=t4[i-1]+float(f.read(5))
            f.read(1)
            t5[i]=t5[i-1]+float(f.read(5))
            f.read(1)
            t6[i]=t6[i-1]+float(f.read(5))
            f.read(1)
            t7[i]=t7[i-1]+float(f.read(5))
            f.read(1)
            t8[i]=t8[i-1]+float(f.read(5))
            f.read(1)
            t9[i]=t9[i-1]+float(f.read(5))
            f.read(1)
            t10[i]=t10[i-1]+float(f.read(5))
            f.read(1)
            #print(v[i], "&", round(t1[i], 2), "&", round(t2[i], 2), "&", round(t3[i], 2), "&", round(t4[i], 2), "&", round(t5[i], 2), "&", round(t6[i], 2), "&", round(t7[i], 2), "&", round(t8[i], 2), "&", round(t9[i], 2), "&", round(t10[i], 2), "\\\\")
            #print("\hline")

def newtable():
    global r1,r2,r3;
    r1 = [0]*k
    r2 = [0]*k
    r3 = [0]*k
    i = 0
    for i in range (k):

        r1[i] = (t1[i] + t2[i] + t3[i] + t4[i] + t5[i] + t6[i] + t7[i] + t8[i] + t9[i] + t10[i])/10
        r2[i] = math.log(20/v[i])
        
        #print( 19-i, '&', round(r1[i], 2), '&', round(r2[i], 2), '\\\\')
        #print('\hline')
        #print("(", r1[i], ",", r2[i], ")"  )
    
def calculating():
        global a,b,c,d
        a = 0
        b = 0
        c = 0
        d = 0
        for i in range (k):
            a = a + r2[i]*r1[i]
            b = b + r2[i]
            c = c + r1[i]
            d = d + r1[i]*r1[i]

        beta = (k*a-c*b)/(k*d-c*c)
        #print (r1[10]/r3[10])
        print('beta = ', beta)
        
        r = 51
        l = 38
        
        eta = (3.14*1000*9.81*0.07*r*r*r*r)/(8*beta*16*l*2.85*1000000000000)
        
        print('eta = ', eta)
        
        
def graphing():

    fig, ax = plt.subplots()
    ax.plot(r2, r1, color = 'blue', linestyle = 'None', marker='.')

    ax.set(xlabel='t(c)', ylabel='ln(U/U0)',
           title=' cерия измереиний при давлении ' + inp +  ' торр')
    ax.grid()

    fig.savefig('pic/' + inp + '.png')
    #plt.show()
    

reading()
newtable()
calculating()
graphing()


