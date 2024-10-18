#!/usr/bin/python3

# Improved version of $src/reseek_scop40/scripts/accuracy_analysis.py
# using scop40.py import lib.

import sys
import scop40
import argparse

Usage = "Usage TODO"

MAX_EVALUE = 0.1

AP = argparse.ArgumentParser(description = Usage)

AP.add_argument("--input", required=False, default="/dev/stdin", help="Hits tsv file (default stdin)")
AP.add_argument("--fields", required=False, default="1,2,3", help="query,target,score (default 1,2,3)")
AP.add_argument('--lookup', default="../data/dom_scopid.tsv", help="Lookup file (default ../data/scop_lookup.fix.tsv)")

Args = AP.parse_args()

tsv_fn = Args.input
dom2scopid_fn = Args.lookup
se = "e"

fs = Args.fields.split(",")
if len(fs) != 3:
     assert False, "--fields must be 3 comma-separated 1-based field numbers"

qfldnr = int(fs[0]) - 1
tfldnr = int(fs[1]) - 1
scorefldnr = int(fs[2]) - 1

assert qfldnr >= 0
assert tfldnr >= 0
assert qfldnr != tfldnr

#	def __init__(self, se, level, dom2scopid_fn):
sc = scop40.Scop40(se, "fold", dom2scopid_fn)

# def eval_file(self, fn, qfldnr, tfldnr, scorefldnr, is_sorted):
sc.read_file(tsv_fn, qfldnr, tfldnr, scorefldnr)
sc.eval_sorted(sc.qs, sc.ts, sc.scores)

qs = sc.qs
ts = sc.ts
evalues = sc.scores
tps = sc.tps

done_sfs = set()

selected_doms = set()
dom2hits = {}

n = len(qs)
assert len(ts) == n
assert len(evalues) == n
assert len(tps) == n
for hit_idx in range(n):
    evalue = evalues[hit_idx]
    if evalue > MAX_EVALUE:
        continue
    q = qs[hit_idx]
    t = ts[hit_idx]
    q = q.split('/')[0]
    qsf = sc.dom2sf[q]

    if not qsf in done_sfs:
        done_sfs.add(qsf)
        selected_doms.add(q)
        dom2hits[q] = []

    if q in selected_doms:
        if len(dom2hits[q]) < 10:
            dom2hits[q].append(hit_idx)

for q in selected_doms:
    qsf = sc.dom2sf[q]
    qfold = sc.dom2fold[q]
    for idx in dom2hits[q]:
        t = sc.ts[idx]
        evalue = sc.scores[idx]
        tsf = sc.dom2sf[t]
        tfold = sc.dom2fold[t]
        if qfold == tfold:
            TP = "TP"
        else:
            TP = "FP"
        s = q
        s += "\t" + qfold
        s += "\t" + t
        s += "\t" + tfold
        s += "\t%.3g" % evalue
        s += "\t" + TP
        print(s)
