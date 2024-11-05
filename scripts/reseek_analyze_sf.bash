#!/bin/bash -e

for mode in fast sensitive verysensitive
do
	./analyze_sf.bash reseek_$mode evalue
done
