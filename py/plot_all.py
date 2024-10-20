#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

# level = sys.argv[1]
# assert level == "family" or level == "sf" or level == "fold"
algos = sys.argv[1:]

svg_fn = "../plots/all.svg"

MIN_EPQ = 0.01
MAX_EPQ = 10

def read_analysis(fn):
	f = open(fn)
	hdr = f.readline()
	#                0	1	2	3			4
	if hdr != "tpr	epq	fpr	precision	score\n":
		sys.stderr.write("hdr=%s\n" % hdr)
		sys.stderr.write("fn=%s\n" % fn)
		assert False
	tprs = []
	epqs = []
	fprs = []
	precisions = []
	scores = []
	for line in f:
		if line.startswith("SEPQ"):
			break
		flds = line[:-1].split('\t')
		assert len(flds) == 5
		tpr = float(flds[0])
		epq = float(flds[1])
		fpr = float(flds[2])
		precision = float(flds[3])
		score = float(flds[4])

		tprs.append(tpr)
		fprs.append(fpr)
		epqs.append(epq)
		precisions.append(precision)
		scores.append(score)
	
	return tprs, epqs, fprs, precisions, scores

# fig = plt.figure()

nr_algos = len(algos)
nr_rows = 3
nr_cols = 3
fig, axs = plt.subplots(ncols=nr_rows, nrows=nr_rows, \
	figsize=(20, 20), layout="constrained")
row = 0
col = 0

ax_idx = 0
for level in [ "family", "sf", "fold" ]:
	strlevel = level
	if level == "sf":
		strlevel = "superfamily"
	tpr_vec = []
	fpr_vec = []
	epq_vec = []
	precision_vec = []

	for algo in algos:
		fn = "../analysis_%s/%s.txt" % (level, algo)
		tprs, epqs, fprs, precisions, scores = read_analysis(fn)
		n = len(tprs)
		assert len(epqs) == n
		assert len(fprs) == n
		assert len(precisions) == n
		assert len(scores) == n

		tpr_vec.append(tprs)
		fpr_vec.append(fprs)
		epq_vec.append(epqs)
		precision_vec.append(precisions)

	##########################################################
	# Precision-recall
	##########################################################
	sys.stderr.write(level + " prec-recall\n")
#	fig, ax = plt.subplots()
	ax = axs[row, col]
	col += 1
	if col >= nr_cols:
		col = 0
		row += 1
		if row > nr_rows:
			sys.stderr.write("WARNING size\n")
			break

	ax.set_title("Precision-recall %s" % strlevel)
	ax.ticklabel_format(axis='y', style='plain')
	ax.set_xlabel("Recall (fraction of all homologs found)")
	ax.set_ylabel("Precision (fraction hits correct)")

	for idx, algo in enumerate(algos):
		name, kwargs = algo_fmt(algo)
		ax.plot(tpr_vec[idx], precision_vec[idx], label=name, **kwargs)

	ax.legend()

	##########################################################
	# ROC
	##########################################################
	sys.stderr.write(level + " ROC\n")
	sys.stderr.write(svg_fn + "\n")
#	fig, ax = plt.subplots()
	ax = axs[row, col]
	col += 1
	if col >= nr_cols:
		col = 0
		row += 1
		if row > nr_rows:
			sys.stderr.write("WARNING size\n")
			break
	ax.set_title("ROC %s" % strlevel)
	ax.ticklabel_format(axis='y', style='plain')
	ax.set_xlabel("FPR (fraction non-homolog hits)")
	ax.set_ylabel("TPR (fraction of all homologs found)")

	for idx, algo in enumerate(algos):
		name, kwargs = algo_fmt(algo)
		ax.plot(fpr_vec[idx], tpr_vec[idx], label=name, **kwargs)

	ax.legend()

	##########################################################
	# Sensitivity-error
	##########################################################
	sys.stderr.write(level + " sens-err\n")
	sys.stderr.write(svg_fn + "\n")
#	fig, ax = plt.subplots()
	ax = axs[row, col]
	col += 1
	if col >= nr_cols:
		col = 0
		row += 1
		if row > nr_rows:
			sys.stderr.write("WARNING size\n")
			break
	ax.set_title("Sensitivity-error %s" % strlevel)
	ax.ticklabel_format(axis='y', style='plain')
	ax.set_yscale('log')
	ax.yaxis.set_major_formatter(ScalarFormatter())
	if level == "family":
		ax.set_xticks(np.arange(0.0, 1.0, 0.1))
	else:
		ax.set_xticks(np.arange(0.0, 0.55, 0.05))
	ax.set_ylim(0.01, 10)
	ax.set_xlabel("Sensitivity (fraction of all homologs found)")
	ax.set_ylabel("False positive errors per query")

	for idx, algo in enumerate(algos):
		name, kwargs = algo_fmt(algo)
		tprs = tpr_vec[idx]
		epqs = epq_vec[idx]
		n = len(tprs)
		assert len(epqs) == n

		xs = []
		ys = []
		for i in range(n):
			tpr = tprs[i]
			epq = epqs[i]
			if epq >= MIN_EPQ and epq <= MAX_EPQ:
				xs.append(tpr)
				ys.append(epq)

		ax.plot(xs, ys, label=name, **kwargs)

	ax.legend()
fig.savefig(svg_fn)
