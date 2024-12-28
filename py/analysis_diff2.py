#!/usr/bin/python3

import sys

fnx = sys.argv[1]
fny = sys.argv[2]

MIN_EPQ = 0.01
MAX_EPQ = 10

def read_analysis(fn):
	f = open(fn)
	hdr = f.readline()
	assert hdr.startswith("tpr\tepq\tfpr\tprecision")
	tprs = []
	epqs = []
	scores = []
	for line in f:
		if line.startswith("SEPQ"):
			break
		flds = line[:-1].split('\t')
		assert len(flds) > 3
		tpr = float(flds[0])
		epq = float(flds[1])
		score = float(flds[2])
		if epq < MIN_EPQ:
			continue
		if epq > MAX_EPQ:
			break

		tprs.append(tpr)
		epqs.append(epq)
		scores.append(score)
	
	return tprs, epqs, scores

tprsx, epqsx, scoresx = read_analysis(fnx)
tprsy, epqsy, scoresy = read_analysis(fny)

nx = len(tprsx)
ny = len(tprsy)
n = min(nx, ny)
for i in range(n):
	tprx = tprsx[i]
	assert tprsy[i] == tprx
	epqx = epqsx[i]
	epqy = epqsy[i]
	diff = epqx - epqy
	s = "%.2f" % tprx
	s += "\t%.4g" % diff
	print(s)