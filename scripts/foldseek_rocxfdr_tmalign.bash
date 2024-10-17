bench=/z/github/foldseek-analysis/scopbenchmark/scripts/bench.fdr.noselfhit.awk
## bench=../awk/bench_rce.awk
lookup=../data/dom_scopid.tsv
hits=../sorted_alns/TMalign.tsv
out=../rocxfdr/TMalign.rocxfdr

mkdir -p ../rocxfdr

$bench $lookup <(cat $hits) > $out
