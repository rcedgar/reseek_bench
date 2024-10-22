#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

# level = sys.argv[1]
# assert level == "family" or level == "sf" or level == "fold"
algos = sys.argv[1:]

svg_fn = "../plots/all_top_hit.svg"

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

nr_algos = len(algos)
nr_rows = 1
nr_cols = 3
fig, axs = plt.subplots(ncols=nr_cols, nrows=nr_rows, \
	figsize=(15, 5), layout="constrained")
row = 0
col = 0

ax_idx = 0
for level in [ "family", "sf", "fold" ]:
	strlevel = level
	if level == "sf":
		strlevel = "superfamily"
	tpr_vec = []
	fpr_vec = []
	for algo in algos:
		fn = "../top_hit/%s.%s.tsv" % (algo, level)
		tprs, fprs = read_analysis(fn)
		n = len(tprs)
		assert len(fprs) == n

		tpr_vec.append(tprs)
		fpr_vec.append(fprs)

	sys.stderr.write(level + " top-hit\n")
#	fig, ax = plt.subplots()
	ax = axs[row]
	row += 1

	ax.set_title("Top-hit %s" % strlevel)
	ax.ticklabel_format(axis='y', style='plain')
	ax.set_yscale('log')
	ax.set_xlabel("TCR")
	ax.set_ylabel("FCR")

	for idx, algo in enumerate(algos):
		name, kwargs = algo_fmt(algo)
		ax.plot(tpr_vec[idx], fpr_vec[idx], label=name, **kwargs)

	ax.legend()
fig.savefig(svg_fn)
