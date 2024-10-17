#!/bin/bash -e

mkdir -p ../sorted_alns

if [ -s ../sorted_alns/TMalign.tsv ] ; then
	echo TMalign already done
else
	echo Sorting TMalign...
	sort -rgk3 ../alns/TMalign.txt \
		> ../sorted_alns/TMalign.tsv
	ls -lh ../sorted_alns/TMalign.tsv
fi

if [ -s ../sorted_alns/foldseekTM.tsv ] ; then
	echo foldseekTM already done
else
	echo Sorting foldseekTM...
	cut -f1,2,3 ../alns/foldseekTM.txt \
		| sort -rgk3 \
		| sed "-es/\.pdb//g" \
		> ../sorted_alns/foldseekTM.tsv
	ls -lh ../sorted_alns/foldseekTM.tsv
fi

if [ -s ../sorted_alns/foldseek.tsv ] ; then
	echo foldseek already done
else
	echo Sorting foldseek...
	cut -f1,2,11 ../alns/foldseek.txt \
		| sort -gk3 \
		| sed "-es/\.pdb//g" \
		> ../sorted_alns/foldseek.tsv
	ls -lh ../sorted_alns/foldseek.tsv
fi

if [ -s ../sorted_alns/CLE-sw.tsv ] ; then
	echo CLE-sw already done
else
	echo Sorting CLE-se
	cat ../alns/CLE-sw.txt \
		| tr ' ' '\t' \
		| sort -rgk3 \
		> ../sorted_alns/CLE-sw.tsv
	ls -lh ../sorted_alns/CLE-sw.tsv
fi

if [ -s ../sorted_alns/CE.tsv ] ; then
	echo CE already done
else
	echo Sorting CE...
	sort -rgk3 ../alns/CE.txt \
		> ../sorted_alns/CE.tsv
	ls -lh ../sorted_alns/CE.tsv
fi

if [ -s ../sorted_alns/dali.tsv ] ; then
	echo dali already done
else
	echo Sorting dali...
	sort -rgk3 ../alns/dali.txt \
		> ../sorted_alns/dali.tsv
	ls -lh ../sorted_alns/dali.tsv
fi

if [ -s ../sorted_alns/3Dblast.tsv ] ; then
	echo 3Dblast already done
else
	echo Sorteding 3Dblast...
	sort -rgk3 ../alns/3Dblast.txt \
		> ../sorted_alns/3Dblast.tsv
	ls -lh ../sorted_alns/3Dblast.tsv
fi

if [ -s ../sorted_alns/mmseqs2.tsv ] ; then
	echo mmseqs2 already done
else
	echo Sorting mmseqs2...
	cut -f1,2,10 ../alns/mmseqs2.txt \
		| sort -rgk3 \
		> ../sorted_alns/mmseqs2.tsv
	ls -lh ../sorted_alns/mmseqs2.tsv
fi
