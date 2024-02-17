f(x) = a * (x - 0.1) + b

set ylabel 'D, см^2/c'
set xlabel '10кПа/P'
fit f(x) 'plot2.data' u 3:1 via a, b

plot 'plot2.data' u 3:1:4:2 w xyerrorbars title 'points', f(x) title 'fitting line'

pause -1