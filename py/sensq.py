#!/usr/bin/python3

import sys

fn = sys.argv[1]
the_dom = sys.argv[2]

def get_sf(fam):
	flds = fam.split('.')
	assert len(flds) == 4
	return flds[0] + '.' + flds[1] + '.' + flds[2]

dom2sf = {}
for line in open("../data/dom_scopid.tsv"):
	flds = line[:-1].split('\t')
	assert len(flds) == 2
	dom = flds[0]
	fam = flds[1]
	sf = get_sf(fam)
	dom2sf[dom] = sf

tps = []
fps = []
tp_evalues = []
fp_evalues = []

for line in open(fn):
	flds = line[:-1].split('\t')
	q = flds[0]
	qflds = q.split('/')
	qdom = qflds[0]
	if qdom != the_dom:
		continue
	qsf = dom2sf[qdom]
	t = flds[1]
	tdom = t.split('/')[0]
	tsf = dom2sf[tdom]
	evalue = float(flds[2])

	if qsf == tsf:
		tps.append(tdom)
		tp_evalues.append(evalue)
	else:
		fps.append(tdom)
		fp_evalues.append(evalue)

print(len(tps), len(fps))