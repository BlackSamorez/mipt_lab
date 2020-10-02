from math import *

vs = 0
for i in range(0, 6):
	s = input()
	d = 32.0
	dd = 0.5

	x00, x01, x1, m, t = [float(x) for x in s.split(' ')]
	x0 = (x00 + x01) / 2
	dx0 = abs(x0 - x00)
	dx1 = 0.05
	fi0 = abs(x0 - x1) / d / 2
	dfi0 = ((dx0 + dx1) / abs(x0 - x1) + dd / d) * fi0
	fi1 = abs(acos(x0 / d) - acos(x1 / d)) / 2
	dfi1 = abs((acos((x0 + dx0) / (d - dd)) - acos((x0 - dx0) / (d + dd)))) / 4 + abs((acos((x1 + dx1) / (d - dd)) - acos((x1 - dx1) / (d + dd)))) / 4
	v0 = fi0 * 0.0929 * t / (2 * pi * m * 0.2015) * 1000
	dv0 = ((dfi0 / fi0) + (0.04 / t) + (0.001 / m)) * v0
	v1 = fi1 * 0.0929 * t / (2 * pi * m * 0.2015) * 1000
	dv1 = ((dfi1 / fi0) + (0.04 / t) + (0.001 / m)) * v0
	vs += v1
	print("{0:.1f}".format(x0), "{0:.1f}".format(dx0), "{0:.1f}".format(x1), "{0:.4f}".format(m), "{0:.2f}".format(t), "{0:.3f}\\pm{1:.3f}".format(fi0, dfi0), "{0:.3f}\\pm{1:.3f}".format(fi1, dfi1), "{0:.0f}\\pm{1:.0f}".format(v0, dv0), "{0:.0f}\\pm{1:.0f}".format(v1, dv1), sep='& ', end='\\\\\n\\hline\n')
