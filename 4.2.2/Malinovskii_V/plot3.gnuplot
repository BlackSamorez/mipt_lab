set terminal png size 1920, 1080 font "Helvetica,30"

set key right bottom

set tics font "Helvetica,30"

#set xrange[-11:11]
#set yrange[3.6:5.2]

set xlabel 't, мин'
set ylabel '\delta n, 10^{-5}'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f(x) = a * exp(-x * b)

fit f(x) 'plot3.data' u 1:2 via a, b

plot 'plot3.data' u 1:2:3 w yerrorbars notitle, f(x) notitle
#pause -1
