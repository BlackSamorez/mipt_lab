import argparse 
parser = argparse.ArgumentParser()

parser.add_argument('-i', action='store', required=True)

args = parser.parse_args()

input_file = args.i

with open(input_file, 'r') as file:
	data = [_.split('\t') for _ in file.read().split('\n')]
	if data[-1] == ['']:
		data = data[:-1]

def error_fixer(v, dv):
	e = 1
	loge = 0
	while dv < 1 or (1.3 <= dv and dv <= 1.6):
		dv *= 10
		v *= 10
		e *= 10
		loge += 1
	v = int(v) + (1 if v - int(v) >= 0.5 else 0)
	dv = int(dv)
	return (loge, v / e, dv / e)

def print_with_error_fixer(v, dv, next_line_error = False):
	out = error_fixer(v, dv)
	print('${:.{}f}$'.format(out[1], out[0]), end='')
	if next_line_error:
		print('&${:.{}f}$'.format(out[2], out[0]), end='')

w = len(data[0]) - 1
h = len(data)

fixed_errors = [-1] * w
rel_errors = [-1] * w
to_print = [True] * w
ignore = [False] * w
for line in data:
	if line[0] == 'err':
		fixed_errors = [float(_) for _ in line[1:]]

	if line[0] == 'err_rel':
		rel_errors = [int(_) for _ in line[1:]]
		for _ in range(w):
			if rel_errors[_] > 0:
				to_print[rel_errors[_]] = False

	if line[0] == 'ignore':
		ignore_data = [int(_) for _ in line[1:]]
		for _ in range(w):
			ignore = [_ != -1 for _ in ignore_data]

def get_error(id_, data_line):
	if not to_print[id_]:
		return None
	if fixed_errors[id_] != -1:
		return float(fixed_errors[id_])
	if rel_errors[id_] != -1:
		return float(data_line[rel_errors[id_]])
	return None


print_error_in_column = [False] * w
final_errors = [-1] * w
final_w = w
for _ in range(w):
	if ignore[_]:
		continue
	tmp_error = None
	for line in data:
		if line[0] != 'data':
			continue

		new_tmp_error = get_error(_, line[1:])
		if tmp_error is None:
			tmp_error = new_tmp_error
			final_errors[_] = tmp_error
		elif tmp_error != new_tmp_error:
			print_error_in_column[_] = True
			final_w += 1
			break 

print('\\begin{center}')
print('\\begin{tabular}{|' + 'c|' * final_w + '}\\hline')
names = []
for line in data:
	if line[0] == 'name':
		names = line[1:]
		name_line = line[1:]
		def print_name(name, print_error = False):
			print(name, end='')
			if print_error:
				print('&$\\Delta {0}'.format(name[1:]))

		comma_flag = False
		for _ in range(w):
			if ignore[_]:
				continue
			if to_print[_]:
				if comma_flag:
					print('&', end='')
				else:
					comma_flag = True
				print_name(name_line[_], print_error_in_column[_])

		print('\\\\ \\hline')
	if line[0] != 'data':
		continue
	data_line = line[1:]

	first_column = True
	for _ in range(w):
		if ignore[_]:
			continue
		if not to_print[_]:
			continue

		if first_column:
			first_column = False
		else:
			print('&', end='')

		error = get_error(_, data_line)
		if error is None:
			print(data_line[_], end='')
		else:
			print_with_error_fixer(float(data_line[_]), error, print_error_in_column[_])
	print('\\\\ \\hline')
print('\\end{tabular}')
print('\\end{center}')

print_bottom = False
for _ in range(w):
	if ignore[_]:
		continue
	if print_error_in_column[_] or final_errors[_] is None:
		continue
	print_bottom = True
	break

if print_bottom:
	print('$$', end='')
	comma_flag = False
	for _ in range(w):
		if ignore[_]:
			continue
		if print_error_in_column[_] or final_errors[_] is None:
			continue
		name_ = names[_][1:-1].split(',')
		if len(name_) > 1:
			name, name_units = name_
		else:
			name = name_[0]
			name_units = None
		if comma_flag:
			print(',\\,\\,', end='')
		else:
			comma_flag = True
		if name_units is None:
			print('\\Delta {0}={1}'.format(name, final_errors[_]), end='')
		else:
			print('\\Delta {0}={1}\\,{2}'.format(name, final_errors[_], name_units), end='')
	print('.$$', end='')