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
		assert not score1 is None and not score2 is None
		if self.se == 's':
			return score1 > score2
		elif self.se == 'e':
			return score1 < score2
		else:
			assert False

	def set_possible_tfs_family(self):
		self.dom2nrpossibletps = {}
		self.NT = 0
		self.NI = 0
		for dom in self.doms:
			fam = self.dom2fam[dom]
			famsize = self.fam2size[fam]
			assert famsize > 0
			if famsize == 1:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = famsize - 1
			self.NT += famsize - 1
		self.NF = self.nrdompairs - self.NT # total possible FPs

	def set_possible_tfs_sf(self):
		self.dom2nrpossibletps = {}
		self.NT = 0
		self.NI = 0
		for dom in self.doms:
			sf = self.dom2sf[dom]
			sfsize = self.sf2size[sf]
			assert sfsize > 0
			if sfsize == 1:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = sfsize - 1
			self.NT += sfsize - 1
		self.NF = self.nrdompairs - self.NT # total possible FPs

	def set_possible_tfs_ignore(self):
		self.dom2nrpossibletps = {}
		self.nrsingletons = 0 # nr singleton domains (no possible non-trivial TPs)
		self.NT = 0 # nr ignored pairs
		self.NI = 0 # nr ignored pairs
		for dom in self.doms:
			n = 0
			sf = self.dom2sf[dom]
			fold = self.dom2fold[dom]
			fold_doms = self.fold2doms[fold]
			for fold_dom in fold_doms:
				if fold_dom == dom:
					continue
				fold_dom_sf = self.dom2sf[fold_dom]
				if fold_dom_sf == sf:
					n += 1
				else:
					self.NI += 1
			if n == 0:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = n
			self.NT += n
		self.NF = self.nrdompairs - self.NT - self.NI # total possible FPs

	def set_possible_tfs_f_s(self):
		self.dom2nrpossibletps = {}
		self.nrsingletons = 0 # nr singleton families (no possible non-trivial TPs)
		self.NT = 0 # nr ignored pairs
		self.NI = 0 # nr ignored pairs
		for dom in self.doms:
			n = 0
			fam = self.dom2fam[dom]
			sf = self.dom2sf[dom]
			fold = self.dom2fold[dom]
			fold_doms = self.fold2doms[fold]
			sf_doms = self.sf2doms[sf]
			for fold_dom in fold_doms:
				if fold_dom == dom:
					continue
				fold_dom_fam = self.dom2fam[fold_dom]
				if fold_dom_fam == fam:
					n += 1
				else:
					self.NI += 1
			for sf_dom in sf_doms:
				if sf_dom == dom:
					continue
				sf_dom_fam = self.dom2fam[sf_dom]
				if sf_dom_fam == fam:
					n += 1
				else:
					self.NI += 1
			if n == 0:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = n
			self.NT += n
		self.NF = self.nrdompairs - self.NT - self.NI # total possible FPs

	def set_possible_tfs_fold(self):
		self.dom2nrpossibletps = {}
		self.NT = 0
		self.NI = 0
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

		if self.level == "family":
			self.set_possible_tfs_family()
		elif self.level == "sf":
			self.set_possible_tfs_sf()
		elif self.level == "half":
			self.set_possible_tfs_sf()
		elif self.level == "ignore":
			self.set_possible_tfs_ignore()
		elif self.level == "fold":
			self.set_possible_tfs_fold()
		elif self.level == "f_s":
			self.set_possible_tfs_f_s()
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

		self.fam2size = {}
		for fam in self.fams:
			self.fam2size[fam] = len(self.fam2doms[fam])
		self.sf2size = {}
		for sf in self.sfs:
			self.sf2size[sf] = len(self.sf2doms[sf])
		self.fold2size = {}
		for fold in self.folds:
			self.fold2size[fold] = len(self.fold2doms[fold])

	def eval_unsorted(self, qs, ts, plot_scores):
		if not self.quiet:
			sys.stderr.write("sorting...\n")
		nrhits = len(qs)
		assert nrhits > 10
		assert len(ts) == nrhits
		assert len(plot_scores) == nrhits
		v = [ (plot_scores[i], i) for i in range(nrhits) ]
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
			scores_sorted.append(plot_scores[i])
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

	def is_tp(self, q, t):
		q = q.split('/')[0]
		t = t.split('/')[0]
		if self.level == "family":
			qfam = self.dom2fam.get(q)
			tfam = self.dom2fam.get(t)
			if qfam is None or tfam is None:
				if qfam is None:
					self.unknown_doms.add(q)
				if tfam is None:
					self.unknown_doms.add(t)
				return 0
			else:
				if qfam == tfam:
					return 1
				else:
					return 0

		elif self.level == "sf":
			qsf = self.dom2sf.get(q)
			tsf = self.dom2sf.get(t)
			if qsf is None or tsf is None:
				if qsf is None:
					self.unknown_doms.add(q)
				if tsf is None:
					self.unknown_doms.add(t)
				return 0
			else:
				if qsf == tsf:
					return 1
				else:
					return 0

		elif self.level == "ignore":
			qsf = self.dom2sf.get(q)
			tsf = self.dom2sf.get(t)
			qfold = self.dom2fold.get(q)
			tfold = self.dom2fold.get(t)
			if qsf is None or tsf is None:
				if qsf is None:
					self.unknown_doms.add(q)
				if tsf is None:
					self.unknown_doms.add(t)
				return -1
			else:
				if qsf == tsf:
					return 1
				elif qfold != tfold:
					return 0
				else:
					return -1

		elif self.level == "half":
			qsf = self.dom2sf.get(q)
			tsf = self.dom2sf.get(t)
			qfold = self.dom2fold.get(q)
			tfold = self.dom2fold.get(t)
			if qsf is None or tsf is None:
				if qsf is None:
					self.unknown_doms.add(q)
				if tsf is None:
					self.unknown_doms.add(t)
				return -1
			else:
				if qsf == tsf:
					return 1
				elif qfold != tfold:
					return 0
				elif qsf != tsf and qfold == tfold:
					return 0.5
				else:
					return -1

		elif self.level == "fold":
			qfold = self.dom2fold.get(q)
			tfold = self.dom2fold.get(t)
			if qfold is None or tfold is None:
				if qfold is None:
					self.unknown_doms.add(q)
				if tfold is None:
					self.unknown_doms.add(t)
				return 0
			else:
				if qfold == tfold:
					return 1
				else:
					return 0
		assert False

	def eval_sorted(self, qs, ts, scores):
		self.qs = qs
		self.ts = ts
		self.scores = scores
		unknown_doms = set()
		nrhits = len(qs)
		assert nrhits > 10
		assert len(ts) == nrhits
		assert len(scores) == nrhits
		last_score = None

		ntp = 0         # accumulated nr of TP hits
		nfp = 0         # accumulated nr of FP hits

		tpstep = 0.01   # bin size for TPs (X axis tick marks)
		tprt = 0.01     # current TPR threshold, +=tpstep during scan

		self.plot_tprs = []
		self.plot_fprs = []
		self.plot_epqs = []
		self.plot_scores = []
		self.plot_precisions = []

		self.tpr_at_fpepq0_1 = None
		self.tpr_at_fpepq1 = None
		self.tpr_at_fpepq10 = None

		self.dom2score_firstfp = {}
		self.dom2score_firsttp = {}
		for dom in self.doms:
			self.dom2score_firstfp[dom] = None
			self.dom2score_firsttp[dom] = None

		self.tps = []
		ni = 0
		if not self.quiet:
			sys.stderr.write("scanning hits...\n")
		for i in range(nrhits):
			if not self.quiet:
				if i%100000 == 0:
					gb = get_memory_usage()
					pct = 100*i/nrhits
					sys.stderr.write("%.1f%%, %.1f Gb RAM used   \r" % (pct, gb))
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

			tp = self.is_tp(q, t)
			if tp == 1:
				ntp += 1
				if self.dom2score_firsttp.get(q) is None or \
					self.score1_is_better(score, self.dom2score_firsttp[q]):
					self.dom2score_firsttp[q] = score
			elif tp == 0:
				nfp += 1
				if self.dom2score_firstfp.get(q) is None or \
					self.score1_is_better(score, self.dom2score_firstfp[q]):
					self.dom2score_firstfp[q] = score
			elif tp == 0.5:
				nfp += 0.5
			elif tp == -1:
				ni += 1
			else:
				assert False
			self.tps.append(tp)

			# tpr=true-positive rate
			tpr = float(ntp)/self.NT

			# fpepq = false-positive errors per query
			fpepq = float(nfp)/self.nrdoms

			# precision = tp/(tp + fp)
			precision = 0
			fpr = 0
			if ntp+nfp > 0:
				precision = ntp/(ntp + nfp)
				fpr = nfp/(ntp + nfp)

			if fpepq >= 0.1 and self.tpr_at_fpepq0_1 is None:
				self.tpr_at_fpepq0_1 = tpr
			if fpepq >= 1 and self.tpr_at_fpepq1 is None:
				self.tpr_at_fpepq1 = tpr
			if fpepq >= 10 and self.tpr_at_fpepq10 is None:
				self.tpr_at_fpepq10 = tpr
			if tpr >= tprt:
				self.plot_tprs.append(tprt)
				self.plot_fprs.append(fpr)
				self.plot_epqs.append(fpepq)
				self.plot_scores.append(last_score)
				self.plot_precisions.append(precision)

				tprt += tpstep

			last_score = score
		sys.stderr.write("ni=%d\n" % ni)
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

		self.plot_tprs.append(tprt)
		self.plot_fprs.append(fpr)
		self.plot_epqs.append(fpepq)
		self.plot_scores.append(last_score)
		self.plot_precisions.append(precision)

		self.nrtps_to_firstfp = 0
		for i in range(nrhits):
			score = scores[i]
			tp = self.tps[i]
			q = qs[i].split('/')[0]
			tp = self.tps[i]
			if tp and not self.dom2score_firstfp[q] is None and \
				self.score1_is_better(score, self.dom2score_firstfp[q]):
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
		assert level == "family" or level == "sf" or level == "half" or level == "fold" or level == "ignore" or level == "f_s"

		self.se = se
		self.level = level
		self.quiet = quiet
		if se == 's':
			self.low_score = -1
		elif se == 'e':
			self.low_score = 99999
		else:
			assert False

		self.unknown_doms = set()
		self.read_dom2scopid(dom2scopid_fn)
		self.set_possible_tfs()

	def plot2file(self, fn):
		f = open(fn, "w")
		self.roc2filehandle(f)
		f.close()

	def plot2filehandle(self, f):
		n = len(self.plot_tprs)
		if len(self.plot_fprs) != n:
			assert False, "%d,%d" % (len(self.plot_fprs), n)
		assert len(self.plot_epqs) == n
		assert len(self.plot_scores) == n
		f.write("tpr\tepq\tfpr\tprecision\tscore\n")
		for i in range(n):
			s = "%.4g" % self.plot_tprs[i]
			s += "\t%.4g" % self.plot_epqs[i]
			s += "\t%.4g" % self.plot_fprs[i]
			s += "\t%.4g" % self.plot_precisions[i]
			s += "\t%.4g" % self.plot_scores[i]
			f.write(s + '\n')

	def roc_area(self, lo_epq, hi_epq):
		n = len(self.plot_tprs)
		assert len(self.plot_epqs) == n
		assert len(self.plot_scores) == n
		total = 0
		for i in range(n):
			epq = self.plot_epqs[i]
			if epq >= lo_epq and epq <= hi_epq:
				tpr = self.plot_tprs[i]
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

	def top_hit_report1(self, f, dom, scoretp, scorefp, ntp, nfp):
		nr_doms = len(self.doms)
		nr_possible_tps = nr_doms - self.nrsingletons
		s = dom
		if scoretp is None:
			s += "\t."
		else:
			s += "\t%.3g" % scoretp

		if scorefp is None:
			s += "\t."
		else:
			s += "\t%.3g" % scorefp
		s += "\t%.4f\t%.4f" % (ntp/nr_possible_tps, nfp/nr_doms)
		f.write(s + "\n")

	def top_hit_report(self, fn):
		K = 100
		f = open(fn, "w")
		ntp = 0
		nfp = 0
		v = []
		for dom in self.doms:
			scoretp = self.dom2score_firsttp[dom]
			scorefp = self.dom2score_firstfp[dom]
			if scoretp is None and scorefp is None:
				continue
			if scoretp is None and scorefp is None:
				if self.score1_is_better(scoretp, scorefp):
					sort_score = scoretp
				else:
					sort_score = scorefp
			elif scoretp is None:
				assert not scorefp is None
				sort_score = scorefp
			else:
				assert not scoretp is None
				sort_score = scoretp
			pair = (sort_score, dom)
			v.append(pair)
		do_reverse = (self.se == "s")
		v_sorted = sorted(v, reverse=do_reverse)
		for score, dom in v_sorted:
			scoretp = self.dom2score_firsttp[dom]
			scorefp = self.dom2score_firstfp[dom]
			if scoretp is None and scorefp is None:
				continue
			elif scoretp is None and not scorefp is None:
				nfp += 1
			elif not scoretp is None and scorefp is None:
				ntp += 1
			elif not scoretp is None and not scorefp is None:
				if self.score1_is_better(scoretp, scorefp):
					ntp += 1
				else:
					nfp += 1
			else:
				assert False
			if (ntp + nfp)%K == 0:
				self.top_hit_report1(f, dom, scoretp, scorefp, ntp, nfp)
		self.top_hit_report1(f, dom, scoretp, scorefp, ntp, nfp)
		f.close()
