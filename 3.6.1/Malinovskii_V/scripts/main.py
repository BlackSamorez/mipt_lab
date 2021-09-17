a = [_.split('\t') for _ in open('a.txt', 'r').read().split('\n')]
b = [_.split('\t') for _ in open('b.txt', 'r').read().split('\n')]

for _ in range(len(a)):
	for a_, b_ in zip(a[_], b[_]):
		print(a_, b_, end='\t', sep='\t')
	print('')