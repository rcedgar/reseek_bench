#!/bin/bash -e

mkdir -p ../reseek_search_full
cd ../reseek_search_full

for t in 1 2 4 8 16 32
do
	for mode in fast sensitive
	do
		name=$mode.t$t
		/usr/bin/time -v -o $name.time \
		reseek \
		  -search ../full_length_out/full_chains.cal \
		  -db ../full_length_out/full_chains.cal \
		  -$mode \
		  -threads $t \
		  -log $name.log
	done
done
