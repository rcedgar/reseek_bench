#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = "../plots/eval_eval.svg"

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

fs_epqs, fs_evalues = read_analysis("../analysis_sf/foldseek.txt")
rs_epqs, rs_evalues = read_analysis("../analysis_sf/reseek_sensitive.txt")

name, kwargs = algo_fmt("foldseek")
ax.plot(fs_evalues, fs_epqs, label="Foldseek", **kwargs)

name, kwargs = algo_fmt("reseek_sensitive")
ax.plot(rs_evalues, rs_epqs, label="Reseek-sensitive", **kwargs)

ax.ticklabel_format(axis='y', style='plain')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Reported E-value")
ax.set_ylabel("Measured FPEPQ")
plt.grid()
ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
