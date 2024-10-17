#!/bin/bash -e

./download_blast_binaries.bash

mkdir -p ../alns ../time ../sorted_alns

/bin/time -v -o ../time/blastp \
	../bin/blastp \
	-query ../data/scop40.fa \
    -db ../blastdb/scop40 \
    -evalue 10 \
    -outfmt 6 \
    > ../alns/blastp.tsv

echo Search done
ls -lh ../alns/blastp.tsv

cut -f1,2,11 ../alns/blastp.tsv \
  | sort -gk3 \
  > ../sorted_alns/blastp.tsv

ls -lh ../sorted_alns/blastp.tsv
