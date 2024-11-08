#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plotter_family.py \
  ../plots/family.svg \
  dali \
  foldseek \
  TMalign \
  reseek_fast \
  reseek_sensitive \
  reseek_verysensitive
