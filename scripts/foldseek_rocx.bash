#!/bin/bash -e

####################################################
# Analysis using awk script from foldseek repo
# https://github.com/steineggerlab/foldseek-analysis
####################################################

lookup=../data/dom_scopid.tsv
hits=../sorted_alns/$1.tsv
out=../rocx/$1.rocx

if [ ! -s $hits ] ; then
	echo "Not found hits=$hits"
	exit 1
fi

if [ -s $out ] ; then
	echo "Already done out=$out"
	exit 0
fi

mkdir -p ../rocx

../awk/bench.fdr.noselfhit.awk $lookup <(cat $hits) > $out

ls -lh $out
