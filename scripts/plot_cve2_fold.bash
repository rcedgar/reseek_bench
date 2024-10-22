#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/roc2_fold.svg \
  foldseekTM CLE-sw CE 3Dblast geometricus reseek_fast
