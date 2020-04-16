
OUT:=out
LMK:=latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(OUT)

all: index

index:
	@mkdir -p $(OUT)
	$(LMK) index.tex

index_watch:
	$(LMK) index.tex -pvc

clean:
	$(LMK) index.tex -C

.PHONY: all index index_watch clean
