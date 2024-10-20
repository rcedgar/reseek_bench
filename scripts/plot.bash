#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plot.py \
  best \
  dali foldseek tmalign reseek_fast reseek_sensitive reseek_verysensitive
