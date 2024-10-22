#!/bin/bash -e

for x in aa_myss  aa_myss_nbrmyss  aa_myss_nbrmyss_revnbrdist
do
	./analyze_sf.bash reseek_$x evalue
done
