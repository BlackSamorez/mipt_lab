import numpy as np
from matplotlib import pyplot as plt
from math import pi

u=0    #x-position of the center
v=0    #y-position of the center
a=0.64     #radius on the x-axis
b=0.54    #radius on the y-axis

t = np.linspace(0, 2*pi, 200)
plt.plot( u+a*np.cos(t) , v+b*np.sin(t) , label=r'$Апроксимация$')
plt.xlabel(r'$OX$', fontsize=10)
plt.ylabel(r'$OZ$', fontsize=10)
plt.legend(loc='upper right', fontsize=7)
plt.grid(color='lightgray',linestyle='--', linewidth = 0.5)
plt.plot([0.64, -0.64, 0, 0], [0, 0, -0.54, 0.54], 'ro')
plt.show()
