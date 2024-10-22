#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../plots/other_cve_sf.svg \
   tmalign foldseek foldseekTM CLE-sw CE 3Dblast geometricus reseek_sensitive
