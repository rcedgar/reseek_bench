import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

class Plotter:
	def __init__(self, nr_rows, nr_cols, fig_width, fig_height):
		self.nr_rows = nr_rows
		self.nr_cols = nr_cols

		self.row_idx = 0
		self.col_idx = 0
		self.fig, self.axs = plt.subplots(ncols=nr_cols, nrows=nr_rows, \
			figsize=(fig_width, fig_height), layout="constrained")

	def level_name(self, level):
		return level

	def read_analysis(self, level, algo):
		fn = "../analysis/%s.%s.txt" % (algo, level)
		f = open(fn)
		hdr = f.readline()
		#                0	1	2	3			4
		if hdr != "tpr	epq	fpr	precision	score\n":
			sys.stderr.write("hdr=%s\n" % hdr)
			sys.stderr.write("fn=%s\n" % fn)
			assert False
		tprs = []
		epqs = []
		fprs = []
		precisions = []
		scores = []
		for line in f:
			if line.startswith("SEPQ"):
				break
			flds = line[:-1].split('\t')
			assert len(flds) == 5
			tpr = float(flds[0])
			epq = float(flds[1])
			fpr = float(flds[2])
			precision = float(flds[3])
			score = float(flds[4])

			tprs.append(tpr)
			fprs.append(fpr)
			epqs.append(epq)
			precisions.append(precision)
			scores.append(score)
	
		return tprs, epqs, fprs, precisions, scores

	def algo_fmt(self, algo):
		name = algo
		lw = 2
		ls = "solid"
		color = None

		if algo == "reseek_fast":
			name = "Reseek (fast)"
			color = "black"
			lw = 3
			ls = "dotted"
		elif algo == "reseek_v1.2":
			name = "Reseek v1.2"
			color = "gray"
		elif algo == "reseek_verysensitive":
			name = "Reseek (verysensitive)"
			color = "gray"
			ls = "dashed"
		elif algo == "reseek_sensitive":
			name = "Reseek (sensitive)"
			color = "black"
		elif algo == "blastp":
			name = "BLASTP"
			ls = "dotted"
			color = "lightgreen"
		elif algo == "dali":
			name = "DALI"
			color = "skyblue"
		elif algo == "tmalign" or algo == "TMalign":
			name = "TM-align"
			color = "magenta"
		elif algo == "foldseek":
			name = "Foldseek"
			lw = 3
			ls = "dotted"
			color = "orange"

		kwargs = {}
		kwargs["linewidth"] = lw
		kwargs["linestyle"] = ls
		if not color is None:
			kwargs["color"] = color
		return name, kwargs

	def get_ax(self):
		if self.nr_rows == 1:
			ax = self.axs[self.col_idx]
		elif self.nr_cols == 1:
			ax = self.axs[self.row_idx]
		else:
			ax = self.axs[self.row_idx, self.col_idx]
		return ax

	def inc_ax(self):
		sys.stderr.write(f"inc_ax {self.row_idx=} {self.col_idx=}\n")
		if self.row_idx >= self.nr_rows:
			assert False, "row_idx=%d, nr_rows=%d" % (self.row_idx, self.nr_rows)

		ax = self.get_ax()
		self.col_idx += 1
		if self.col_idx >= self.nr_cols:
			self.col_idx = 0
			self.row_idx += 1
		return ax

	def plot_pr(self, level, algos, show_legend = True):
		ax = self.inc_ax()
		ax.set_title("Precision-recall %s" % self.level_name(level))
		ax.ticklabel_format(axis='y', style='plain')
		ax.set_xlabel("Recall (fraction of all homologs found)")
		ax.set_ylabel("Precision (fraction hits correct)")

		for algo in algos:
			fn = "../analysis_%s/%s.txt" % (level, algo)
			tprs, epqs, fprs, precisions, scores = self.read_analysis(level, algo)
			name, kwargs = self.algo_fmt(algo)
			ax.plot(tprs, precisions, label=name, **kwargs)
		if show_legend:
			ax.legend()

	def plot_roc(self, level, algos, show_legend = True):
		ax = self.inc_ax()
		ax.set_title("ROC %s" % self.level_name(level))
		ax.ticklabel_format(axis='y', style='plain')
		ax.set_xlabel("FPR (fraction non-homolog hits)")
		ax.set_ylabel("TPR (fraction of all homologs found)")

		for algo in algos:
			fn = "../analysis_%s/%s.txt" % (level, algo)
			tprs, epqs, fprs, precisions, scores = self.read_analysis(level, algo)
			name, kwargs = self.algo_fmt(algo)
			ax.plot(fprs, tprs , label=name, **kwargs)

		if show_legend:
			ax.legend()

	def plot_cve(self, level, algos, show_legend = True, min_epq = 0.01, max_epq = 10):
		sys.stderr.write(f"plot_cve({level=}")
		ax = self.inc_ax()
		ax.set_title("CVE %s" % self.level_name(level))
		ax.ticklabel_format(axis='y', style='plain')
		ax.set_yscale('log')
		ax.yaxis.set_major_formatter(ScalarFormatter())
		if level == "fam1":
			ax.set_xticks(np.arange(0.0, 1.0, 0.1))
		else:
			ax.set_xticks(np.arange(0.0, 0.6, 0.1))
		ax.set_ylim(0.01, 10)
		ax.set_xlabel("Sensitivity (fraction of all homologs found)")
		ax.set_ylabel("False positive errors per query")

		for algo in algos:
			tprs, epqs, fprs, precisions, scores = \
			  self.read_analysis(level, algo)
			name, kwargs = self.algo_fmt(algo)

			xs = []
			ys = []
			for i in range(len(tprs)):
				tpr = tprs[i]
				epq = epqs[i]
				if epq >= min_epq and epq <= max_epq:
					xs.append(tpr)
					ys.append(epq)

			ax.plot(xs, ys, label=name, **kwargs)
		if show_legend:
			ax.legend()

	def plot_cves(self, levels, algos, svg_fn):
		for level in levels:
			self.plot_cve(level, algos) 
		self.fig.savefig(svg_fn)

	def plot_rocs(self, levels, algos, svg_fn):
		for level in levels:
			self.plot_roc(level, algos)
		self.fig.savefig(svg_fn)

	def plot_prs(self, levels, algos, svg_fn):
		for level in levels:
			self.plot_pr(level, algos) 
		self.fig.savefig(svg_fn)

	def plot_levels(self, style, levels, algos):
		n = len(levels)
		for i in range(n):
			level = levels[i]
			leg = (i == n-1)
			if style == "cve":
				self.plot_cve(level, algos, leg)
			elif style == "pr":
				self.plot_pr(level, algos, leg)
			elif style == "roc":
				self.plot_roc(level, algos, leg)
			else:
				assert False, style
