#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_pr.py \
  ../results/pr.svg \
  dali foldseek tmalign reseek_fast reseek_sensitive reseek_verysensitive
