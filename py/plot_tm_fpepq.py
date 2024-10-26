#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = "../plots/tm_fpepq.svg"

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

sf_epqs, sf_scores = read_analysis("../analysis_sf/tmalign.txt")
fold_epqs, fold_scores = read_analysis("../analysis_fold/tmalign.txt")

ax.plot(sf_scores, sf_epqs, label="Superfamily")
ax.plot(fold_scores, fold_epqs, label="Fold")

ax.ticklabel_format(axis='y', style='plain')
ax.set_xlim(0.4, 1.0)
ax.set_ylim(1e-5, 1000)
ax.set_yscale('log')
ax.set_xlabel("TM-score")
ax.set_ylabel("Measured FPEPQ")
plt.grid()
ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
