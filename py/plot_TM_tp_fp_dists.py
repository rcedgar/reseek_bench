#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

tsv_fn = "../results/TM_tp_fp_dists.tsv"
svg_fn = "../plots/TM_tp_fp_dists.svg"

BINS = 100

domv = []
tpv = []
fpv = []
f = open(tsv_fn)
hdr = f.readline()[:-1]
hdr_flds = hdr.split('\t')
assert hdr_flds[0] == "TM"
nr_doms = (len(hdr_flds) - 1)//2

doms = []
tpv = []
fpv = []
nv = []
for dom_idx in range(nr_doms):
	fldTP = hdr_flds[2*dom_idx + 1]
	fldFP = hdr_flds[2*dom_idx + 2]
	assert fldTP.endswith("-TP")
	dom = fldTP.split('-')[0]
	assert fldFP == dom + "-FP"
	doms.append(dom)
	tpv.append([])
	fpv.append([])
	nv.append([])

assert len(tpv) == nr_doms
assert len(fpv) == nr_doms

TMs = []
TM = 0
for line in f:
	flds = line[:-1].split('\t')
	assert len(flds) == 1 + 2*nr_doms
	# TM = float(flds[0])
	TM += 1
	TMs.append(TM)
	for dom_idx in range(nr_doms):
		ntp = int(flds[2*dom_idx + 1])
		nfp = int(flds[2*dom_idx + 2])
		n = ntp + nfp
		tpv[dom_idx].append(ntp)
		fpv[dom_idx].append(nfp)
		nv[dom_idx].append(n)

nr_doms = 3
nr_rows = 2
nr_cols = 3
fig, axs = plt.subplots(ncols=nr_cols, nrows=nr_rows, \
	figsize=(20, 20), layout="constrained")

x = []
for b in range(BINS+1):
	x.append("%.3f" % (b/100.0))

col = 0
row = 0
for dom_idx in [1, 0, 2]:
	ax = axs[row, col]
	ax.set_xlim(10, 80)
	ax.set_ylim(0, 50)
	tps = tpv[dom_idx]
	fps = fpv[dom_idx]
	ax.set_title(doms[dom_idx])
	ax.bar(x, tps, color="limegreen", width=1)
	ax.bar(x, fps, bottom=tps, color="magenta", width=1)
	ax.get_xaxis().set_visible(False)
	ax.figure.set_size_inches(30, 6)
	ax.tick_params(labelsize=14)
	col += 1

row = 1
col = 0
for dom_idx in [1, 0, 2]:
	ax = axs[row, col]
	ax.set_xlim(10, 80)
	ns = nv[dom_idx]
	ax.set_title(doms[dom_idx])
	ax.bar(x, ns, color="magenta", width=1)
	ax.get_xaxis().set_visible(False)
	ax.figure.set_size_inches(20, 6)
	ax.tick_params(labelsize=14)
	col += 1

fig.savefig(svg_fn)
