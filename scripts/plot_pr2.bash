#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_pr.py \
  ../results/pr2.svg \
  reseek_verysensitive tmalign foldseekTM CE CLE-sw 3Dblast geometricus
