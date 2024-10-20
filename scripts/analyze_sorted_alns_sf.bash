#!/bin/bash -e

for algo in TMalign dali foldseekTM CLE-sw 3Dblast mmseqs2 CE
do
	./analyze_sf.bash $algo score
done

for algo in blastp geometricus foldseek reseek_fast reseek_sensitive reseek_verysensitive reseek_v1.2
do
	./analyze_sf.bash $algo evalue
done
