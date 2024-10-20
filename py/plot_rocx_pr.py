#!/usr/bin/python3

####################################################
# Plot results of precision-recall analysis using 
# awk script from foldseek repo
# https://github.com/steineggerlab/foldseek-analysis
####################################################


import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = sys.argv[1]
do_fold = (svg_fn.find("fold") >= 0)

algos = [ "TMalign", "dali", "foldseek", "CE" ]

#        0                1               2                3                4               5
# PREC_FAM        PREC_SFAM       PREC_FOLD       RECALL_FAM      RECALL_SFAM     RECALL_FOLD
def read_analysis(fn):
	f = open(fn)
	precisions = []
	recalls = []
	hdr = f.readline()
	flds = hdr.split('\t')
	assert flds[1] == "PREC_SFAM"
	assert flds[4] == "RECALL_SFAM"
	last_value = None
	first = True
	for line in f:
		flds = line[:-1].split('\t')
		try:
			if do_fold:
				precision= float(flds[2])
				recall = float(flds[5])
			else:
				precision = float(flds[1])
				recall = float(flds[4])
			value = int(precision*100)
		except:
			continue
		if last_value is None or value != last_value:
			precisions.append(precision)
			recalls.append(recall)
			last_value = value
	return precisions, recalls

fig, ax = plt.subplots()
ax.set_xlabel("Recall")
ax.set_ylabel("Precision")

precisions_vec = []
recalls_vec = []

precisions_fold_vec = []
recalls_fold_vec = []

for algo in algos:
	precisions, recalls, = read_analysis("../rocx/" + algo + ".rocx")
	name, kwargs = algo_fmt(algo)
	ax.plot(recalls, precisions, label=name, **kwargs)

ax.legend()
fig.savefig(svg_fn)
