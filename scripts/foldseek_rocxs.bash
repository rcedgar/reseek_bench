#!/bin/bash -e

for algo in dali TMalign foldseek CE
do
	./foldseek_rocx.bash $algo
done
