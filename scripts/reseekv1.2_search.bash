#!/bin/bash -e

mkdir -p ../alns ../sorted_alns

../bin/reseek-linux-x86-v1.2 \
  -search ../data/scop40.cal \
  -output ../alns/reseek_v1.2.tsv \
  -columns query+target+evalue

sort -gk3 ../alns/reseek_v1.2.tsv \
  > ../sorted_alns/reseek_v1.2.tsv
