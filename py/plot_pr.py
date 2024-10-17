#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

svg_fn = sys.argv[1]
algos = sys.argv[2:]

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

def algo_fmt(algo):
	name = algo
	lw = 2
	ls = "solid"
	color = None

	if algo == "reseek_fast":
		name = "Reseek (fast)"
		color = "black"
		lw = 3
		ls = "dotted"
	elif algo == "reseek_sensitive":
		name = "Reseek (sensitive)"
		color = "black"
	elif algo == "blastp":
		name = "BLASTP"
		color = "magenta"
	elif algo == "dali":
		name = "DALI"
	elif algo == "tmalign":
		name = "TM-align"
	elif algo == "foldseek":
		name = "Foldseek"
		lw = 3
		ls = "dotted"

	kwargs = {}
	kwargs["linewidth"] = lw
	kwargs["linestyle"] = ls
	if not color is None:
		kwargs["color"] = color
	return name, kwargs

# ax.set_xlim(0, 0.5)
# ax.set_ylim(0.5, 1)
for algo in algos:
	name, kwargs = algo_fmt(algo)
	fn = "../analysis/" + algo + ".txt"
	precisions, recalls, scores = read_analysis(fn)
	ax.plot(recalls, precisions, label=name, **kwargs)

ax.legend()
fig.savefig(svg_fn)
