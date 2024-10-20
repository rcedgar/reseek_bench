#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plot_all.py \
  dali foldseek tmalign reseek_fast reseek_sensitive reseek_verysensitive
