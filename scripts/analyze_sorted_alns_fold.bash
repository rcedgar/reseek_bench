#!/bin/bash -e

mkdir -p ../analysis

for algo in TMalign dali foldseekTM CLE-sw 3Dblast mmseqs2 CE
do
	./analyze_fold.bash $algo score
done

for algo in blastp geometricus foldseek reseek_fast reseek_sensitive reseek_v1.2
do
	./analyze_fold.bash $algo evalue
done
