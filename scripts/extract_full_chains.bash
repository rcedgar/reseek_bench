#!/bin/bash -e

mkdir -p ../full_chains
cd ../full_chains

for x in `cat ../data/pdbid_chain.txt | sed "-es/\t/@/"`
do
	pdbid=`echo $x | cut -d@ -f1`
	chain=`echo $x | cut -d@ -f2`
	c=`echo $chain | tr '[A-Z]' '[a-z]'`
	echo pdbid=$pdbid chain=$chain c=$c
	inpdb=../full_pdbs/$pdbid.pdb
	outpdb=${pdbid}$c.pdb
	if [ -s $outpdb ] ; then
		echo Done $outpdb
		continue
	fi
	if [ ! -s $inpdb ] ; then
		echo Not found $inpdb
		continue
	fi
	pdb_get_chain.py \
		--input ../full_pdbs/$pdbid.pdb \
		--chain $chain \
		--output $outpdb
done
