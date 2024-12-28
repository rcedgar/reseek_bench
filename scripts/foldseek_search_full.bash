#!/bin/bash -e

dir=../full_chains

mkdir -p ../foldseek_search_full
cd ../foldseek_search_full

rm -rf ../foldseek_tmp
mkdir -p ../foldseek_tmp

/bin/time -v -o foldseek_search_full.time \
foldseek \
  easy-search \
  $dir \
  $dir \
  -s 9.5 --max-seqs 2000 -e 10 \
  hits.tsv \
  ../foldseek_tmp

cut -f1,2,11 hits.tsv | sed "-es/\.pdb//g" | sort -gk3 > hits_sorted.tsv
