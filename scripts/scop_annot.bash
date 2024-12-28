#!/bin/bash -e

cd ../data

grep -wFf doms.txt /z/a/res/scop/data_1.75/dir.des.scop.txt_1.75 \
  > scop_annot.tsv

cut -f5 scop_annot.tsv \
  | sed "-es/ /\t/" \
  | sed "-es/:.*//" \
  | sort \
  | uniq \
  > pdbid_chain.txt
