#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

/bin/time -v -o ../time/reseek_sensitive \
reseek \
  -search ../data/scop40.bca \
  -sensitive \
  -output ../alns/reseek_sensitive.tsv \
  -columns query+target+evalue \
  -log ../reseek_log/sensitive.log

sort -gk3 ../alns/reseek_sensitive.tsv \
  > ../sorted_alns/reseek_sensitive.tsv

rm -f ../analysis/reseek_sensitive.sf2.txt
./analyze_level.bash sf2 reseek_sensitive evalue
grep SEPQ ../analysis/reseek_sensitive.sf2.txt
