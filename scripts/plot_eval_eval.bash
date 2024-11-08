#!/bin/bash -e

for level in sf half fold
do
	echo === $level ===
	../py/plot_eval_eval.py ../plots/eval_eval_$level.svg
done
