import matplotlib as mpl
import matplotlib.pyplot as plt
import math
def picture():
    dpi = 80
    fig = plt.figure(dpi = dpi, figsize = (1024 / dpi, 576 / dpi) )
    mpl.rcParams.update({'font.size': 10})

    
    x1 = [0]*13
    y1 = [0]*13
    
    
    x1[1], x1[2], x1[3], x1[4], x1[5], x1[6], x1[7], x1[8], x1[9], x1[10] = 238.4 , 238.5, 238.6, 238.7, 238.8, 238.85, 238.9, 239.0, 239.1, 239.2
    y1[1], y1[2], y1[3], y1[4], y1[5], y1[6], y1[7], y1[8], y1[9], y1[10] = 1, 1.5 , 2.5, 4, 7, 8, 4, 2, 1.5, 1
   

    plt.axis([238, 239.5, 0, 10])


    plt.title('Амплитудно-частотная характеристика')
    plt.xlabel('v')
    plt.ylabel('А')


    plt.plot(x1, y1, color = 'blue', linestyle = 'solid', label = '')
  

    plt.legend(loc = 'upper left')
    fig.savefig('task1.png')

picture()
