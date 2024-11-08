#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from algo_fmt import algo_fmt

# level = sys.argv[1]
# assert level == "family" or level == "sf" or level == "fold"
svg_fn = sys.argv[1]
algos = sys.argv[2:]

level = "sf"
if svg_fn.find("fold") >= 0:
	level = "fold"
elif svg_fn.find("family") >= 0:
	level = "family"
elif svg_fn.find("half") >= 0:
	level = "half"
elif svg_fn.find("ignore") >= 0:
	level = "ignore"
sys.stderr.write("level=" + level + "\n")

def read_analysis(fn):
	f = open(fn)
	tprs = []
	fprs = []
	for line in f:
		flds = line[:-1].split('\t')
		assert len(flds) == 5
		tpr = float(flds[3])
		fpr = float(flds[4])

		tprs.append(tpr)
		fprs.append(fpr)
	
	return tprs, fprs

# fig = plt.figure()

nr_algos = len(algos)
fig, ax = plt.subplots()

ax_idx = 0

strlevel = level
if level == "sf":
	strlevel = "superfamily"
tpr_vec = []
fpr_vec = []
for algo in algos:
	fn = "../top_hit/%s.%s.tsv" % (algo, level)
	tprs, fprs = read_analysis(fn)
	n = len(tprs)
	assert len(fprs) == n

	tpr_vec.append(tprs)
	fpr_vec.append(fprs)

sys.stderr.write(level + " top-hit\n")

#	ax.set_title("Top-hit %s" % strlevel)
ax.ticklabel_format(axis='y', style='plain')
ax.set_yscale('log')
ax.set_ylim(1e-4, 0.1)
ax.set_xlabel("Category coverage")
ax.set_ylabel("Category errors per query")

for idx, algo in enumerate(algos):
	name, kwargs = algo_fmt(algo)
	ax.plot(tpr_vec[idx], fpr_vec[idx], label=name, **kwargs)

ax.legend()

sys.stderr.write(svg_fn + "\n")
fig.savefig(svg_fn)
