from math import *

with open('data2', 'r') as file:
	s = file.read()

s = s.split('\n')
s = [_.split('\t') for _ in s if _.split('\t')[0] == 'сталь']
for x in range(5):
	T = 0
	eta = 0
	deta = 0
	dT = 0.2
	for y in range(2):
		i = x * 2 + y
		T += float(s[i][1])
		eta += float(s[i][5])
		deta += float(s[i][9])
	T /= 2
	T += 273.3
	eta /= 2
	deta /= 2
	print(1000 / T)