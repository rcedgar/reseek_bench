#!/bin/bash -e

for algo in TMalign dali
do
	./analyze_half.bash $algo score
done

for algo in foldseek reseek_fast reseek_sensitive reseek_verysensitive
do
	./analyze_half.bash $algo evalue
done
