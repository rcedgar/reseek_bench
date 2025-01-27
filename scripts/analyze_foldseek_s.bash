#!/bin/bash -e

hits=../alns/foldseek_s$1.tsv
sorted=../sorted_alns/foldseek_s$1.tsv

if [ ! -s $hits ] ; then
	echo Not found hits=$hits
	exit 1
fi

if [ ! -s $sorted ] ; then
	cut -f1,2,11 $hits \
		| sort -gk3 \
		> $sorted
fi

./analyze_level.bash sf2 foldseek_s$1 evalue

grep SEPQ ../analysis/foldseek_s$1.sf2.txt
