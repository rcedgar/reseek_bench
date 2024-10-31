#!/usr/bin/python3

import sys
import scop40
import math

a = 5
b = -40
def get_qual(ts):
	LogE = a + b*ts
	if LogE < -20:
		return 1
	c = LogE
	# x = math.exp(0.25*c)
	x = 10**(c/10)
	Qual = 1/(1 + 0.5*x)
	return Qual

tsv_fn = "../sorted_alns/reseek_verysensitive_qual.tsv"
# tsv_fn = "../sorted_alns/tmp100.tsv"
qfldnr = 0
tfldnr = 1
scorefldnr = 2
tsfldnr = 3

se = "s"
level = "sf"
dom2scopid_fn = "../data/dom_scopid.tsv"

sc = scop40.Scop40(se, level, dom2scopid_fn)
NT = sc.NT

tp_counts = [0]*101
fp_counts = [0]*101

def score2idx(score):
	assert score >= 0 and score <= 1
	idx = int(score*100)
	assert idx >= 0 and idx <= 100
	return idx

n = 0
for line in open(tsv_fn):
	n += 1
	if n%100000 == 0:
		sys.stderr.write("%d\r" % n)

	flds = line[:-1].split('\t')
	q = flds[qfldnr]
	t = flds[tfldnr]
	# if q == t:
	# 	continue

	ts = float(flds[tsfldnr])
	qual = get_qual(ts)
	tp = sc.is_tp(q, t)
	idx = score2idx(qual)
#	print(q, t, ts, qual, tp, idx)
	if tp:
		tp_counts[idx] += 1
	else:
		fp_counts[idx] += 1
sys.stderr.write("%d\n" % n)

tp = 0
fp = 0
for idx in range(100, 30, -1):
	tp += tp_counts[idx]
	fp += fp_counts[idx]

	precision = 0
	fpr = 0
	n = tp + fp
	if n > 0:
		precision = tp/n
		fpr = fp/n
	sens = tp/NT

	s = "%.3f" % (idx/100)
	s += "\t%d" % tp
	s += "\t%d" % fp
	s += "\t%.3g" % sens
	s += "\t%.3g" % precision
	s += "\t%.3g" % fpr

	print(s)
