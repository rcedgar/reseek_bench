#!/bin/bash -e

db=../foldseek_db/scop40

tmpdir=/tmp/foldseek_tmp
rm -rf $tmpdir

mkdir -p ../foldseek_search
cd ../foldseek_search

mkdir -p ../big_hits

/bin/time -v -o foldseek_search.time \
	foldseek-v10 \
	  easy-search \
	  $db \
	  $db \
	  ../big_hits/foldseek.scop40 \
	  $tmpdir \
	  --format-output query,target,evalue

head ../big_hits/foldseek.scop40
ls -lh ../big_hits/foldseek.scop40

rm -rf $tmpdir
