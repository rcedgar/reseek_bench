#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_rocxfdr_pr.py \
  ../results/rocxfdr_pr.svg
