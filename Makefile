# If you are new to Makefiles: https://makefiletutorial.com

PAPER := output/paper.pdf
PRESENTATION := output/presentation.pdf

TARGETS :=  $(PAPER) $(PRESENTATION)

EXTERNAL_DATA := data/external/wscp_panel.xlsx \
	data/external/wscp_static.txt

RESULTS := output/results.pickle

.PHONY: all clean very-clean dist-clean

all: $(TARGETS)

clean:
	rm -f $(TARGETS) $(RESULTS)

$(RESULTS): code/python/do_analysis.py $(EXTERNAL_DATA)
	python $<

$(PAPER): doc/paper.qmd doc/references.bib $(RESULTS)
	quarto render $< --quiet
	mv doc/paper.pdf output
	rm -f doc/paper.ttt doc/paper.fff

$(PRESENTATION): doc/presentation.qmd doc/beamer_theme_trr266.sty $(RESULTS)
	quarto render $< --quiet
	mv doc/presentation.pdf output
	rm -rf doc/presentation_files