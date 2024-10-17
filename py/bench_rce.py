#!/usr/bin/python3

import sys

lookup_fn = sys.argv[1]
hits_fn = sys.argv[2]

removeSelfHit = 1;
tp_fam = 0
tp_sfam = 0
tp_fold = 0
fp = 0;
print("PREC_FAM","PREC_SFAM","PREC_FOLD","RECALL_FAM","RECALL_SFAM","RECALL_FOLD")

def get_sf(fam):
	flds = fam.split('.')
	assert len(flds) == 4
	return flds[0] + '.' + flds[1] + '.' + flds[2]

def get_fold(scopid):
	flds = fam.split('.')
	assert len(flds) == 4
	return flds[0] + '.' + flds[1]

doms = set()
fams = set()
sfs = set()
folds = set()

dom2fam = {}
dom2sf = {}
dom2fold = {}

fam2size = {}
sf2size = {}
fold2size = {}

for line in open(lookup_fn):
	flds = line[:-1].split('\t')
	dom = flds[0]
	fam = flds[1]
	sf = get_sf(fam)
	fold = get_fold(fam)

	doms.add(dom)

	if fam not in fams:
		fams.add(fam)
		fam2size[fam] = 0

	if sf not in fams:
		fams.add(sf)
		fam2size[sf] = 0

	if fold not in fams:
		fams.add(fold)
		fam2size[fold] = 0

	dom2fam[dom] = fam
	dom2sf[dom] = sf
	dom2fam[fold] = fold

	fam2size[fam] += 1
	sf2size[sf] += 1
	fold2size[fold] += 1

for fam in fams:
	fam2size[fam] -= 1

for sf in fams:
	sf2size[sf] -= 1

for fold in folds:
	fold2size[sf] -= 1

queries = 3566 # don't understand this calculation

for line in open(hits_fn):
	flds = line[:-1].split('\t')
	q = flds[0]
	t = flds[1]
##	score = float(flds[2]) # not used
	if q == t:	# ignore self-hits
		continue
	assert q in doms and t in doms
!($1 in dom2fam) {next}	
!($2 in dom2fam) {next}
$1 == $2 {next} # skip self hit

# print(             "PREC_FAM",         "PREC_SFAM",          "PREC_FOLD",          "RECALL_FAM",     "RECALL_SFAM",     "RECALL_FOLD")
NR %1000 == 0{ print tp_fam/(tp_fam+fp), tp_sfam/(tp_sfam+fp), tp_fold/(tp_fold+fp), tp_fam / queries, tp_sfam / queries, tp_fold / queries, tp_fam; }										      
id2fold[$1] != id2fold[$2] {norm=(foldCnt[id2fold[$1]] - sfamCnt[id2sfam[$1]]); norm = (norm > famCnt[dom2fam[$1]]) ? norm : famCnt[dom2fam[$1]]; norm = (norm == 0) ? 1 : norm; fp = fp + (1 / norm); next }
(famCnt[dom2fam[$1]] == 0 || sfamCnt[id2sfam[$1]] - famCnt[dom2fam[$1]] == 0 || foldCnt[id2fold[$1]] - sfamCnt[id2sfam[$1]] == 0){ next } 

dom2fam[$1] == dom2fam[$2] { norm=famCnt[dom2fam[$1]];
					   tp_fam = tp_fam + (1 / norm);
			   next }
dom2fam[$1] != dom2fam[$2] && id2sfam[$1] == id2sfam[$2]  { norm=(sfamCnt[id2sfam[$1]] - famCnt[dom2fam[$1]]);
													  tp_sfam = tp_sfam + (1 / norm);
							  next }
dom2fam[$1] != dom2fam[$2] && id2sfam[$1] != id2sfam[$2] && id2fold[$1] == id2fold[$2] { norm=(foldCnt[id2fold[$1]] - sfamCnt[id2sfam[$1]]); 
																				   tp_fold = tp_fold + (1 / norm); 
											   next }

END{
	   print tp_fam/(tp_fam+fp), tp_sfam/(tp_sfam+fp), tp_fold/(tp_fold+fp), tp_fam / queries, tp_sfam / queries, tp_fold / queries, tp_fam; 									       
	   #print tp_fam, tp_sfam, tp_fold, fp;	
}
