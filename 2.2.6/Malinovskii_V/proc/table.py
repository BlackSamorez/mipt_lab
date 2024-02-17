def centered(x):
	return '\\begin{{center}}\n' + str(x) + '\\end{{center}}\n'

class RawTable:
	def __init__(self, title = [], content = []):
		self.title = title
		self.content = content

	def __str__(self):
		w = len(self.content)
		h = len(self.content[0])

		out = ''
		out += '\\begin{{tabular}}{{' + '|' + 'c|' * w + '}}\n'

		for x in range(w):
			out += str(self.title[x]) + ('&' if x != w - 1 else '\\\\')
		out += '\n'

		for y in range(h):
			for x in range(w):
				out += str(self.content[x][y]) + ('&' if x != w - 1 else '\\\\')
			out += '\n'
		out += '\\end{{tabular}}\n'
		return out

class ProcessingTable:
	def __init__(self, title = [], input_ids = [], functions = []):
		self.rawTable = RawTable(title = title, content = [])
		self.input_ids = input_ids
		self.functions = functions
	
	def file_load(self, filename):
		w = len(self.rawTable.title)
		self.rawTable.content = [[] for _ in range(w)]
		with open(filename, 'r') as f:
			for line in f.read().split('\n'):
				if line == '':
					continue
				
				for _ in range(w):
					self.rawTable.content[_].append('--')

				for val_place, val in zip(self.input_ids, line.split(' ')):
					self.rawTable.content[val_place][-1] = float(val)

				for function in self.functions:
					self.rawTable.content[function[0][1]][-1] = function[1]([self.rawTable.content[_][-1] for _ in function[0][0]])

	def __str__(self):
		return str(self.rawTable)

def foo(v):
	print(v)
	x, y = v
	return x + y

#table = ProcessingTable(title=['title_{0}'.format(_) for _ in range(5)], input_ids = [0, 1, 2], functions = [[((0, 1), 3), foo]])
#table.file_load('table')

#print(centered(RawTable(title=['$1$!','2!','3!','4!'], content=[[1, 2, 3, 4], [5, 6, 7, 8], [5, 6, 7, 8], [5, 6, 7, 8]])))