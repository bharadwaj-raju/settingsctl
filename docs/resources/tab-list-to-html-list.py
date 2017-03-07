#!/usr/bin/env python3

import sys

input_file = sys.argv[1]

print('<ul>')

with open(input_file) as f:
	for line in f:
		if not line.startswith('\t'):
			print('<ul>')
			print(line)
			print()

