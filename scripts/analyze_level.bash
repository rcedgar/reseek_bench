#!/bin/bash -e

level=$1
algo=$2
score_or_evalue=$3

if [ x$score_or_evalue == x ] ; then
	echo Missing arg
	exit 1
fi

hits=../sorted_alns/$algo.tsv

if [ ! -s $hits ] ; then
	echo Not found hits=$hits
	exit 1
fi

mkdir -p ../analysis

ana=../analysis/$algo.$level.txt
if [ -s $ana ] ; then
	echo Already done $ana
else
	echo Analyzing $algo
	../py/analyze_hits.py \
	  --input $hits \
	  --type $score_or_evalue \
	  --level $level \
	  > $ana

	ls -lh $ana
fi
