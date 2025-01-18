#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/cve_big_vs_21.svg \
  dali foldseek tmalign reseek21_fast reseek_bigfast reseek21_sensitive reseek_bigsensitive reseek21_verysensitive reseek_bigverysensitive
