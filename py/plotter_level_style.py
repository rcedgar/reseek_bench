#!/usr/bin/python3

import sys
import plotter

svg_fn = sys.argv[1]
style = sys.argv[2]
algos = sys.argv[3:]

assert style in [ "cve", "roc", "pr" ]

levels = [ "fam1", "sf2", "sf3", "sf4", "fold5", "fold6" ]

nr_levels = len(levels)
nr_cols = 3
nr_rows = (nr_levels + nr_cols - 1)//nr_cols

fig_width = 13
fig_height = 8
p = plotter.Plotter(nr_rows, nr_cols, fig_width, fig_height)

p.plot_levels(style, levels, algos)

p.fig.savefig(svg_fn)
sys.stderr.write(svg_fn + "\n")
