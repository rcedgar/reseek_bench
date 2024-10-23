#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plot_cate.py \
  ../plots/cate_sf.svg \
  dali foldseek TMalign reseek_fast reseek_sensitive reseek_verysensitive
