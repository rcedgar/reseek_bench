#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

for mode in fast sensitive verysensitive
do
	name=big$mode
	/bin/time -v -o ../time/reseek_$name \
	reseek \
	  -bigsearch ../data/scop40.bca \
	  -db ../data/scop40.bca \
	  -$mode \
	  -output ../alns/reseek_$name.tsv \
	  -columns query+target+evalue \
	  -log ../reseek_log/$name.log

	sort -gk3 ../alns/reseek_$name.tsv \
	  > ../sorted_alns/reseek_$name.tsv
done

./analyze_reseek_big.bash
