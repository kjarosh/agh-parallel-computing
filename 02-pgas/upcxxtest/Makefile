PROC=4
OUT=out

all: rbsolver rpcexample

rbsolver: rbsolver.cpp
	mkdir -p $(OUT)
	upcxx -g $< -o $(OUT)/$@.out
	upcxx-run -n $(PROC) $(OUT)/$@.out


rpcexample: rpcexample.cpp
	mkdir -p $(OUT)
	upcxx -g $< -o $(OUT)/$@.out
	upcxx-run -n $(PROC) $(OUT)/$@.out

clean:
	rm -rf $(OUT)

.PHONY: all rbsolver rpcexample
