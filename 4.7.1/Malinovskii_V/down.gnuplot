set terminal png size 1920, 1080 font "Helvetica,30"

set key right bottom

set tics font "Helvetica,30"

set xrange[-0.012:1]#0.425]
#set yrange[0:3.1]

set ylabel 'n'
set xlabel 'cos^2(\theta)'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f(x) = a * (x - 1) + b
fit f(x) 'down.data' u 1:3 via a, b


g(x) = a2
fit g(x) 'up.data' u 1:3 via a2

plot 'down.data' u 1:3:2:4 w xyerrorbars notitle, 'up.data' u 1:3:2:4 w xyerrorbars notitle, g(x) notitle, f(x) notitle
#pause -1
