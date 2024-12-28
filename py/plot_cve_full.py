#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = sys.argv[1]
algos = [ "foldseek", "reseek_fast", "reseek_sensitive", "reseek_verysensitive" ]

MIN_EPQ = 0.01
MAX_EPQ = 10

def read_analysis(fn):
	f = open(fn)
	hdr = f.readline()
	assert hdr.startswith("tpr\tepq\tE")
	tprs = []
	epqs = []
	scores = []
	for line in f:
		if line.startswith("tpr_epq1="):
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
ax.set_xticks(np.arange(0.0, 0.55, 0.05))
ax.set_ylim(0.01, 10)
ax.set_xlabel("Sensitivity (true positive rate)")
ax.set_ylabel("False positive errors per query")

for algo in algos:
	name, kwargs = algo_fmt(algo)
	if algo.find('/') > 0:
		fn = algo
	else:
		fn = "../analysis_full/" + algo + ".txt"
	sys.stderr.write(fn + "\n")
	tprs, epqs, scores = read_analysis(fn)
	ax.plot(tprs, epqs, label=name, **kwargs)

ax.legend()
fig.savefig(svg_fn)
sys.stderr.write(svg_fn + "\n")