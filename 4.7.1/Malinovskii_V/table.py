print('\\hline', end=' ')
for line in open('table.txt'):
	line = line[:-1].split('\t')
	for i in line[:-1]:
		print(i, end='&')
	print(line[-1], end='\\\\ \\hline\n')