#!/bin/bash -e

mkdir -p ../reseek_search_full
cd ../reseek_search_full

for mode in fast sensitive verysensitive
do
	/usr/bin/time -v -o $mode.time \
	reseek \
	  -search ../full_length_out/full_chains.cal \
	  -db ../full_length_out/full_chains.cal \
	  -$mode \
	  -dbsize 7283 \
	  -log $mode.log \
	  -output $mode.tsv

	cut -f2,3,4 $mode.tsv \
	  | sort -gk3 \
	  > $mode.qte.tsv
done
