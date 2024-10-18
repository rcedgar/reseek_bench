#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = sys.argv[1]
fn_dali = "../rocxfdr/dali.rocxfdr"
fn_tmalign = "../rocxfdr/TMalign.100.rocxfdr"

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
	for line in f:
		flds = line[:-1].split('\t')
		precision = float(flds[1])
		recall = float(flds[4])
		precisions.append(precision)
		recalls.append(recall)
	return precisions, recalls

fig, ax = plt.subplots()
ax.set_xlabel("Recall")
ax.set_ylabel("Precision")

name, kwargs = algo_fmt("dali")
precisions, recalls = read_analysis(fn_dali)
ax.plot(recalls, precisions, label=name, **kwargs)

name, kwargs = algo_fmt("tmalign")
precisions, recalls = read_analysis(fn_tmalign)
ax.plot(recalls, precisions, label=name, **kwargs)

ax.legend()
fig.savefig(svg_fn)
