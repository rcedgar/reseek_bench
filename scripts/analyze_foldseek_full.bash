#!/bin/bash -e

cd ../foldseek_search_full
mkdir -p ../analysis_full

scop40_full_length_ana.py \
  hits_sorted.tsv \
  > ../analysis_full/reseek.txt
