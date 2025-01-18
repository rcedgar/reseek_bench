#!/bin/bash -e

for level in sf2
do
	for algo in reseek_bigfast reseek_bigsensitive reseek_bigverysensitive
	do
		./analyze_level.bash $level $algo evalue
	done
done

grep SEPQ ../analysis/reseek_big*
