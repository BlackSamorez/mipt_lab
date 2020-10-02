from math import *

with open('data.txt', 'r') as file:
	s = [[[float(k) for k in x.split('\t')] for x in a.split('\n')] for a in file.read().split('\n\n')]

rdt = 0.005
rdv = 0.0005
rdp = 0.05
vpd = [39.8, 40.7, 41.6, 42.5, 43.3, 44.1]
vpd = [x / 1000 for x in vpd]
vpd2 = [(vpd[i] + vpd[i + 1]) / 2 for i in range(0, 5)]
dvpd2 = [abs(vpd[i] - vpd[i + 1]) / 2 for i in range(0, 5)]

def avg(values, errors = None):
	if errors is None:
		errors = [0] * len(values)
	v = e = 0
	for v_, e_ in zip(values, errors):
		v += v_
		e += e_
	v /= len(values)
	e /= len(errors)
	div = 0
	for v_ in values:
		div += (v_ - v) ** 2
	div /= len(errors) * (len(errors) - 1)
	div = sqrt(div)
	return (v, sqrt(e ** 2 + div ** 2))

def mse(valuesx, valuesy):
	mxy = mx = my = mxs = mys = 0
	for x_, y_ in zip(valuesx, valuesy):
		mxy += x_ * y_
		mx += x_
		my += y_
		mxs += x_ ** 2
		mys += y_ ** 2

	mxy /= len(valuesx)
	my /= len(valuesx)
	mx /= len(valuesx)
	mxs /= len(valuesx)
	mys /= len(valuesx)
	b = (mxy - mx * my) / (mxs - mx ** 2)
	a = my - b * mx
	db = sqrt(((mys - my ** 2) / (mxs - mx ** 2) - b ** 2) / len(valuesx))
	da = db * sqrt(mxs - mx ** 2)
	return (a, da, b, db)

texts = []
datas = []
points = {}
for series, vpd_, dvpd_ in zip(s, vpd2, dvpd2):
	for x_, y_ in zip([x[0] for x in series], [x[1] for x in series]):
		#print(x_, y_)
		if x_ not in points:
			points[x_] = []
		points[x_].append(y_)
	a, da, b, db = mse([x[0] for x in series], [x[1] for x in series])
	t, dt = avg([x[2] + 273.15 for x in series], [rdt for x in series])
	rdb = b * (rdp / avg([x[0] for x in series])[0] + rdv / avg([x[1] for x in series])[0])
	db = sqrt(db ** 2 + rdb ** 2)
	mu = - b / vpd_
	dmu = mu * (abs(db / b) + abs(dvpd_ / vpd_))
	tmf = 1 / t
	dtmf = dt / t * tmf
	s = '\\begin{tabular}{|c|c|c|} \\hline'
	s += '$p,\\,\\text{бар}$ & $V,\\,\\text{$\\mu$В}$ & $T,\\,\\text{К}$ \\\\ \\hline'
	for line in series:
		s += '${0:.2f}\\pm{1:.2f}$&${2:.1f}\\pm{3:.1f}$&${4:.3f}\\pm{5:.3f}$\\\\ \\hline '.format(line[0], rdp, -line[1] * 1000, rdv * 1000, line[2], rdt)
	s = s + '\\end{tabular}'
	texts.append(s)
	#print('${0:.2f}\\pm{1:.2f}$'.format(t, dt), '${0:.2f}\\pm{1:.2f}$'.format(-b * 1000, db * 1000), '${0:.2f}\\pm{1:.2f}$'.format(vpd_ * 1000, dvpd_ * 1000), '${0:.2f}\\pm{1:.2f}$'.format(mu, dmu), '${0:.4f}\\pm{1:.4f}$'.format(tmf * 1000, dtmf * 1000), sep='&', end='\\\\ \\hline\n')
	#print(tmf * 1000, dtmf * 1000, mu, dmu)
	datas.append([tmf * 1000, dtmf * 1000, mu, dmu])
for key in points.keys():
	print(key, end='\t')
	for i in points[key]:
		print(i, end='\t')
	print('')

out = '\\begin{tabular}{cc}'
for i in range(0, 12):
	k = i % 4
	if k < 2:
		out += (texts[(i // 4) * 2 + k] + ('&' if k == 0 else '\\\\ \\\\') if (i // 4) * 2 + k < 5 else '\\\\')
out += '\\end{tabular}'

#print(out)
a, da = avg([x[0] for x in datas])
b, db = avg([x[2] for x in datas])
a2, da2, b2, db2 = mse([x[0] for x in datas], [x[2] for x in datas])
#print(sqrt(da ** 2 + da2 ** 2))
#print(sqrt((b * (da / a + db / b)) ** 2 + db2 ** 2))
#print(a2, b2)