set terminal png size 1920, 1080 font "Helvetica,30"

set key left top

set tics font "Helvetica,30"

set xlabel 'I, мА'
set ylabel 'U, В'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f1(x) = a1 * sqrt(abs(x)) + b
f2(x) = a2 * sqrt(x)

#fit f1(x) 'c.data' u 1:3 via a1, b
#fit f2(x) 'c.data' u 1:5 via a2

plot 'iu.data' u 3:1:4:5 w xyerrorbars title "ВАХ"