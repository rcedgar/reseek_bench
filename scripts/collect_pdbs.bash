#!/bin/bash -e

## ls /mnt/c/data/pdb/pdb/34 | head
# pdb134d.ent.gz
# pdb134l.ent.gz
# pdb234d.ent.gz
# pdb234l.ent.gz
# pdb334d.ent.gz
# pdb434d.ent.gz

mkdir -p ../full_pdbs
cd ../full_pdbs

dir=$c/data/pdb/pdb/

nf=0
for x in `cat ../data/pdbid_chain.txt | cut -f1`
do
	nn=`echo $x | sed "-es/.\(..\).*/\1/"`
	# echo $x $nn
	fn=$dir/$nn/pdb$x.ent.gz
	outfn=$x.pdb.gz
	if [ -s $fn ] ; then
		cp -v $outfn .
	else
		echo Not found $fn
		nf=$(($nf+1))
	fi
done

echo $nf not found
