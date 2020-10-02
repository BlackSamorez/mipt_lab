from math import *

file = open('in', 'r')
s = file.read()



for line in s.split('\n'):
	h0, a0, rot, a1, h1, t, m = [int(x) for x in line.split('\t')]
	a1 = a1 + rot * 360
	a0_ = a0
	a1_ = a1
	a0 = a0 / 180 * pi
	a1 = a1 / 180 * pi
	t = t / 10.
	dt = 0.4
	dh = 0.5
	da = 1 / 180 * pi
	l = 125.2
	dl = 0.7
	h_ = 145
	Omega = (a1 - a0) / t
	dOmega = (da * 2 / (a1 - a0) + dt / t) * Omega
	omega = (asin((h0 - h_) / l) - asin((h1 - h_) / l)) / t
	domega0 = (((h0 - h_) / l) * (2 * dh / (h0 - h_) + dl / l)) / sqrt(1 - ((h0 - h_) / l) ** 2)
	domega1 = (((h1 - h_) / l) * (2 * dh / (h1 - h_) + dl / l)) / sqrt(1 - ((h1 - h_) / l) ** 2)
	domega = ((domega0 + domega1) / (asin((h0 - h_) / l) - asin((h1 - h_) / l)) + dt / t) * omega
	print(dOmega / Omega, 0)
	#print('$' + str(m), t, h0, h1, a0_, a1_, "{0:.1f}\\pm {1:.1f}".format(1000 * Omega, 1000 * dOmega), "{0:.1f}\\pm {1:.1f}".format(1000 * omega, 1000 * domega) + '$',sep = '$ & $', end = ' \\\\\n\\hline\n')