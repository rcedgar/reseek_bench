#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = sys.argv[1]
algos = sys.argv[2:]

do_fold = (svg_fn.find("fold") >= 0)

def read_analysis(fn):
	f = open(fn)
	precisions = []
	recalls = []
	scores = []
	found = False
	for line in f:
		if line.startswith("precision"):
			found = True
			continue
		if line.startswith("SEPQ0.1="):
			break
		if found:
			flds = line[:-1].split('\t')
			assert len(flds) == 3
			precision = float(flds[0])
			recall = float(flds[1])
			score = float(flds[2])
			precisions.append(precision)
			recalls.append(recall)
			scores.append(score)
	assert found
	return precisions, recalls, scores

fig, ax = plt.subplots()
ax.set_xlabel("Recall")
ax.set_ylabel("Precision")

for algo in algos:
	name, kwargs = algo_fmt(algo)
	if do_fold:
		fn = "../analysis_fold/" + algo + ".txt"
	else:
		fn = "../analysis/" + algo + ".txt"
	precisions, recalls, scores = read_analysis(fn)
	ax.plot(recalls, precisions, label=name, **kwargs)

ax.legend()
fig.savefig(svg_fn)
