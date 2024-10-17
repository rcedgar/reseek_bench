#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_roc.py \
  ../results/roc2.svg \
  foldseekTM CLE-sw CE 3Dblast geometricus reseek_sensitive
