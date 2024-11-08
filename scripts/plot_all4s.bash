#!/bin/bash -e

mkdir -p ../plots

for style in cve roc precision_recall
do
	python3 ../py/plotter_any.py \
	  $style \
	  ../plots/$style.4.svg \
	  sf \
	  half \
	  ignore \
	  fold \
	  + \
	  dali \
	  foldseek \
	  TMalign \
	  reseek_fast \
	  reseek_sensitive \
	  reseek_verysensitive
done
