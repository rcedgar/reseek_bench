#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/twohit.svg \
  dali foldseek twohit reseek_fast reseek_sensitive
