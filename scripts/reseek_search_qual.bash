#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

mode=verysensitive
name=verysensitive_qual

/bin/time -v -o ../time/reseek_$mode \
reseek \
  -search ../data/scop40.cal \
  -$mode \
  -output ../alns/reseek_$name.tsv \
  -columns query+target+qual+newts \
  -log ../reseek_log/$name.log

echo
echo
head ../alns/reseek_verysensitive_qual.tsv
echo
tail ../alns/reseek_verysensitive_qual.tsv
echo
echo Sorting...

sort -rgk3 ../alns/reseek_$name.tsv \
  > ../sorted_alns/reseek_$name.tsv

echo
head ../sorted_alns/reseek_verysensitive_qual.tsv
echo
tail ../sorted_alns/reseek_verysensitive_qual.tsv
