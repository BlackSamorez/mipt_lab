set terminal png size 1920, 1920 font "Helvetica,30"

set key left top

set tics font "Helvetica,30"

set xrange [-30:30]
set yrange [-120:120]

set ylabel 'U, В'
set xlabel 'I, мА'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

set fit limit 0

f1(x) = a1 * tanh(b1 * x) + c1 * x + d1
f2(x) = a2 * tanh(b2 * x) + c2 * x + d2
f3(x) = a3 * tanh(b3 * x) + c3 * x + d3

a1 = 100
b1 = 0.1
c1 = 0.001
fit f1(x) 'iu2.data' u 1:3 via a1, b1, c1, d1
fit f2(x) 'iu2.data' u 6:8 via a2, b2, c2, d2
fit f3(x) 'iu2.data' u 11:13 via a3, b3, c3, d3

plot 'iu2.data' u 1:3:5:4 w xyerrorbars title "5мА",\
'iu2.data' u 6:8:10:9 w xyerrorbars title "3мА",\
'iu2.data' u 11:13:15:14 w xyerrorbars title "1.5мА",\
f1(x) notitle,\
f2(x) notitle,\
f3(x) notitle