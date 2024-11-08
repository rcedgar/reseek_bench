#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plot_cate.py \
  ../plots/cate_half.svg \
  dali foldseek TMalign reseek_fast reseek_sensitive reseek_verysensitive
