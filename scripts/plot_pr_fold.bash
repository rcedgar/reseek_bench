#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_pr.py \
  ../results/pr_fold.svg \
   reseek_verysensitive  reseek_sensitive  reseek_fast tmalign foldseek dali
