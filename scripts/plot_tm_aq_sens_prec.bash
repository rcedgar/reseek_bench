#!/bin/bash -e

svg=../plots/tm_aq_sens_prec.svg
python3 ../py/plot_tm_aq_sens_prec.py $svg $x
ls -lh $svg
