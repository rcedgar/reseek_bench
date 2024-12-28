#!/bin/bash -e

mkdir -p ../reseek_search_dbsizes
cd ../reseek_search_dbsizes

dir=../dbsizes
q=../dbsizes/256.cal

for n in 256 512 1024 2048 4096
do
	for t in 1 2 4 8 16 32
	do
		for mode in fast
		do
			name=n$n.t$t
			/usr/bin/time -v -o $name.time \
			reseek \
			  -search $q \
			  -db $dir/$n.cal \
			  -fast \
			  -threads $t \
			  -log $name.log
		done
	done
done
