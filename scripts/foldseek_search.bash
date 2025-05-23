#!/bin/bash -e

./download_foldseek_binary.bash
./download_scop40pdb.bash

query_pdbdir=../scop40pdb/pdb
db=../foldseek_db/scop40

tmpdir=/tmp/foldseek_tmp
rm -rf $tmpdir

mkdir -p ../foldseek_search
cd ../foldseek_search

/bin/time -v -o foldseek_search.time \
	../bin/foldseek \
	  easy-search \
	  $query_pdbdir \
	  $db \
	  foldseek.tsv \
	  $tmpdir

rm -rf $tmpdir
