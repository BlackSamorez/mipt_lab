set terminal png size 1920, 1080 font "Helvetica,30"

#set key right bottom
set key out

set tics font "Helvetica,30"

set xrange[0:1.05]
set yrange[-0.5:0]

set ylabel 'k, мТл/А'
set xlabel 'I, мА'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f(x) = a * x

fit f(x) 'sum.data' u 1:2 via a

plot 'sum.data' u 1:2:3:4 w xyerrorbars notitle, f(x) notitle

#pause -1