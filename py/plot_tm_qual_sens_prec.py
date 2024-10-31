#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = "../plots/tm_qual_sens_prec.svg"

qual_fn = "../bin_scores/qual.tsv"
tm_fn = "../bin_scores/tm.tsv"

#   0       1       2     3             4
# tpr     epq     fpr     precision       score
# 0.01    0       0       1				2.308e-21

def read_analysis(fn):
	f = open(fn)
	hdr = f.readline()
	assert hdr.startswith("TM\tTP\tFP\tSens\tPrec")
	tmv = []
	sensv = []
	precv = []
	for line in f:
		flds = line[:-1].split('\t')
		assert len(flds) == 6
		TM = float(flds[0])
		if TM > 0.9:
			continue
		if TM < 0.3:
			break
		sens = float(flds[3])
		prec = float(flds[4])

		tmv.append(TM)
		sensv.append(sens)
		precv.append(prec)
	return tmv, sensv, precv

fig, ax = plt.subplots()

qual_tmv, qual_sensv, qual_precv = read_analysis(qual_fn)
tm_tmv, tm_sensv, tm_precv = read_analysis(tm_fn)

ax.figure.set_size_inches(6, 3.7)
ax.plot(qual_tmv, qual_sensv, label="Sens. AQ", color="black")
ax.plot(qual_tmv, qual_precv, label="Prec. AQ", color="black", linestyle="dashed")

ax.plot(tm_tmv, tm_sensv, label="Sens. TM", color="magenta")
ax.plot(tm_tmv, tm_precv, label="Prec. TM", color="magenta", linestyle="dashed")
ax.ticklabel_format(axis='y', style='plain')
ax.set_xlabel("TM or AQ")
ax.set_ylabel("Sens. or Prec.")
plt.grid()
ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
