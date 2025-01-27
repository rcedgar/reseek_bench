#!/bin/bash -e

## ./download_foldseek_binary.bash
## ./download_scop40pdb.bash

if [ x$1 == x ] ; then
	echo Missing arg
	exit 1
fi

query_pdbdir=../scop40pdb/pdb
db=../foldseek_db/scop40

tmpdir=/tmp/foldseek_tmp
rm -rf $tmpdir

mkdir -p ../foldseek_search_s
cd ../foldseek_search_s

/bin/time -v -o foldseek_search.s$1.time \
	../bin/foldseek \
	  easy-search \
	  $query_pdbdir \
	  $db \
	  ../alns/foldseek_s$1.tsv \
	  $tmpdir \
	  -s $1

rm -rf $tmpdir
