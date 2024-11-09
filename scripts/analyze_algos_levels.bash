#!/bin/bash -e

for level in fam1 sf2 sf3 sf4 fold5 fold6
do
	for algo in dali TMalign
	do
		./analyze_level.bash $level $algo score
	done

	for algo in blastp reseek_fast foldseek reseek_sensitive reseek_verysensitive
	do
		./analyze_level.bash $level $algo evalue
	done
done
