#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

/bin/time -v -o ../time/reseek_verysensitive \
reseek \
  -search ../data/scop40.bca \
  -db ../data/scop40.bca \
  -verysensitive \
  -output ../alns/reseek_verysensitive.tsv \
  -columns query+target+evalue \
  -log ../reseek_log/verysensitive.log

sort -gk3 ../alns/reseek_verysensitive.tsv \
  > ../sorted_alns/reseek_verysensitive.tsv

rm -f ../analysis/reseek_verysensitive.sf2.txt
./analyze_level.bash sf2 reseek_verysensitive evalue
grep SEPQ ../analysis/reseek_verysensitive.sf2.txt
