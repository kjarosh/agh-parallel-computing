PROC := 8
OUT := out
SRC := src

all: benchmark run
benchmark: $(OUT)/benchmark

$(OUT)/%: $(SRC)/%.cpp
	@mkdir -p $(OUT)
	upcxx -g $< -o $@

run:
	@echo ==== Running benchmark
	upcxx-run -n $(PROC) $(OUT)/benchmark

clean:
	rm -rf $(OUT)

.PHONY: all clean run benchmark
