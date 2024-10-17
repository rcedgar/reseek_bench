#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_roc.py \
  ../results/roc_v12.svg \
  dali foldseek tmalign reseek_v1.2 reseek_fast reseek_sensitive
