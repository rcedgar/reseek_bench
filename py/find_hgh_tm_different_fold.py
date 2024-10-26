#!/usr/bin/python3

import sys
import scop40

sc = scop40.Scop40("s", "fold", "../data/dom_scopid.tsv")
# sc.read_file("../sorted_alns/TMalign.tsv", 0, 1, 2)
# sc.eval_sorted(sc.qs, sc.ts, sc.scores)

for line in open("../sorted_alns/TMalign.tsv"):
    flds = line[:-1].split('\t')
    score = float(flds[2])
    if score <= 0.5001:
        break
    qdom = flds[0]
    tdom = flds[1]
    qfold = sc.dom2fold[qdom]
    tfold = sc.dom2fold[tdom]
    if qfold == tfold:
        continue
    qclass = qfold.split('.')[0]
    tclass = tfold.split('.')[0]
    s = "%.4f" % score
    s += "\t" + qdom
    s += "\t" + qfold
    s += "\t" + tdom
    s += "\t" + tfold
    s += "\t" + qclass
    s += "\t" + tclass
    if qclass != tclass:
        s += "\tDIFFERENT_CLASS"
    print(s)
