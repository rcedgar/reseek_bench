#!/bin/bash -e

algo=$1
score_or_evalue=$2

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

ana=../analysis/$1.txt
if [ -s $ana ] ; then
	echo Already done $ana
else
	echo Analyzing $algo
	../py/analyze_hits.py \
	  --input $hits \
	  --type $score_or_evalue \
	  --level sf \
	  > $ana

	ls -lh $ana
fi
