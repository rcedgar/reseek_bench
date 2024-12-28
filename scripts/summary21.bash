#!/bin/bash -e

cd ../analysis

(grep SEPQ \
  reseek21_fast.sf2.txt \
  reseek_fast.sf2.txt;
echo ; \
grep SEPQ \
  reseek21_sensitive.sf2.txt \
  reseek_sensitive.sf2.txt ; \
echo ; \
grep SEPQ \
  reseek21_verysensitive.sf2.txt \
  reseek_verysensitive.sf2.txt) \
  | columns.py

cd ../time

echo
(grep laps \
  reseek21_fast \
  reseek_fast;
echo ; \
grep laps \
  reseek21_sensitive \
  reseek_sensitive ; \
echo ; \
grep laps \
  reseek21_verysensitive \
  reseek_verysensitive) \
  | sed "-es/(wa.*)://" \
  | columns.py

