#!/bin/bash -e

for mode in fast sensitive verysensitive
do
	  rm -f ../alns/reseek_$mode.tsv \
	  rm -f ../reseek_log/$mode.log
	  rm -f ../sorted_alns/reseek_$mode.tsv
	  rm -f ../analysis/reseek_$mode.*
done
