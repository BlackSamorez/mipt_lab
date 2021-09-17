set terminal png size 1920, 1080 font "Helvetica,30"

set key right bottom

set tics font "Helvetica,30"

#set xrange[0:0.45]
#set yrange[0:0.45]

set xlabel 'd, мкм'
set ylabel 'K/Y, 1/мм'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f(x) = a * x + b

fit f(x) 'plot3.data' u 3:1 via a, b

plot 'plot3.data' u 3:1:4:2 w xyerrorbars notitle, f(x) notitle
#pause -1
