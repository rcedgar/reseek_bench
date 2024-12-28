#!/bin/bash -e

for mode in fast sensitive verysensitive
do
	rm -f  $mode.time \
	  ../reseek_search_full/$mode.log \
	  ../reseek_search_full/$mode.tsv \
	  ../reseek_search_full/$mode.qte.tsv \
	  ../reseek_search_full/$mode.ana.tsv
done
