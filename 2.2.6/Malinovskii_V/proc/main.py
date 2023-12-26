from math import *

with open('data') as file:
	s = file.read()

for line in s.split('\n'):
	steel, T0, T1, d0, d1, t0, t1 = [float(_) for _ in line.split('\t')]
	T = (T0 + T1) / 2
	dT = 0.2
	dd = 0.03
	d = d0 / 1000
	steel = (steel == 1.0)
	rho = 7700 if steel else 2600
	с = 1930 

	eta = 2 / 9. * 9.8 * d ** 2 / 4 * (rho - 1250) / (0.1 / (t0 + t1) * 2)
	re = 1250 * (0.1 / (t0 + t1) * 2) * d / 2 / eta
	tau = 2 / 9 * d ** 2 / 4 * rho / eta
	s = (0.1 / (t0 + t1) * 2) * tau / exp(1)
	print(('сталь' if steel else 'стекло') + '&{0:.1f}&{1:.1f}&{2:.1f}&{3:.1f}&{4:.3f}&{5:.2f}&{6:.0f}&{7:.0f}\\\\ \\hline'.format(T, d * 1000, t0, t1, eta, re, tau * 1000, s * 10 ** 6))