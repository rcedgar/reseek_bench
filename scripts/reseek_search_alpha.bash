#!/bin/bash -e

params=$1
name=$2

if [ x$name == x ] ; then
	echo Missing name
	exit 1
fi

mkdir -p ../alns ../sorted_alns ../time

/bin/time -v -o ../time/reseek_$name \
reseek \
  -search ../data/scop40.cal \
  -params $params \
  -sensitive \
  -output ../alns/reseek_$name.tsv \
  -columns query+target+evalue

sort -gk3 ../alns/reseek_$name.tsv \
  > ../sorted_alns/reseek_$name.tsv
