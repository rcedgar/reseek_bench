#!/bin/bash -e

for mode in fast
do
	  rm -f ../alns/reseek_$mode.tsv \
	  rm -f ../reseek_log/$mode.log
	  rm -f ../sorted_alns/reseek_$mode.tsv
	  rm -f ../analysis/reseek_$mode.*
done

for mode in fast
do
	/bin/time -v -o ../time/reseek_$mode \
	reseek \
	  -search ../data/scop40.cal \
	  -$mode \
	  -output ../alns/reseek_$mode.tsv \
	  -columns query+target+evalue \
	  -log ../reseek_log/$mode.log

	sort -gk3 ../alns/reseek_$mode.tsv \
	  > ../sorted_alns/reseek_$mode.tsv
done


for level in sf2
do
	for algo in reseek_fast
	do
		./analyze_level.bash $level $algo evalue
	done
done
