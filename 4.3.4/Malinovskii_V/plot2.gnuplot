set terminal png size 1080, 980 font "Helvetica,30"

set key right bottom

set tics font "Helvetica,30"

#set xrange[0:0.45]
#set yrange[0:0.45]

set xlabel 'D, мм'
set ylabel 'D_c, мм'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f(x) = a * x + b

fit f(x) 'plot2.data' u 1:3 via a, b

plot 'plot2.data' u 1:3:2:4 w xyerrorbars notitle, f(x) notitle
#pause -1
