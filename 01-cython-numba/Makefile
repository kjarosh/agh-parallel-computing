
VENV := test -f ../venv/bin/activate && . ../venv/bin/activate;
LMK=latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error

run:
	$(VENV) cd src && python3 -m run

run_pi:
	$(VENV) cd src && python3 -m run_pi

run_pi_plot:
	$(VENV) cd src && python3.7 -m run_pi plot

report:
	cd report && $(LMK) -output-directory=../report-out index.tex

report_watch:
	cd report && $(LMK) -output-directory=../report-out index.tex -pvc

clean:
	cd report && $(LMK) -output-directory=../report-out index.tex -C

.PHONY: run run_pi report report_watch clean
