#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/afdbr.svg \
  dali foldseek foldseek_afdbr foldseek_afdbr_ms4000 reseek_fast reseek_sensitive
