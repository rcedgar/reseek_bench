#!/bin/bash -e

level=$1

if [ x$level == x ] ; then
	echo Missing level
	exit 1
fi

for algo in TMalign dali foldseekTM CLE-sw 3Dblast mmseqs2 CE
do
	echo ===== $algo $level ======
	./top_hit.bash $algo score $level &
done

for algo in blastp geometricus foldseek reseek_fast reseek_sensitive reseek_verysensitive reseek_v1.2
do
	echo ===== $algo $level ======
	./top_hit.bash $algo evalue $level &
done
