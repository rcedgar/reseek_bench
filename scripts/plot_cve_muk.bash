#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/roc_muk.svg \
  dali foldseek tmalign reseek_fast reseek_sensitive reseek_muk
