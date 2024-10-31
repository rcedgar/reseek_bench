#!/usr/bin/python3

import sys
import scop40

se = "s"
level = "sf"
dom2scopid_fn = "../data/dom_scopid.tsv"

sc = scop40.Scop40(se, level, dom2scopid_fn)
NT = sc.NT
print(NT)