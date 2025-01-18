#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

/bin/time -v -o ../time/reseek_fast \
reseek \
  -search ../data/scop40.bca \
  -fast \
  -output ../alns/reseek_fast.tsv \
  -columns query+target+evalue \
  -log ../reseek_log/fast.log

sort -gk3 ../alns/reseek_fast.tsv \
  > ../sorted_alns/reseek_fast.tsv

rm -f ../analysis/reseek_fast.sf2.txt
./analyze_level.bash sf2 reseek_fast evalue
grep SEPQ ../analysis/reseek_fast.sf2.txt
