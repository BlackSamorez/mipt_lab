set terminal png size 1920, 1080 font "Helvetica,30"

set key left top

set tics font "Helvetica,30"

set xrange [3:13]

set xlabel 'N'
set ylabel 'M, дин*см'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f1(x) = a * x + b
f2(x) = a2 * sqrt(x)

fit f1(x) 'plot1.data' u 1:3 via a, b
#fit f2(x) 'c.data' u 1:5 via a2

plot 'plot1.data' u 1:3:4 w yerrorbars notitle, f1(x) notitle