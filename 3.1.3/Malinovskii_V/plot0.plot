set terminal png size 1920, 1080 font "Helvetica,30"

set key left top

set tics font "Helvetica,30"

set xlabel 'N'
set ylabel 'T, с'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f1(x) = a * x + b
f2(x) = a2 * sqrt(x)

fit f1(x) 'plot0.data' u 1:2 via a, b
#fit f2(x) 'c.data' u 1:5 via a2

plot 'plot0.data' u 1:2:3 w yerrorbars notitle, f1(x) notitle