#!/bin/bash -e

for level in sf2
do
	for algo in reseek21_fast reseek21_sensitive
	do
		./analyze_level.bash $level $algo evalue
	done
done
