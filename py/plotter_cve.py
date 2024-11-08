#!/usr/bin/python3

import sys
import plotter

all_levels = [ "family", "sf", "half", "ignore", "fold" ]

svg_fn = sys.argv[1]
levels = []
algos = []

plus_found = False
for i in range(2, len(sys.argv)):
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

print(f"{nr_rows=} {nr_cols=}")
fig_width = 10
fig_height = 10
p = plotter.Plotter(nr_rows, nr_cols, fig_width, fig_height)
p.plot_cves(algos, levels, svg_fn)
sys.stderr.write(svg_fn + "\n")
