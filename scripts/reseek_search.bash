#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time

for mode in fast sensitive ## verysensitive not worth it
do
	/bin/time -v -o ../time/reseek_$mode \
	reseek \
	  -search ../data/scop40.cal \
	  -$mode \
	  -output ../alns/reseek_$mode.tsv \
	  -columns query+target+evalue

	sort -gk3 ../alns/reseek_$mode.tsv \
	  > ../sorted_alns/reseek_$mode.tsv
done
