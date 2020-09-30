from math import *


data = [[0] * 10 for x in range(3)]

i=0

with open('./data', 'r') as file:
    s = file.read()  # reading scene.cfg containig map, entitties and targets  # map size x and y
for line in s.split('\n')[0:-1]:
    if (i % 2) == 0 and line != '':
        data[0][i // 2] = line.split('&')[0]
        data[1][i // 2] = line.split('&')[1]
        data[1][i // 2] = data[1][i // 2][0:-2]

        data[1][i // 2] = data[1][i // 2]+'001'
        data[0][i // 2] = data[0][i // 2]+'001'

        data[1][i // 2] = float(data[1][i // 2])
        data[0][i // 2] = float(data[0][i // 2])

        data[2][i // 2] = sqrt((0.000035 + 0.000005 * 1000 / data[0][i // 2])**2 + (0.000035 + 0.000005 * 10 / data[1][i // 2])**2)   

        temp = data[1][i // 2]
        
        data[1][i // 2] = 10000 * data[1][i // 2] / data[0][i // 2]

        data[0][i // 2] = 10**(-2) * temp * data[0][i // 2]

        #data[2][i // 2] = data[2][i // 2] * data[1][i // 2]


        
        i = i + 1
    else:
    	i = i + 1

line = 'A B err \n' 

for num in range(6):

	

	line += str(data[1][num])
	line += '\t'
	line += str(data[0][num])
	line += '\t'
	line += str(data[2][num])
	line += '\n'

print(line)

with open('./exit70', 'w') as file:
	file.write(line)




            