#!/bin/bash -e

labels=../full_length_out/ge150.labels
cal=../full_length_out/full_chains.cal

mkdir -p ../dbsizes
cd ../dbsizes

for n in 256 512 1024 2048 4096
do
	randlines.py $labels $n \
	  > $n.labels

	reseek \
	  -getchains $cal \
	  -labels $n.labels \
	  -cal $n.cal
done
