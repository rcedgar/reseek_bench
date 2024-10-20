#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_roc.py \
  ../results/roc_alphas.svg \
  reseek_sensitive reseek_aa_myss reseek_aa_myss_nbrmyss reseek_aa_myss_nbrmyss_revnbrdist foldseek

ls -lh ../results/roc_alphas.svg
