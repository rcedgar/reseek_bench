#!/usr/bin/python3

import sys
import plotter

svg_fn = sys.argv[1]
algos = sys.argv[2:]

nr_cols = 3
nr_rows = 1

fig_width = 10
fig_height = 3
p = plotter.Plotter(nr_rows, nr_cols, fig_width, fig_height)

p.plot_cve("family", algos, True)
p.plot_roc("family", algos, False)
p.plot_precision_recall("family", algos, False)
p.get_ax().legend()

p.fig.savefig(svg_fn)
sys.stderr.write(svg_fn + "\n")
