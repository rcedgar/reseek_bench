#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/cve_new_vs_21.svg \
  dali foldseek tmalign reseek21_fast reseek_fast reseek21_sensitive reseek_sensitive reseek21_verysensitive reseek_verysensitive
