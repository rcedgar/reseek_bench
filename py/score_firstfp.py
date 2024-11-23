#!/usr/bin/python3

# Improved version of $src/reseek_scop40/scripts/accuracy_analysis.py
# using scop40.py import lib.

import sys
import scop40

tsv_fn = sys.argv[1]
se = sys.argv[2]

qfldnr = 0
tfldnr = 1
scorefldnr = 2

dom2scopid_fn = "../data/dom_scopid.tsv"
sc = scop40.Scop40(se, "sf2", dom2scopid_fn)

sc.eval_file(tsv_fn, qfldnr, tfldnr, scorefldnr, True)
sys.stderr.write(sc.get_summary() + "\n")
for dom in sc.doms:
	score = sc.dom2score_firstfp[dom]
	print(dom, score)
