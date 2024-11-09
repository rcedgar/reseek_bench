#!/bin/bash -e

for level in fam1 sf2 sf3 sf4 fold5 fold6
do
	for algo in TMalign dali
	do
		echo ===== $algo $level ======
		./top_hit.bash $algo score $level
	done

	for algo in blastp foldseek reseek_fast reseek_sensitive reseek_verysensitive
	do
		echo ===== $algo $level ======
		./top_hit.bash $algo evalue $level
	done
done
