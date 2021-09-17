set terminal png size 1920, 1080 font "Helvetica,30"

set key right bottom

set tics font "Helvetica,30"

#set xrange[-0.012:1]#0.425]
#set yrange[0:3.1]

set ylabel 'theta'
set xlabel 'phi'

set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 5           # set the spacing for the mytics
set grid

set grid ytics lc rgb "#bbbbbb" lw 2 lt 0
set grid xtics lc rgb "#bbbbbb" lw 2 lt 0

f(x) = f0 + f1 * x + f2 * x * x + f3 * x * x * x
fit f(x) 'plot2_down.csv' u 1:2 via f0, f1, f2, f3

g(x) = g0 + g1 * x + g2 * x * x + g3 * x * x * x + g4 * x * x * x * x + g5 * x * x * x * x * x + g6 * x * x * x * x * x * x + g7 * x * x * x * x * x * x * x
fit g(x) 'plot2_up.csv' u 1:2 via g0, g1, g2, g3, g4, g5, g6, g7

plot 'plot2_down.csv' u 1:2:3:4 w xyerrorbars title 'необыкновенная волна', 'plot2_up.csv' u 1:2:3:4 w xyerrorbars title 'обыкновенная волна', g(x) notitle, f(x) notitle