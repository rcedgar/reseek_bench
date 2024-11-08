#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = "../plots/eval_evals.svg"

#   0       1       2     3             4
# tpr     epq     fpr     precision       score
# 0.01    0       0       1				2.308e-21

def read_analysis(fn):
	f = open(fn)
	hdr = f.readline()
	assert hdr.startswith("tpr\tepq")
	epqs = []
	evalues = []
	for line in f:
		if line.startswith("SEPQ"):
			continue
		flds = line[:-1].split('\t')
		assert len(flds) == 5
		epq = float(flds[1])
		if epq < 0.01:
			continue
		evalue = float(flds[4])

		epqs.append(epq)
		evalues.append(evalue)
	
	return epqs, evalues

# fig = plt.figure()

fig, ax = plt.subplots()

for algo in [ "foldseek", "reseek_sensitive" ]:
	for level in [ "sf", "half", "fold" ]:
		fs_epqs, fs_evalues = read_analysis("../analysis_" + level + "/" + algo + ".txt")
		rs_epqs, rs_evalues = read_analysis("../analysis_" + level + "/" + algo + ".txt")

		kwargs = {}
		if algo == "foldseek":
			name = "Foldseek"
			kwargs["color"] = "orange"
		elif algo == "reseek_sensitive":
			name = "Reseek (sensitive)"
			kwargs["color"] = "black"

		kwargs["linewidth"] = 3
		if level == "sf":
			kwargs["linestyle"] = "dashed"
		elif level == "half":
			kwargs["linestyle"] = "solid"
		elif level == "fold":
			kwargs["linestyle"] = "dotted"

		ax.plot(fs_evalues, fs_epqs, label=name +" / "+level, **kwargs)

ax.ticklabel_format(axis='y', style='plain')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Reported E-value")
ax.set_ylabel("Measured FPEPQ")
plt.grid()
ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
