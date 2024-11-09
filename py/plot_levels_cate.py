#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = sys.argv[1]
algos = sys.argv[2:]


def read_analysis(fn):
	f = open(fn)
	tprs = []
	fprs = []
	for line in f:
		flds = line[:-1].split('\t')
		assert len(flds) == 5
		tpr = float(flds[3])
		fpr = float(flds[4])

		tprs.append(tpr)
		fprs.append(fpr)
	
	return tprs, fprs

# fig = plt.figure()

levels = [ "fam1", "sf2", "sf3", "sf4", "fold5", "fold6" ]

nr_levels = len(levels)
nr_cols = 3
nr_rows = (nr_levels + nr_cols - 1)//nr_cols

fig_width = 13
fig_height = 8

fig, axs = plt.subplots(ncols=nr_cols, nrows=nr_rows, \
	figsize=(fig_width, fig_height), layout="constrained")
row = 0
col = 0

ax_idx = 0
for level in levels:
	print(row, col)
	ax = axs[row, col]
	col += 1
	if col >= nr_cols:
		row += 1
		col = 0
	for algo in algos:
		fn = "../top_hit/%s.%s.tsv" % (algo, level)
		tprs, fprs = read_analysis(fn)
		n = len(tprs)
		assert len(fprs) == n

		ax.set_title("CatE %s" % level)
#		ax.ticklabel_format(axis='y', style='plain')
		ax.set_yscale('log')
		ax.set_xlabel("Category coverage")
		ax.set_ylabel("Category errors per query")

		name, kwargs = algo_fmt(algo)
		ax.plot(tprs, fprs, label=name, **kwargs)

	ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
