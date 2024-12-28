#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

for mode in fast sensitive verysensitive
do
	/bin/time -v -o ../time/reseek_newdb_$mode \
	reseek \
	  -search ../data/scop40.cal \
	  -db ../data/scop40.cal \
	  -$mode \
	  -output ../alns/reseek_newdb_$mode.tsv \
	  -columns query+target+evalue \
	  -log ../reseek_log/$mode._newdb.log

	sort -gk3 ../alns/reseek_newdb_$mode.tsv \
	  > ../sorted_alns/reseek_newdb_$mode.tsv
done

for level in sf2
do
	for algo in reseek_newdb_fast reseek_newdb_sensitive reseek_newdb_verysensitive
	do
		rm -f ../analysis/$algo.$level.txt
		./analyze_level.bash $level $algo evalue
	done
done

./new_summary.bash
