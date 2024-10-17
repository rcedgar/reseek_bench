#!/bin/bash

if [ -s ../foldseek_db/scop40_ss.index ] ; then
	echo "foldseek db found"
	exit 0
fi

./download_scop40pdb.bash
./download_foldseek_binary.bash

mkdir -p ../foldseek_db
cd ../foldseek_db

/bin/time -v -o foldseek_createdb.time \
	foldseek createdb ../scop40pdb/pdb scop40
