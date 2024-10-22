#!/bin/bash -e

mkdir -p ../results

svg=../plots/cve_alphas.svg

python3 ../py/plot_cve.py \
  $out \
  reseek_sensitive reseek_aa_myss reseek_aa_myss_nbrmyss reseek_aa_myss_nbrmyss_revnbrdist foldseek

ls -lh $out
