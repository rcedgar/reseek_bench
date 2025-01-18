#!/usr/bin/python3

# Improved version of $src/reseek_scop40/scripts/accuracy_analysis.py
# using scop40.py import lib.

import sys
import scop40
import argparse

Usage = "Usage TODO"
levels =[ "fam1", "sf2", "sf3", "sf4", "fold5", "fold6" ]

AP = argparse.ArgumentParser(description = Usage)

AP.add_argument("--input", required=False, default="/dev/stdin", help="Hits tsv file (default stdin)")
AP.add_argument("--fields", required=False, default="1,2,3", help="query,target,score (default 1,2,3)")
AP.add_argument('--type', required=True, choices=[ "score", "evalue"], help="Larger value is better (score) or worse (E-value)")
AP.add_argument("--level", required=False, choices=levels, default="sf2", help="level (default sf2)")
AP.add_argument('--sort', action='store_true', help="Sort input (default already sorted)")
AP.add_argument('--lookup', default="../data/dom_scopid.tsv", help="Lookup file (default ../data/dom_scopid.tsv)")

Args = AP.parse_args()

tsv_fn = Args.input
dom2scopid_fn = Args.lookup
level = Args.level
if Args.type == "score":
    se = "s"
elif Args.type == "evalue":
    se = "e"
else:
    assert False

fs = Args.fields.split(",")
if len(fs) != 3:
     assert False, "--fields must be 3 comma-separated 1-based field numbers"

qfldnr = int(fs[0]) - 1
tfldnr = int(fs[1]) - 1
scorefldnr = int(fs[2]) - 1

assert qfldnr >= 0
assert tfldnr >= 0
assert qfldnr != tfldnr

if Args.sort:
    is_sorted = False
else:
    is_sorted = True

#	def __init__(self, se, level, dom2scopid_fn):
sc = scop40.Scop40(se, level, dom2scopid_fn)

# def eval_file(self, fn, qfldnr, tfldnr, scorefldnr, is_sorted):
sc.eval_file(tsv_fn, qfldnr, tfldnr, scorefldnr, is_sorted)
sc.plot2filehandle(sys.stdout)
print(sc.get_summary())

