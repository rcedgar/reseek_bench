bench=/z/github/foldseek-analysis/scopbenchmark/scripts/bench.fdr.noselfhit.awk
lookup=../data/dom_scopid.tsv
hits=../sorted_alns/dali.tsv
out=../rocxfdr/dali.rocxfdr

## bench=../awk/bench_rce.awk

mkdir -p ../rocxfdr

$bench $lookup <(cat $hits) > $out
