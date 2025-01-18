#!/bin/bash -e

for mode in fast sensitive verysensitive
do
	./reseek_search_$mode.bash
done
