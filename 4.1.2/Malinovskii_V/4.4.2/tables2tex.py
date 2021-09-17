import sys

s = sys.stdin.read()

lines = s.split('\n')

if lines[-1] == '':
	lines = lines[:-1]

if len(lines) == 0:
	raise Exception('Empty file')

lines = [_.split('\t') for _ in lines]

def process_dataline(line):
	line = [float(_) for _ in line[1:]]
	return line

def process_dataline_int(line):
	line = [int(_) for _ in line[1:]]
	return line

def process_error(line):
	def process_error_v(v):
		if v == 'None':
			return None
		if v[0] == 'c':
			return {'link': True, 'link_to': int(v[1:])}
		else:
			return {'link': False, 'val': float(v)}

	line = [process_error_v(_) for _ in line]
	return line

data_lines = [process_dataline(_) for _ in lines if _[0] == 'data']

for line in lines:
	if line[0] == 'err':
		errors = process_error(line[1:])
	if line[0] == 'name':
		names = line[1:]
	if line[0] == '#':
		ids = process_dataline_int(line)

def get_id_place(search_id):
	global ids
	for place, check_id in enumerate(ids):
		if check_id == search_id:
			return place

is_data_column = [True] * len(data_lines[0])
for err_id, err in enumerate(errors):
	if err is None:
		is_data_column[err_id] = False

data_out = []
err_out = []

for line in data_lines:
	new_data_line = []
	new_err_line = []

	for _ in range(len(line)):
		if is_data_column[_]:
			new_data_line.append(line[_])
			if errors[_]['link']:
				new_err_line.append(line[get_id_place(errors[_]['link_to'])])
			else:
				new_err_line.append(errors[_]['val'])
		else:
			new_data_line.append(None)
			new_err_line.append(None)

	data_out.append(new_data_line)
	err_out.append(new_err_line)

float_round = lambda x: int(x) + (0 if (x - int(x)) < 0.5 else 1)

def val_error_norm(val, error):
	if val is None:
		return (None, None)
	if error == 0:
		if val == 0:
			return ('0', '0')
		return (str(val), '0')
	e = 1;
	shift = 0
	while error >= 10:
		error /= 10
		val /= 10
		e *= 10
		shift += 1

	while error < 1:
		error *= 10
		val *= 10
		e /= 10
		shift -= 1

	if error < 2:
		error *= 10
		val *= 10
		e /= 10
		shift -= 1

	error = float_round(error)
	val = float_round(val)

	if error == 10:
		error /= 10
		val /= 10
		e *= 10
		shift += 1

	val = val * e
	error = error * e
	return ("{:.{}f}".format(val, max(-shift, 0)), "{:.{}f}".format(error, max(-shift, 0)))

data_out_str = []
err_out_str = []

for line_data, line_err in zip(data_out, err_out):
	str_line_data = []
	str_line_err = []
	for data_point, err_point in zip(line_data, line_err):
		str_data_point, str_err_point = val_error_norm(data_point, err_point)
		str_line_data.append(str_data_point)
		str_line_err.append(str_err_point)
	data_out_str.append(str_line_data)
	err_out_str.append(str_line_err)

print_down = [False] * len(err_out_str[0])
for column_id in range(len(err_out_str[0])):
	if not is_data_column[column_id]:
		continue

	to_print_down = True
	for row_id in range(len(err_out_str) - 1):
		to_print_down = to_print_down and (err_out_str[row_id][column_id] == err_out_str[row_id + 1][column_id])

	print_down[column_id] = to_print_down

table_len = sum(is_data_column) * 2 - sum(print_down)

def texify_name(name, end_ket = False):
	parts = name.split(',')
	out = '${}'.format(parts[0])
	if end_ket:
		out += ')'
	if len(parts) > 1:
		if parts[1] == ' Тл^2':
			out += '\\text{, Тл}^2'
		else:
			out += '\\text{{,{}}}'.format(parts[1])
	out += '$'
	return out

def texify_val(val):
	return f'${val}$'

def texify_err(name, err):
	try:
		beg, end = name.split(', ')
	except:
		beg = name
		end = ''
	if beg[:len('\\Delta')] == '\\Delta' or beg[:len(' \\Delta')] == ' \\Delta' or beg[:len('  \\Delta')] == '  \\Delta':
		return '\\Delta ({})={}\\,\\text{{{}}}'.format(beg, err, end)
	else:
		return '\\Delta {}={}\\,\\text{{{}}}'.format(beg, err, end)

print('\\begin{center}')
print('\\begin{tabular}{|' + 'c|' * table_len + '}\\hline')

counter_col = 0
for column_id in range(len(err_out_str[0])):
	if is_data_column[column_id]:
		counter_col += 1
		print(texify_name(names[column_id]), end='&' if counter_col != table_len else '\\\\\\hline')
		if not print_down[column_id]:
			counter_col += 1
			if names[column_id][:len('\\Delta')] == '\\Delta' or names[column_id][:len(' \\Delta')] == ' \\Delta':
				print(texify_name('\\Delta (' + names[column_id], True), end='&' if counter_col != table_len else '\\\\\\hline')
			else:
				print(texify_name('\\Delta ' + names[column_id]), end='&' if counter_col != table_len else '\\\\\\hline')

print()

for row_id in range(len(err_out_str)):
	counter_col = 0
	for column_id in range(len(err_out_str[0])):
		if not is_data_column[column_id]:
			continue
		counter_col += 1
		print(texify_val(data_out_str[row_id][column_id]), end='&' if counter_col != table_len else '\\\\\\hline')
		if not print_down[column_id]:
			counter_col += 1
			print(texify_val(err_out_str[row_id][column_id]), end='&' if counter_col != table_len else '\\\\\\hline')
	print()

print('\\end{tabular}\\\\~\\\\')

if sum(print_down) > 0:
	print('$', end='')
	counter_col = 0
	for column_id in range(len(err_out_str[0])):
		if print_down[column_id]:
			counter_col += 1
			print(texify_err(names[column_id], err_out_str[0][column_id]), end=', ' if counter_col < sum(print_down) else '')
	print('$')
print('\\end{center}')