#!/bin/bash -e

mkdir -p ../results

python3 ../py/plot_rocx_pr.py \
  ../results/rocx_pr.svg \

python3 ../py/plot_rocx_pr.py \
  ../results/rocx_pr_fold.svg
