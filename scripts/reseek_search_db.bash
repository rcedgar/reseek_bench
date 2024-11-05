#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

for mode in fast sensitive verysensitive
do
	/bin/time -v -o ../time/reseek_$mode \
	reseek \
	  -search ../data/scop40.cal \
	  -db ../data/scop40.cal \
	  -$mode \
	  -output ../alns/reseek_db_$mode.tsv \
	  -columns query+target+evalue \
	  -log ../reseek_log/$mode.log

	sort -gk3 ../alns/reseek_db_$mode.tsv \
	  > ../sorted_alns/reseek_db_$mode.tsv
done
