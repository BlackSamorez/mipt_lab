set xlabel 't, с'
set ylabel 'ln(v/v_0)'

f1(x) = a1 * x + b1
fit f1(x) '1.data' u 1:2 via a1, b1
f2(x) = a2 * x + b2
fit f2(x) '2.data' u 1:2 via a2, b2
f3(x) = a3 * x + b3
fit f3(x) '3.data' u 1:2 via a3, b3
f4(x) = a4 * x + b4
fit f4(x) '4.data' u 1:2 via a4, b4
f5(x) = a5 * x + b5
fit f5(x) '5.data' u 1:2 via a5, b5
f6(x) = a6 * x + b6
fit f6(x) '6.data' u 1:2 via a6, b6
f7(x) = a7 * x + b7
fit f7(x) '7.data' u 1:2 via a7, b7

plot '1.data' u 1:2 title 'P=5.5кПа', '2.data' u 1:2 title 'P=11.5кПа', '3.data' u 1:2 title 'P=19кПа', '4.data' u 1:2 title 'P=22.5кПа', '5.data' u 1:2 title 'P=29кПа', '6.data' u 1:2 title 'P=34.5кПа', '7.data' u 1:2 title 'P=40кПа'

pause -1