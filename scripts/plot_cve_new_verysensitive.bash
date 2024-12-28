#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/cve_new_verysensitive.svg \
  dali foldseek tmalign reseek21_verysensitive reseek_new_verysensitive
