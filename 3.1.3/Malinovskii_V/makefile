all:
# 	ssh 192.168.1.65 "rm -rf /tmp/tex && mkdir /tmp/tex"
# 	rsync -a *.tex *.png 192.168.1.65:/tmp/tex
# 	ssh 192.168.1.65 "cd /tmp/tex && pdflatex main.tex"
# 	rsync -a 192.168.1.65:/tmp/tex/main.pdf ./
	pdflatex main.tex interaction=batchmode
	
clear:
	rm *.log *.aux *.out -f

read:
	xreader main.pdf