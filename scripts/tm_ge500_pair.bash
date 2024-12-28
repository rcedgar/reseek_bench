#!/bin/bash -e

x=`echo $1 | cut -d@ -f1`
y=`echo $1 | cut -d@ -f2`

mkdir -p ../tm_ge500

pdbdir=../full_chains_ge500

TMalign $pdbdir/$x.pdb $pdbdir/$y.pdb -outfmt 2 \
  > ../tm_ge500/$x.$y
