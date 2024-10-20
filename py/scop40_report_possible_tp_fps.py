#!/usr/bin/python3

import sys
import scop40

first = True
for level in [ "sf", "fold" ]:
	sc = scop40.Scop40("e", level, "../data/dom_scopid.tsv")
	NQ = len(sc.doms)
	nr_pairs = NQ*(NQ - 1)
	if first:
		print("nr_queries = ", NQ)
		print("nr_pairs = ", nr_pairs)
		first = False
	print(level, " NT = ", sc.NT)
	print(level, " NF = ", sc.NF)
