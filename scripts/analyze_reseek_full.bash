#!/bin/bash -e

cd ../reseek_search_full
mkdir -p ../analysis_full

for mode in fast sensitive verysensitive
do
	scop40_full_length_ana.py \
	  $mode.qte.tsv \
	  > ../analysis_full/$mode.txt
	echo $mode `grep tpr_epq1 ../analysis_full/reseek_$mode.txt`
done
