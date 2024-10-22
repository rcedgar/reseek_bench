#!/bin/bash -e

mkdir -p ../plots

python3 ../py/plot_cve.py \
  ../plots/cve_alphas.svg \
  foldseek reseek_aa_myss  reseek_aa_myss_nbrmyss  reseek_aa_myss_nbrmyss_revnbrdist reseek_sensitive
