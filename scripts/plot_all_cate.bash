#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plot_all_cate.py \
  dali foldseek TMalign reseek_fast reseek_sensitive reseek_verysensitive
