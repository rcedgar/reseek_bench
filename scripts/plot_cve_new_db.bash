#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_cve.py \
  ../results/cve_new_db.svg \
  dali foldseek tmalign reseek_new_db_fast reseek21_fast reseek_new_db_sensitive reseek21_sensitive
