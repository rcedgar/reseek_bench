#!/usr/bin/python3

import sys
import plotter

all_levels = [ "family", "sf", "half", "ignore", "fold" ]

style = sys.argv[1]
svg_fn = sys.argv[2]
levels = []
algos = []

plus_found = False
for i in range(3, len(sys.argv)):
	a = sys.argv[i]
	if a == "+":
		plus_found = True
		continue
	elif plus_found:
		algos.append(a)
	else:
		levels.append(a)

nr_levels = len(levels)

nr_cols = 2
nr_rows = (nr_levels + nr_cols - 1)//nr_cols

print(f"{style=} {nr_rows=} {nr_cols=} {svg_fn=}")
fig_width = 10
fig_height = 8
p = plotter.Plotter(nr_rows, nr_cols, fig_width, fig_height)

if style == "cve":
	p.plot_cves(levels, algos, svg_fn)
elif style == "roc":
	p.plot_rocs(levels, algos, svg_fn)
elif style == "precision_recall":
	p.plot_precision_recalls(levels, algos, svg_fn)

sys.stderr.write(svg_fn + "\n")
