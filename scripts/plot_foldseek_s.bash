#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plot_cve_fns.py \
  ../plots/foldseek_s.svg \
  ../analysis/foldseek_s4.sf2.txt \
  ../analysis/foldseek_s6.sf2.txt \
  ../analysis/foldseek_s8.sf2.txt \
  ../analysis/foldseek_s12.sf2.txt \
  ../analysis/foldseek_s14.sf2.txt \
  ../analysis/foldseek.sf2.txt \
  ../analysis/reseek_fast.sf2.txt \
