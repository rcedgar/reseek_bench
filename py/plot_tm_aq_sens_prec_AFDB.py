#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

svg_fn = sys.argv[1] # "../plots/tm_qual_sens_prec.svg"

AFDB_fp_factor = 1
if len(sys.argv) > 1:
	AFDB_fp_factor = float(sys.argv[2])
sys.stderr.write("AFDB_fp_factor = %.3g\n" % AFDB_fp_factor)

NT = 454766 # SCOP40 SF

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
		if TM > 0.8:
			continue
		if TM < 0.4:
			break
		tp = int(flds[1])
		fp = int(flds[2])
		fp *= AFDB_fp_factor

		prec = 0
		fpr = 0
		n = tp + fp
		if n > 0:
			prec = tp/n
			fpr = fp/n
		sens = tp/NT

		tmv.append(TM)
		sensv.append(sens)
		precv.append(prec)

		if TM == 0.5 or TM == 0.6 or TM == 0.8:
			s = fn
			s += "\tAFx=%d" % AFDB_fp_factor
			s += "\t%.2f" % TM
			s += "\t%.3g" % prec
			# sys.stderr.write(s + "\n")

	return tmv, sensv, precv

fig, ax = plt.subplots()

qual_tmv, qual_sensv, qual_precv = read_analysis(qual_fn)
tm_tmv, tm_sensv, tm_precv = read_analysis(tm_fn)

ax.figure.set_size_inches(2.5, 2)
ax.set_ylim(0, 1)
ax.plot(qual_tmv, qual_sensv, label="Sens. AQ", color="black")
ax.plot(qual_tmv, qual_precv, label="Prec. AQ", color="black", linestyle="dashed")

ax.plot(tm_tmv, tm_sensv, label="Sens. TM", color="magenta")
ax.plot(tm_tmv, tm_precv, label="Prec. TM", color="magenta", linestyle="dashed")
ax.ticklabel_format(axis='y', style='plain')
ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8])
ax.set_xlabel("TM or AQ")
ax.set_ylabel("Sens. or Prec.")
plt.grid()
# ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
