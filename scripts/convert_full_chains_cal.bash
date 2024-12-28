#!/bin/bash -e

mkdir -p ../full_length_out
cd ../full_length_out

reseek -convert ../full_chains -cal full_chains.cal -nochainchar -fasta full_chains.fa
