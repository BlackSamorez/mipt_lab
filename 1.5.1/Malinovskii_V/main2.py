from math import *

s = [float(x) for x in '176	176	176	176	175'.split('\t')]


def avg(list_):
	m = 0
	ms = 0
	for v in list_:
		m += v
		ms += v ** 2
	n = len(list_)

	m /= n
	ms /= n
	return (m, ((ms - m ** 2) / (n * (n - 1))) ** 0.5)

print(avg(s))