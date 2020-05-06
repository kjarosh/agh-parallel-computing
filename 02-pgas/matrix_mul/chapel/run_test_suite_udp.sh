#!/bin/bash
# udp setup
# DIR="$(pwd)"
# cd $CHPL_HOME
# export CHPL_COMM=gasnet
# export CHPL_COMM_SUBSTRATE=udp
export GASNET_SPAWNFN=L
export CHPL_RT_NUM_THREADS_PER_LOCALE=1
# cd DIR
chpl -o matrix_mul matrix_mul.chpl

for locales in {1..8}
do
	for size in 100
	do
		echo "seed: 1234  size: $size  repetitions: 2  locales: $locales"
		./matrix_mul --size $size --repetitions 2 -nl $locales
		echo ""
	done
done