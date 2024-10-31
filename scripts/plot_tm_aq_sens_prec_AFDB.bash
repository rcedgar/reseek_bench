#!/bin/bash -e

for x in 1 10 100 1000
do
	svg=../plots/tm_aq_sens_prec_AFDB_$x.svg
	python3 ../py/plot_tm_aq_sens_prec_AFDB.py $svg $x
	ls -lh $svg
done
