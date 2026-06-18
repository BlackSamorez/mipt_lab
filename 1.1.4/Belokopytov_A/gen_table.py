#\begin{table}
#\centering
#\begin{tabular}{|l|l|l|l|} 
#\hline
# &  &  &   \\ 
#\hline
# &  &  &   \\
# &  &  &   \\
# &  &  &   \\
# &  &  &   \\
#\hline
#\end{tabular}
#\end{table}
cnt1 = 0
cnt2 = 0
with open("exp_data1.txt", 'r') as file:
    read_data = file.read()

strings = read_data.split()
print("\\begin{table}")
print("\\centering")
print("\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|}")
print("\\hline")
print("\\textbf{№ опыта} & \\textbf{", end='')
print(*range(1,11), sep='} & \\textbf{', end='} \\\\\n')
print("\\hline")
for i in range(0, 400, 10):
    print("\\textbf{", i, "}", sep='', end=' ');
    for j in range(i, i+10):
        sm = 0
        for k in range(0, 10):
            sm += int(strings[j*10+k])
        print(" & ", sm, sep='', end='')
        if(abs(sm-10.0425) < 3.1671): cnt1 += 1
        if(abs(sm-10.0425) < 3.1671*2): cnt2 += 1
    print(' \\\\')
print("\\hline")
print("\\end{tabular}")
print("\\end{table}")
print(cnt1, cnt2)

