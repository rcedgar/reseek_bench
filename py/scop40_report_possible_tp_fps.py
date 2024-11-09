#!/usr/bin/python3

import sys
import scop40

sc = scop40.Scop40("e", "sf3", "../data/dom_scopid.tsv")
sc.report_standard_counts()

doms = sc.doms
dom2fam = sc.dom2fam
dom2sf = sc.dom2sf
dom2fold = sc.dom2fold

nr_singleton_sfs = 0
for sf in sc.sfs:
	if sc.sf2size[sf] == 1:
		nr_singleton_sfs += 1
print("nr_singleton_sfs = %d\n" % nr_singleton_sfs)

nr_same_fam = 0
nr_same_sf = 0
nr_same_fold = 0

nr_diff_fam = 0
nr_diff_sf = 0
nr_diff_fold = 0

nr_same_fold_diff_sf = 0
nr_same_sf_diff_fam = 0

nr_pairs = 0

nr_doms = len(doms)
k = 0
for dom1 in doms:
	k += 1
	if k%100 == 0:
		pct = k*100.0/nr_doms
		sys.stderr.write("%.1f%%\r" % pct)
	fam1 = dom2fam[dom1]
	sf1 = dom2sf[dom1]
	fold1 = dom2fold[dom1]
	for dom2 in doms:
		if dom1 == dom2:
			continue
		nr_pairs += 1

		fam2 = dom2fam[dom2]
		sf2 = dom2sf[dom2]
		fold2 = dom2fold[dom2]

		if fam1 == fam2:
			nr_same_fam += 1
		else:
			nr_diff_fam += 1

		if sf1 == sf2:
			nr_same_sf += 1
			if fam1 != fam2:
				nr_same_sf_diff_fam += 1
		else:
			nr_diff_sf += 1

		if fold1 == fold2:
			nr_same_fold += 1
			if sf1 != sf2:
				nr_same_fold_diff_sf += 1
		else:
			nr_diff_fold += 1

print(f"{nr_same_fam=}")
print(f"{nr_same_sf=}")
print(f"{nr_same_fold=}")
print(f"{nr_same_fold_diff_sf=}")
print(f"{nr_same_sf_diff_fam=}")
print("nr_doms=%d" % nr_doms)
print("nr_fams=%d" % len(sc.fams))
print("nr_sfs=%d" % len(sc.sfs))
print("nr_folds=%d" % len(sc.folds))

NT1 = nr_same_fam
NF1 = nr_diff_fold
NI1 = nr_same_sf_diff_fam + nr_same_fold_diff_sf

NT2 = nr_same_sf
NF2 = nr_diff_sf
NI2 = 0

NT3 = nr_same_sf
NF3 = nr_diff_fold
NI3 = nr_same_fold_diff_sf

NT4 = nr_same_sf - nr_same_fam
NF4 = nr_diff_fold
NI4 = nr_same_fam + nr_same_fold_diff_sf

NT5 = nr_same_fold - nr_same_sf
NF5 = nr_diff_fold
NI5 = nr_same_sf

NT6 = nr_same_fold
NF6 = nr_diff_fold
NI6 = 0

print("NT1=%8d  NI1=%8d  NF1=%8d  N1=%8d" % (NT1, NI1, NF1, NT1+NI1+NF1))

print("NT2=%8d  NI2=%8d  NF2=%8d  N2=%8d" % (NT2, NI2, NF2, NT2+NI2+NF2))

print("NT3=%8d  NI3=%8d  NF3=%8d  N3=%8d" % (NT3, NI3, NF3, NT3+NI3+NF3))

print("NT4=%8d  NI4=%8d  NF4=%8d  N4=%8d" % (NT4, NI4, NF4, NT4+NI4+NF4))

print("NT5=%8d  NI5=%8d  NF5=%8d  N5=%8d" % (NT5, NI5, NF5, NT5+NI5+NF5))

print("NT6=%8d  NI6=%8d  NF6=%8d  N6=%8d" % (NT6, NI6, NF6, NT6+NI6+NF6))
