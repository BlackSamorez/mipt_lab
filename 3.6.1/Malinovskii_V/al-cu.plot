set terminal png size 1920, 1080 font "Helvetica,30"

set key left top

set tics font "Helvetica,30"

set xlabel 'B^2, Тл^2'
set ylabel 'm, мг'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f1(x) = a1 * x
f2(x) = a2 * x
f3(x) = a3 * x
f4(x) = a4 * x

fit f1(x) 'al.data' u 1:3 via a1
fit f2(x) 'al.data' u 1:5 via a2
fit f3(x) 'cu.data' u 1:3 via a3
fit f4(x) 'cu.data' u 1:5 via a4

plot 'al.data' u 1:3:2:4 w xyerrorbars title "алюминий-up", 'al.data' u 1:5:2:6 w xyerrorbars title "алюминий-down", 'cu.data' u 1:3:2:4 w xyerrorbars title "медь-up", 'cu.data' u 1:5:2:6 w xyerrorbars title "медь-down", f1(x) lt rgb "red" notitle, f2(x) notitle, f3(x) notitle, f4(x) notitle