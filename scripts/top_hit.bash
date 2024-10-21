#!/bin/bash -e

algo=$1
se=$2
level=$3

mkdir -p ../top_hit

out=../top_hit/$algo.$level.tsv

if [ -s $out ] ; then
	echo Already done $out
	exit 0
fi

../py/top_hits_eval.py \
  ../sorted_alns/$algo.tsv \
  $se \
  $level \
  $out

tail -n5 $out
ls -lh $out
