#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

mode=try

/bin/time -v -o ../time/reseek_$mode \
reseek \
  -search ../data/scop40.cal \
  -fast \
  -output ../alns/reseek_$mode.tsv \
  -columns query+target+evalue \
  -log ../reseek_log/$mode.log

sort -gk3 ../alns/reseek_$mode.tsv \
  > ../sorted_alns/reseek_$mode.tsv

rm -f ../analysis_family/reseek_try.txt
./analyze_family.bash reseek_$mode evalue
grep SEPQ ../analysis_family/reseek_try.txt
