# LaTeX Makefile
FILE=wigi-dataset-icwsm

all: $(FILE).pdf clean

.PHONY: $(FILE).pdf clean cleanall

clean:
	\rm -fv *.aux *.blg *.ilg *.lot *.idx *.lof *.out *.ind *.bbl *.log *.toc

cleanall:
	\rm -fv *.aux *.blg *.ilg *.lot *.idx *.lof *.out *.ind *.bbl *.log *.toc $(FILE).pdf

# -shell-escape required for minted package to work since it depends on
#  pygments
$(FILE).pdf: $(FILE).tex
	pdflatex -shell-escape $(FILE)
	bibtex $(FILE)
	pdflatex -shell-escape $(FILE)
	pdflatex -shell-escape $(FILE)
 
