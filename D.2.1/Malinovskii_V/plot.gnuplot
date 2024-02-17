set xlabel 'T, ^o C'
set ylabel 'V, дел'

plot 'up.data' u 2:1:3:4 w xyerrorbars title 'нагр', 'down.data' u 2:1:3:4 w xyerrorbars title 'охл'

pause -1