#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = sys.argv[1]
algos = sys.argv[2:]

level = "sf"
if svg_fn.find("fold") >= 0:
	level = "fold"
elif svg_fn.find("family") >= 0:
	level = "family"

MIN_EPQ = 0.01
MAX_EPQ = 10

def read_analysis(fn):
	f = open(fn)
	hdr = f.readline()
	assert hdr == "tpr\tepq\tscore\n"
	tprs = []
	epqs = []
	scores = []
	for line in f:
		if line.startswith("epq"):
			break
		flds = line[:-1].split('\t')
		assert len(flds) == 3
		tpr = float(flds[0])
		epq = float(flds[1])
		score = float(flds[2])
		if epq < MIN_EPQ:
			continue
		if epq > MAX_EPQ:
			break

		tprs.append(tpr)
		epqs.append(epq)
		scores.append(score)
	
	return tprs, epqs, scores

fig, ax = plt.subplots()
ax.ticklabel_format(axis='y', style='plain')
ax.set_yscale('log')
ax.yaxis.set_major_formatter(ScalarFormatter())
if level == "family":
	ax.set_xticks(np.arange(0.0, 1.0, 0.1))
else:
	ax.set_xticks(np.arange(0.0, 0.55, 0.05))
ax.set_ylim(0.01, 10)
ax.set_xlabel("Sensitivity (true positive rate)")
ax.set_ylabel("False positive errors per query")

for algo in algos:
	name, kwargs = algo_fmt(algo)
	if level == "fold":
		fn = "../analysis_fold/" + algo + ".txt"
	elif level == "family":
		fn = "../analysis_family/" + algo + ".txt"
	else:
		fn = "../analysis/" + algo + ".txt"
	tprs, epqs, scores = read_analysis(fn)
	ax.plot(tprs, epqs, label=name, **kwargs)

ax.legend()
fig.savefig(svg_fn)
