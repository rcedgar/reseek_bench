#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

for mode in fast sensitive verysensitive
do
	/bin/time -v -o ../time/reseek_new_$mode \
	reseek \
	  -search ../data/scop40.cal \
	  -$mode \
	  -output ../alns/reseek_new_$mode.tsv \
	  -columns query+target+evalue \
	  -log ../reseek_log/$mode._new.log

	sort -gk3 ../alns/reseek_new_$mode.tsv \
	  > ../sorted_alns/reseek_new_$mode.tsv
done

for level in sf2
do
	for algo in reseek_new_fast reseek_new_sensitive reseek_new_verysensitive
	do
		rm -f ../analysis/$algo.$level.txt
		./analyze_level.bash $level $algo evalue
	done
done

./new_summary.bash
