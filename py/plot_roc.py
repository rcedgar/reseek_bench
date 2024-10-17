#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

svg_fn = sys.argv[1]
algos = sys.argv[2:]

do_fold = (svg_fn.find("fold") >= 0)
print("do_fold", do_fold)

MIN_EPQ = 0.01
MAX_EPQ = 10

def read_analysis(fn):
	f = open(fn)
	hdr = f.readline()
	assert hdr == "tpr\tepq\tscore\n"
	tprs = []
	epqs = []
	scores = []
	for line in f:
		if line.startswith("epq"):
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
ax.set_xticks(np.arange(0.0, 0.5, 0.05))
ax.set_ylim(0.01, 10)
ax.set_xlabel("Sensitivity (true positive rate)")
ax.set_ylabel("False positive errors per query")

def algo_fmt(algo):
	name = algo
	lw = 2
	ls = "solid"
	color = None

	if algo == "reseek_fast":
		name = "Reseek v2.0 (fast)"
		color = "black"
		lw = 3
		ls = "dotted"
	elif algo == "reseek_v1.2":
		name = "Reseek v1.2"
		color = "gray"
	elif algo == "reseek_sensitive":
		name = "Reseek v2.0 (sensitive)"
		color = "black"
	elif algo == "blastp":
		name = "BLASTP"
		ls = "dotted"
		color = "lightgreen"
	elif algo == "dali":
		name = "DALI"
		color = "skyblue"
	elif algo == "tmalign":
		name = "TM-align"
		color = "magenta"
	elif algo == "foldseek":
		name = "Foldseek"
		lw = 3
		ls = "dotted"
		color = "orange"

	kwargs = {}
	kwargs["linewidth"] = lw
	kwargs["linestyle"] = ls
	if not color is None:
		kwargs["color"] = color
	return name, kwargs

for algo in algos:
	name, kwargs = algo_fmt(algo)
	if do_fold:
		fn = "../analysis_fold/" + algo + ".txt"
	else:
		fn = "../analysis/" + algo + ".txt"
	tprs, epqs, scores = read_analysis(fn)
	ax.plot(tprs, epqs, label=name, **kwargs)

ax.legend()
fig.savefig(svg_fn)
