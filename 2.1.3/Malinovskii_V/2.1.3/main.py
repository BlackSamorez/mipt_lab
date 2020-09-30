from math import *

def avg(v):
	mxy = mx = my = mx2 = my2 = 0
	for x, y in enumerate(v):
		if y == -1:
			continue
		mx += x
		my += y
		mxy += x * y
		mx2 += x * x
		my2 += y * y
	n = len([y for y in v if y != -1])
	mx /= n
	my /= n
	mxy /= n
	mx2 /= n
	my2 /= n
	b = (mxy - mx * my) / (mx2 - mx * mx)
	db = (((my2 - my * my) / (mx2 - mx * mx) - b * b) / n) ** 0.5
	return (b, db)
		
line_id = 0
speeds = []
for line in open('data'):
	vals = [(float(x) if x != '' else -1) for x in line[:-1].split('\t')]
	f0, f1 = vals[:2]
	f = (f0 + f1) / 2
	df = ((abs(f1 - f0) / 2) ** 2 + 0.01 ** 2) ** 0.5
	vals = vals[2:]
	with open('air_{0}.data'.format(line_id + 1), 'w') as file:
		for x, y in enumerate([y for y in vals if y != -1]):
			file.write('{0}\t{1}\t0.5\n'.format(x, y))
	#print(line_id + 1, end='\t')
	#print('{0:.2f}\t'.format((f0 + f1) / 2, max(((abs(f1 - f0) / 2) ** 2 + 0.01 ** 2) ** 0.5, 0.01)), end='')
	#for i in vals:
	#	print('{0:.0f}'.format(i) if i != -1 else '-', end='\t')
	b, db = avg(vals)
	#print('{0:.1f}\t{1:.1f}\t'.format(b * 2, max(2 * db, 0.1)), end='')
	c = 2 * b * f
	dc = c * (db / b + df / f)
	#print('{0:.0f}\t{1:.0f}\t'.format(c, max(dc, 0)))
	if line_id not in [1, 2]:
		speeds.append([c, dc])
	line_id += 1

def avg2(v):
	out = out2 = 0
	dout = 0
	for i, di in v:
		out += i
		out2 += i * i
		dout += di
	n = len(v)
	out /= n
	out2 /= n
	dout /= n
	D = out2 - out * out
	return [out, sqrt(D / n + dout ** 2)]
#print(avg2(speeds))