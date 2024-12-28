#!/bin/bash -e

mkdir -p ../time_mem

cd ../foldseek_search_full

time_mem_threads.py *.t*.time \
  > ../time_mem/foldseek.tsv

cd ../reseek_search_full

time_mem_threads.py fast.t*.time \
  > ../time_mem/fast.tsv

time_mem_threads.py sensitive.t*.time \
  > ../time_mem/sensitive.tsv

cd ../time_mem

echo
echo === Foldseek ===
columns.py foldseek.tsv

echo
echo === Fast ===
columns.py fast.tsv

echo
echo === Sensitive ===
columns.py sensitive.tsv
