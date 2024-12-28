#!/bin/bash -e

mkdir -p ../reseek_ge500
cd ../reseek_ge500

for mode in fast sensitive verysensitive
do
	reseek \
	  -search ../full_length_out/ge500.cal \
	  -db ../full_length_out/ge500.cal \
	  -$mode \
	  -output $mode.tsv \
	  -noself

	cut -f2,3,4 $mode.tsv \
	  | sort -gk3 \
	  > $mode.qte.tsv

	scop40_full_length_ana.py $mode.qte.tsv \
	  > $mode.ana.tsv
done
