PROC := 4
OUT := out
SRC := src

all: matrixdet run
matrixdet: $(OUT)/matrixdet.out

$(OUT)/%.out: $(SRC)/%.cpp
	@mkdir -p $(OUT)
	upcxx -g $< -o $@

run: run-matrixdet

run-matrixdet:
	@echo ==== Running matrixdet
	upcxx-run -n $(PROC) $(OUT)/matrixdet.out

clean:
	rm -rf $(OUT)

.PHONY: all clean run run-matrixdet matrixdet
