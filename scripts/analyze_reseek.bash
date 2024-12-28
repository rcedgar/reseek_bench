#!/bin/bash -e

for level in sf2
do
	for algo in reseek_fast reseek_sensitive reseek_verysensitive
	do
		./analyze_level.bash $level $algo evalue
	done
done
