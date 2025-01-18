#!/usr/bin/python3

import sys

fn1 = "../misc/mkf.tsv"
fn2 = "../alns/reseek_fast.tsv"

pair2e = {}
for line in open(fn2):
	flds = line[:-1].split('\t')
	assert len(flds) == 3
	q = flds[0]
	t = flds[1]
	e = float(flds[2])
	pair = (q, t)
	pair2e[pair] = e

for line in open(fn1):
	flds = line[:-1].split('\t')
	q = flds[0]
	t = flds[1]
	pair = (q, t)
	e = pair2e.get(pair, None)
	if e is None:
		se = "999"
	else:
		se = "%.3g" % e
	sys.stdout.write(se + "\t" + line)
