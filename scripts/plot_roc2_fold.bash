#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_roc.py \
  ../results/roc2_fold.svg \
  foldseekTM CLE-sw CE 3Dblast geometricus reseek_fast
