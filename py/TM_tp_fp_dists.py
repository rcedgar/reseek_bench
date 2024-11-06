#!/usr/bin/python3

import sys
import scop40
import random

sc = scop40.Scop40("s", "sf", "../data/dom_scopid.tsv")

sf2size = sc.sf2size

M = 100
BINS = 100

doms_ge_M = set()
for sf in sc.sfs:
    if sf2size[sf] >= M:
        doms = sc.sf2doms[sf]
        dom = random.choice(doms)
        doms_ge_M.add(dom)

dom2tpcounts = {}
dom2fpcounts = {}
for dom in doms_ge_M:
    dom2tpcounts[dom] = [0]*(BINS+1)
    dom2fpcounts[dom] = [0]*(BINS+1)

for line in open("../sorted_alns/TMalign.tsv"):
    flds = line[:-1].split('\t')
    score = float(flds[2])
    qdom = flds[0]
    if not qdom in doms_ge_M:
        continue
    tdom = flds[1]
    qsf = sc.dom2sf[qdom]
    tsf = sc.dom2sf[tdom]
    b = int(score*100.0)
    assert b >= 0 and b <= 100
    if qsf == tsf:
        dom2tpcounts[qdom][b] += 1
    else:
        dom2fpcounts[qdom][b] += 1
s = "TM"
for dom in doms_ge_M:
    s += "\t"
    s += dom + "-TP"
    s += "\t"
    s += dom + "-FP"
print(s)

for b in range(BINS+1):
    s = "%.3f" % (b/100.0)
    for dom in doms_ge_M:
        s += "\t%u" % dom2tpcounts[dom][b]
        s += "\t%u" % dom2fpcounts[dom][b]
    print(s)
