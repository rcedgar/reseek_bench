# scop40 library functions

import sys

# in Gb
def get_memory_usage():
	import resource
	kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
	return kb*1000/1e9

# Scop identifier looks like a.1.2.3 
#     a    1           2      3
# class.fold.superfamily.family
def getfold(scopid):
	flds = scopid.split('.')
	assert len(flds) == 4
	fold = flds[0] + "." + flds[1]
	return fold

def getsf(scopid):
	flds = scopid.split('.')
	assert len(flds) == 4
	sf = flds[0] + "." + flds[1] + "." + flds[2]
	return sf

class Scop40:
	def score1_is_better(self, score1, score2):
		if self.se == 's':
			return score1 > score2
		elif self.se == 'e':
			return score1 < score2
		else:
			assert False

	def set_possible_tfs_sf(self):
		self.dom2nrpossibletps = {}
		self.NT = 0
		for dom in self.doms:
			sf = self.dom2sf[dom]
			sfsize = self.sf2size[sf]
			assert sfsize > 0
			if sfsize == 1:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = sfsize - 1
			self.NT += sfsize - 1
		self.NF = self.nrdompairs - self.NT # total possible FPs

	def set_possible_tfs_fold(self):
		self.dom2nrpossibletps = {}
		self.NT = 0
		for dom in self.doms:
			fold = self.dom2fold[dom]
			foldsize = self.fold2size[fold]
			assert foldsize > 0
			if foldsize == 1:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = foldsize - 1
			self.NT += foldsize - 1
		self.NF = self.nrdompairs - self.NT # total possible FPs

	def set_possible_tfs(self):
		self.nrdoms = len(self.doms)
		self.nrdompairs = self.nrdoms*self.nrdoms - self.nrdoms
		self.nrsingletons = 0 # nr singleton domains (no possible non-trivial TPs)

		if self.level == "sf":
			self.set_possible_tfs_sf()
		elif self.level == "fold":
			self.set_possible_tfs_fold()
		else:
			assert False

	def read_dom2scopid(self, dom2scopid_fn):
		self.doms = set()
		self.fams = set()
		self.sfs = set()
		self.folds = set()
		self.fam2doms = {}
		self.sf2doms = {}
		self.fold2doms = {}
		self.dom2fam = {}
		self.dom2sf = {}
		self.dom2fold = {}

		for line in open(dom2scopid_fn):
			flds = line[:-1].split('\t')
			assert len(flds) == 2
			dom = flds[0]
			scopid = flds[1]
			assert dom not in self.doms
			self.doms.add(dom)

			fam = scopid
			sf = getsf(scopid)
			fold = getfold(scopid)

			self.dom2fam[dom] = scopid
			self.dom2sf[dom] = sf
			self.dom2fold[dom] = fold

			if not fam in self.fams:
				self.fam2doms[fam] = []
				self.fams.add(fam)
			self.fam2doms[fam].append(dom)

			if not sf in self.sfs:
				self.sf2doms[sf] = []
				self.sfs.add(sf)
			self.sf2doms[sf].append(dom)

			if not fold in self.folds:
				self.fold2doms[fold] = []
				self.folds.add(fold)
			self.fold2doms[fold].append(dom)

		if self.level == "sf":
			self.sf2size = {}
			for sf in self.sfs:
				self.sf2size[sf] = len(self.sf2doms[sf])
		elif self.level == "fold":
			self.fold2size = {}
			for fold in self.folds:
				self.fold2size[fold] = len(self.fold2doms[fold])
		else:
			assert False

	def eval_unsorted(self, qs, ts, scores):
		if not self.quiet:
			sys.stderr.write("sorting...\n")
		nrhits = len(qs)
		assert nrhits > 10
		assert len(ts) == nrhits
		assert len(scores) == nrhits
		v = [ (scores[i], i) for i in range(nrhits) ]
		do_reverse = (self.se == "s")
		v_sorted = sorted(v, reverse=do_reverse)
		qs_sorted = []
		ts_sorted = []
		scores_sorted = []
		for _, i in v_sorted:
			q = qs[i]
			t = ts[i]
			if q == t:
				continue
			qs_sorted.append(q)
			ts_sorted.append(t)
			scores_sorted.append(scores[i])
		if not self.quiet:
			sys.stderr.write("...done\n")
		self.eval_sorted(qs_sorted, ts_sorted, scores_sorted)

	# 0-based field nrs
	def read_file(self, fn, qfldnr, tfldnr, scorefldnr):
		self.qs = []
		self.ts = []
		self.scores = []
		if not self.quiet:
			sys.stderr.write("Reading %s...\n" % fn)
		for line in open(fn):
			flds = line[:-1].split('\t')
			q = flds[qfldnr]
			t = flds[tfldnr]
			if q == t:
				continue
			self.qs.append(q)
			self.ts.append(t)
			self.scores.append(float(flds[scorefldnr]))
		if not self.quiet:
			sys.stderr.write("...done\n")

	def eval_file(self, fn, qfldnr, tfldnr, scorefldnr, is_sorted):
		self.read_file(fn, qfldnr, tfldnr, scorefldnr)
		if is_sorted:
			self.eval_sorted(self.qs, self.ts, self.scores)
		else:
			self.eval_unsorted(self.qs, self.ts, self.scores)

	def eval_sorted(self, qs, ts, scores):
		unknown_doms = set()
		nrhits = len(qs)
		assert nrhits > 10
		assert len(ts) == nrhits
		assert len(scores) == nrhits
		last_score = None

		ntp = 0         # accumulated nr of TP hits
		nfp = 0         # accumulated nr of FP hits

	# for plot with TPR on X axis
		tpstep = 0.01   # bin size for TPs (X axis tick marks)
		tprt = 0.01     # current TPR threshold, +=tpstep during scan
		self.roc_tprs = []
		self.roc_epqs = []
		self.roc_scores = []

	# for plot with FPR on X axis
		epqmul = pow(2, 1/3)	# multiplier
		epqt = 0.01				# current FPR threshold, *=epqmul during scan
		maxepq = 10
		self.rocf_tprs = []
		self.rocf_epqs = []
		self.rocf_scores = []

	# for Precision-Recall plot
		self.rocpr_precisions = []
		self.rocpr_recalls = []
		self.rocpr_scores= []

		self.tpr_at_fpepq0_1 = None
		self.tpr_at_fpepq1 = None
		self.tpr_at_fpepq10 = None

		dom2score_firstfp = {}
		for dom in self.doms:
			dom2score_firstfp[dom] = None

		self.tps = []
		if not self.quiet:
			sys.stderr.write("scanning hits...\n")
		for i in range(nrhits):
			if not self.quiet:
				if i%100000 == 0:
					gb = get_memory_usage()
					sys.stderr.write("%.1f k hits, %.1f Gb RAM used   \r" % (i/1000, gb))
			q = qs[i].split('/')[0]
			t = ts[i].split('/')[0]
			if q == t:
				assert False, "Self-hits not removed"
			score = scores[i]

			if i > 0 and last_score != score:
				if not self.score1_is_better(last_score, score):
					assert False, \
						f"Not sorted correctly {q=} {t=} {self.se=} {last_score=} {score=}"
			last_score = score

			if self.level == "sf":
				qsf = self.dom2sf.get(q)
				tsf = self.dom2sf.get(t)
				if qsf is None or tsf is None:
					if qsf is None:
						unknown_doms.add(q)
					if tsf is None:
						unknown_doms.add(t)
					tp = False
				else:
					tp = (qsf == tsf)
			elif self.level == "fold":
				qfold = self.dom2fold.get(q)
				tfold = self.dom2fold.get(t)
				if qfold is None or tfold is None:
					if qfold is None:
						unknown_doms.add(q)
					if tfold is None:
						unknown_doms.add(t)
					tp = False
				else:
					tp = (qfold == tfold)

			if tp:
				ntp += 1
			else:
				nfp += 1
				if dom2score_firstfp.get(q) is None or \
					self.score1_is_better(score, dom2score_firstfp[q]):
					dom2score_firstfp[q] = score
			self.tps.append(tp)

			# tpr=true-positive rate
			tpr = float(ntp)/self.NT

			# fpepq = false-positive errors per query
			fpepq = float(nfp)/self.nrdoms

			# precision = tp/(tp + fp)
			# recall = tp/(fp + fn)
			nfn = self.NT - ntp
			precision = 0
			if ntp+nfp > 0:
				precision = ntp/(ntp + nfp)
			recall = 0
			if ntp+nfn > 0:
				recall = ntp/(ntp + nfn)

			if fpepq >= 0.1 and self.tpr_at_fpepq0_1 is None:
				self.tpr_at_fpepq0_1 = tpr
			if fpepq >= 1 and self.tpr_at_fpepq1 is None:
				self.tpr_at_fpepq1 = tpr
			if fpepq >= 10 and self.tpr_at_fpepq10 is None:
				self.tpr_at_fpepq10 = tpr
			if tpr >= tprt:
				self.roc_tprs.append(tprt)
				self.roc_epqs.append(fpepq)
				self.roc_scores.append(last_score)

				self.rocpr_precisions.append(precision)
				self.rocpr_recalls.append(recall)
				self.rocpr_scores.append(last_score)

				tprt += tpstep

			if epqt < maxepq and fpepq >= epqt:
				self.rocf_tprs.append(tpr)
				self.rocf_epqs.append(fpepq)
				self.rocf_scores.append(last_score)
				epqt *= epqmul

			last_score = score

		if self.tpr_at_fpepq0_1 is None:
			self.tpr_at_fpepq0_1 = tpr
		if self.tpr_at_fpepq1 is None:
			self.tpr_at_fpepq1 = tpr
		if self.tpr_at_fpepq10 is None:
			self.tpr_at_fpepq10 = tpr

		nrhits = len(qs)
		assert len(self.tps) == nrhits

		if not self.quiet:
			sys.stderr.write("%.1f M hits, %.1f Gb RAM used   \n" % (nrhits/1e6, get_memory_usage()))

		if self.tpr_at_fpepq0_1 is None:
			self.tpr_at_fpepq0_1 = tpr

		if self.tpr_at_fpepq1 is None:
			self.tpr_at_fpepq1 = tpr

		if self.tpr_at_fpepq10 is None:
			self.tpr_at_fpepq1 = tpr
	
		tpr = float(ntp)/self.NT
		fpepq = float(nfp)/self.nrdoms

		self.roc_tprs.append(tprt)
		self.roc_epqs.append(fpepq)
		self.roc_scores.append(last_score)

		self.rocf_tprs.append(tprt)
		self.rocf_epqs.append(fpepq)
		self.rocf_scores.append(last_score)

		self.rocpr_precisions.append(precision)
		self.rocpr_recalls.append(recall)
		self.rocpr_scores.append(last_score)

		self.nrtps_to_firstfp = 0
		for i in range(nrhits):
			score = scores[i]
			tp = self.tps[i]
			q = qs[i].split('/')[0]
			tp = self.tps[i]
			if tp and not dom2score_firstfp[q] is None and \
				self.score1_is_better(score, dom2score_firstfp[q]):
				self.nrtps_to_firstfp += 1
		self.sens_to_firstfp = float(self.nrtps_to_firstfp)/self.NT
		nr_unknown = len(unknown_doms)
		if nr_unknown > 0:
			sys.stderr.write("Warning %d unknown doms\n" % nr_unknown)
			s = ""
			k = 0
			for dom in unknown_doms:
				s += " " + dom
				k += 1
				if nr_unknown > k:
					s += "..."
					break
			sys.stderr.write(s + "\n")

	def __init__(self, se, level, dom2scopid_fn, quiet = False):
		assert se == "s" or se == "e" # score or E-value
		assert level == "sf" or level == "fold"

		self.se = se
		self.level = level
		self.quiet = quiet
		if se == 's':
			self.low_score = -1
		elif se == 'e':
			self.low_score = 99999
		else:
			assert False

		self.read_dom2scopid(dom2scopid_fn)
		self.set_possible_tfs()

	def roc2file(self, fn):
		f = open(fn, "w")
		self.roc2filehandle(f)
		f.close()

	def roc2filehandle(self, f):
		n = len(self.roc_tprs)
		assert len(self.roc_epqs) == n
		assert len(self.roc_scores) == n
		f.write("tpr\tepq\tscore\n")
		for i in range(n):
			s = "%.4g" % self.roc_tprs[i]
			s += "\t%.4g" % self.roc_epqs[i]
			s += "\t%.4g" % self.roc_scores[i]
			f.write(s + '\n')

		n = len(self.rocf_tprs)
		assert len(self.rocf_epqs) == n
		assert len(self.rocf_scores) == n
		f.write("epq\ttpr\tscore\n")
		for i in range(n):
			s = "%.4g" % self.rocf_epqs[i]
			s += "\t%.4g" % self.rocf_tprs[i]
			s += "\t%.4g" % self.rocf_scores[i]
			f.write(s + '\n')

		n = len(self.rocpr_precisions)
		assert len(self.rocpr_recalls) == n
		assert len(self.rocpr_scores) == n
		f.write("precision\trecall\tscore\n")
		for i in range(n):
			s = "%.4g" % self.rocpr_precisions[i]
			s += "\t%.4g" % self.rocpr_recalls[i]
			s += "\t%.4g" % self.rocpr_scores[i]
			f.write(s + '\n')

	def roc_area(self, lo_epq, hi_epq):
		n = len(self.rocf_tprs)
		assert len(self.rocf_epqs) == n
		assert len(self.rocf_scores) == n
		total = 0
		for i in range(n):
			epq = self.rocf_epqs[i]
			if epq >= lo_epq and epq <= hi_epq:
				tpr = self.rocf_tprs[i]
				total += tpr
		return total

	def get_summary(self):
		area = self.roc_area(0.01, 10)
		summary = "SEPQ0.1=%.4f" % self.tpr_at_fpepq0_1
		summary += " SEPQ1=%.4f" % self.tpr_at_fpepq1
		summary += " SEPQ10=%.4f" % self.tpr_at_fpepq10
		summary += " S1FP=%.4f" % self.sens_to_firstfp
		summary += " N1FP=%u" % self.nrtps_to_firstfp
		summary += " area=%.3g" % area
		return summary
