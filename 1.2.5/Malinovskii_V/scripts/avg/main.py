from math import *

avg = 0
N = 0
for line in open('data', 'r'):
	x, dx = [float(x_) for x_ in line.split(' ')]
	avg += x
	N += 1

avg /= N

div = 0
div_ = 0
for line in open('data', 'r'):
	x, dx = [float(x_) for x_ in line.split(' ')]
	div += (x - avg) ** 2
	div_ += dx

div_ /= N
div = sqrt(div / (N * (N + 1)))
div = sqrt(div ** 2 + div_ ** 2)

print(avg, div)