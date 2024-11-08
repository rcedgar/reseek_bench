#!/usr/bin/python3

import sys
import scop40
import argparse

tsv_fn = sys.argv[1]
score_or_evalue = sys.argv[2]
level = sys.argv[3]
out_fn = sys.argv[4]
dom2scopid_fn = "../data/dom_scopid.tsv"

assert level == "family" or level == "sf" or level == "fold" or level == "ignore" or level == "half"

if score_or_evalue == "score":
	se = "s"
elif score_or_evalue == "evalue":
	se = "e"
else:
	assert False

qfldnr = 0
tfldnr = 1
scorefldnr = 2

assert qfldnr >= 0
assert tfldnr >= 0
assert qfldnr != tfldnr

sc = scop40.Scop40(se, level, dom2scopid_fn)

sc.read_file(tsv_fn, qfldnr, tfldnr, scorefldnr)
sc.eval_sorted(sc.qs, sc.ts, sc.scores)
sc.top_hit_report(out_fn)
