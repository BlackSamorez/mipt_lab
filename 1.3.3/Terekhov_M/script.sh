#!/bin/bash
number=$RANDOM
mkdir $number
python3 change_name.py $1 $2 123 > $number/lab.tex
cp *.png  $number/
cd $number
pdflatex lab.tex
pdflatex lab.tex
mv lab.pdf ../asd.pdf
cd ..
rm -rf $number
