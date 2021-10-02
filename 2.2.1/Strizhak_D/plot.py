import csv
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

inp = input()
time = input()

def reading():
    global U0,r1,r2,r3,k,i
    U0=0
    k = 0
    i = 0
    with open('wer/' + inp + '_' + time + '.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            k = k+1
            if float(row[1])>U0:
                U0 = float(row[1])
    r1=[0]*k
    r2=[0]*k
    r3=[0]*k
    with open('wer/' + inp + '_' + time + '.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r1[i] = float(row[0])
            r2[i] = float(row[1])
            r3[i] = math.log(r2[i]/U0)
            i = i + 1

def calculating():
        global a,b,c,d
        a = 0
        b = 0
        c = 0
        d = 0
        for i in range (k):
            a = a + r1[i]*r3[i]
            b = b + r1[i]
            c = c + r3[i]
            d = d + r3[i]*r3[i]

        tau = (k*a-c*b)/(k*d-c*c)
        #print (r1[10]/r3[10])
        print('tau = ', -tau)

        D = 5.3*775/(2*tau)

        print('D = ', -D)
        
def graphing():

    fig, ax = plt.subplots()
    ax.plot(r1, r3)

    ax.set(xlabel='t(c)', ylabel='ln(U/U0)',
           title=time + ' cерия измереиний при давлении ' + inp +  ' торр')
    ax.grid()

    fig.savefig('pic/' + inp + '_' + time + '.png')
    #plt.show()
    

reading()
calculating()
graphing()


