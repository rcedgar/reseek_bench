#!/usr/bin/python3

import sys
import scop40

tsv_fn = sys.argv[1]
qfldnr = 0
tfldnr = 1
scorefldnr = 2

se = "s"
level = "sf"
dom2scopid_fn = "../data/dom_scopid.tsv"

sc = scop40.Scop40(se, level, dom2scopid_fn)
NT = sc.NT

# def eval_file(self, fn, qfldnr, tfldnr, scorefldnr, is_sorted):
sc.eval_file(tsv_fn, qfldnr, tfldnr, scorefldnr, True)
sys.stderr.write(sc.get_summary() + "\n")

tps = sc.tps
scores = sc.scores
n = len(tps)
assert len(scores) == n

lo = 0
hi = 1

tp_counts = [0]*101
fp_counts = [0]*101

def score2idx(score):
	assert score >= 0 and score <= 1
	idx = int(score*100)
	assert idx >= 0 and idx <= 100
	return idx

for i in range(n):
	tp = tps[i]
	score = scores[i]
	idx = score2idx(score)
	if tp:
		tp_counts[idx] += 1
	else:
		fp_counts[idx] += 1

last_precision = 0
last_precision_afdb = 0

last_fpr = 1
last_fpr_afdb = 0

tp = 0
fp = 0
print("TM\tTP\tFP\tSens\tPrec\tFPR")
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

	s = "%.2f" % (idx/100)
	s += "\t%d" % tp
	s += "\t%d" % fp
	s += "\t%.3g" % sens
	s += "\t%.3g" % precision
	s += "\t%.3g" % fpr

	print(s)
