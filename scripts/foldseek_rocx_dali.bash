bench=/z/github/foldseek-analysis/scopbenchmark/scripts/bench.noselfhit.awk
lookup=../data/dom_scopid.tsv
hits=../sorted_alns/dali.tsv
out=../rocx/dali.rocx

mkdir -p ../rocx

$bench $lookup <(cat $hits) > $out

# ./bench.awk ../data/scop_lookup.fix.tsv <(cat ../alignResults/rawoutput/tmaln) > ../alignResults/rocx/tmaln.rocx
