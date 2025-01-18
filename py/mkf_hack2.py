#!/usr/bin/python3

import sys

fn = "../misc/mkf_hack.tsv"

N = 1000

q2tups = {}

def get_hsp(tup):
	return tup[1]

def sort_tups(tups):
	return sorted(tups, key=get_hsp, reverse=True)

for line in open(fn):
	flds = line[:-1].split('\t')
	assert len(flds) == 5
	e = flds[0]
	q = flds[1]
	t = flds[2]
	hsp = int(flds[3])
	chain = int(flds[4])
	
	tup = (e, hsp, chain, t)
	v = q2tups.get(q, [])
	v.append(tup)
	q2tups[q] = v

qs = list(q2tups.keys())
for q in qs:
	tups = q2tups[q]
	sorted_tups = sort_tups(tups)
	n = len(sorted_tups)
	if n > N:
		n = N
	for i in range(n):
		e, hsp, chain, t = sorted_tups[i]
		if e != "999":
			s = q
			s += "\t" + t
			s += "\t" + e
			print(s)
