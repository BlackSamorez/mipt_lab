set terminal png size 1920, 1080 font "Helvetica,30"

set key right bottom

set tics font "Helvetica,30"

#set xrange[0:1.1]
#set yrange[0:16]

set xlabel 'n'
set ylabel 'z, мм'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f(x) = a * x * x * x * x + b * x * x * x + c * x * x + d * x + e

fit f(x) 'plot1.data' u 1:2 via a, b, c, d, e

plot 'plot1.data' u 1:2 notitle, f(x) notitle
#pause -1
