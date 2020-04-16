PROC := 4
OUT := out
SRC := src

all: rbsolver rpcexample run
rbsolver: $(OUT)/rbsolver.out
rpcexample: $(OUT)/rpcexample.out

$(OUT)/%.out: $(SRC)/%.cpp
	@mkdir -p $(OUT)
	upcxx -g $< -o $@

run: run-rbsolver run-rpcexample

run-rbsolver:
	@echo ==== Running rbresolver
	upcxx-run -n $(PROC) $(OUT)/rbsolver.out

run-rpcexample:
	@echo ==== Running rpcexample
	upcxx-run -n $(PROC) $(OUT)/rpcexample.out

clean:
	rm -rf $(OUT)

.PHONY: all clean run run-rbsolver run-rpcexample rbsolver rpcexample
