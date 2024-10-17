#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_roc.py \
  ../results/roc_fold.svg \
  dali foldseek tmalign reseek_fast reseek_sensitive
