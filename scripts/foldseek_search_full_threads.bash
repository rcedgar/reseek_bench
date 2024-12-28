#!/bin/bash -e

dir=../full_chains

mkdir -p ../foldseek_search_full
cd ../foldseek_search_full

for t in 1 2 4 8 16 32
do
	rm -rf ../foldseek_tmp
	mkdir -p ../foldseek_tmp

	/bin/time -v -o foldseek_search_full.t$t.time \
	foldseek \
	  easy-search \
	  $dir \
	  $dir \
	  -s 9.5 --max-seqs 2000 -e 10 \
	  --threads $t \
	  hits.tsv \
	  ../foldseek_tmp
done
