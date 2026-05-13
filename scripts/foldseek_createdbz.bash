#!/bin/bash


mkdir -p ../foldseek_db
cd ../foldseek_db

foldseek-v10 createdb /z/data/scop40pdb/pdb scop40
