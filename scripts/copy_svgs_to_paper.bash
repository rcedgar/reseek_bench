#!/bin/bash -e

d=$doc/papers/reseek/revision_work/roc_figs

mkdir -p $d

cd ../results
/bin/cp -v `ls roc*.svg *pr*.svg | sort | uniq` $d
