#!/bin/bash -e

mkdir -p ../alns ../sorted_alns ../time ../reseek_log

reseek=$src/reseek/github_releases/reseek-v2.1-linux-x86

for mode in verysensitive # fast sensitive
do
	/bin/time -v -o ../time/reseek21_$mode \
	$reseek \
	  -search ../data/scop40.cal \
	  -$mode \
	  -output ../alns/reseek21_$mode.tsv \
	  -columns query+target+evalue \
	  -log ../reseek_log/$mode.21.log

	sort -gk3 ../alns/reseek21_$mode.tsv \
	  > ../sorted_alns/reseek21_$mode.tsv
done
