#!/usr/bin/env python3

'''Use this script to remove 'score' values from genbank records generated using Mitos Web Server annotation
Usage: python3 remove_score_seqin.py genbank_file'''

import sys

filename = sys.argv[-1]

with open(filename) as seqin:
    for line in seqin:
        if line.strip().startswith("score"):
            continue
        else:
            print(line, end='')
