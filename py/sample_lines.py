#!/usr/bin/python3

import sys

fn = sys.argv[1]
n = int(sys.argv[2])

last_value = None
first = True
for line in open(fn):
	if first:
		sys.stdout.write(line)
		first = False
	flds = line.split('\t')
	fld2 = flds[2]
	try:
		value = int(float(fld2)*100)
	except:
		continue
	if last_value is None or value != last_value:
		sys.stdout.write(line)
		last_value = value
