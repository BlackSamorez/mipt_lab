set xrange[1.75:4.25]

plot 'big.plotdata' u 1:2:7:8 w xyerrorbars title '20^oC', 'big.plotdata' u 1:3:7:8 w xyerrorbars title '30^oC', 'big.plotdata' u 1:4:7:8 w xyerrorbars title '40^oC', 'big.plotdata' u 1:5:7:8 w xyerrorbars title '50^oC', 'big.plotdata' u 1:6:7:8 w xyerrorbars title '60^oC',
pause -1