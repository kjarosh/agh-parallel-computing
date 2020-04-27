ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER_IMAGE:=$(shell docker build -q .)
DOCKER_PREFIX:=docker run --rm -v "$(ROOT_DIR)":/opt/benchmark -w /opt/benchmark \
	$(DOCKER_IMAGE)

_all: build run

build: out/benchmark

out/benchmark: src
	@mkdir -p out
	$(DOCKER_PREFIX) chpl --fast --static -o out/benchmark src/main.chpl

run:
	./out/benchmark -nl 2

clean:
	rm -rf out

docker: src
	@mkdir -p out
	$(DOCKER_PREFIX) bash

.PHONY: _all run build clean docker
