#!/bin/bash -e

for style in cve roc pr
do
	../py/plotter_level_style.py \
	  ../plots/pls.$style.svg \
	  $style \
	  dali \
	  TMalign \
	  foldseek \
	  reseek_fast \
	  reseek_sensitive \
	  reseek_verysensitive
done
