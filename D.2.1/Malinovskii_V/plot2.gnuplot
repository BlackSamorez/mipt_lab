f(x) = af * x + bf
g(x) = ag * x + bg

fit f(x) 'up2.data' u 2:1 via af, bf
fit g(x) 'down2.data' u 2:1 via ag, bg

set ylabel 'ln(p/p_а)'
set xlabel '1000К/T'

plot 'up2.data' u 2:1:4:3 w xyerrorbars title 'нагр', 'down2.data' u 2:1:4:3 w xyerrorbars title 'охл', f(x) title 'нагр-fit', g(x) title 'охл-fit'

pause -1