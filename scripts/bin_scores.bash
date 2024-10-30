#!/bin/bash -e

mkdir -p ../bin_scores
cd ../bin_scores

python3 ../py/bin_scores.py ../sorted_alns/reseek_verysensitive_qual.tsv > qual.tsv
python3 ../py/bin_scores.py ../sorted_alns/TMalign.tsv > tm.tsv
