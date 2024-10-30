#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = "../plots/tm_qual_fpepq.svg"

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

tm_sf_epqs, tm_sf_scores = read_analysis("../analysis_sf/tmalign.txt")
tm_fold_epqs, tm_fold_scores = read_analysis("../analysis_fold/tmalign.txt")

qual_sf_epqs, qual_sf_scores = read_analysis("../analysis_sf/reseek_sensitive_qual.txt")
qual_fold_epqs, qual_fold_scores = read_analysis("../analysis_fold/reseek_sensitive_qual.txt")

ax.plot(tm_sf_scores, tm_sf_epqs, label="TM Superfamily", color="blue")
ax.plot(tm_fold_scores, tm_fold_epqs, label="TM Fold", color="blue", linestyle="dotted")
ax.plot(qual_sf_scores, qual_sf_epqs, label="Qual Superfamily", color="magenta")
ax.plot(qual_fold_scores, qual_fold_epqs, label="Qual Fold", color="magenta", linestyle="dotted")

ax.ticklabel_format(axis='y', style='plain')
ax.set_xlim(0.3, 0.8)
ax.set_ylim(0.01, 1000)
ax.set_yscale('log')
ax.set_xlabel("TM or Qual")
ax.set_ylabel("FPEPQ")
plt.grid()
ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
