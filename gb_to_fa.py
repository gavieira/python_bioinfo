#!/usr/bin/env python3

import sys
filename = sys.argv[-1]
with open(filename) as gb:
    seq = ""
    nucl = ("a", "c", "g", "t", "n")
    accession = gb.readline().split()[1]
    description = gb.readline().rstrip().split(" ", 1)[-1]
    head = "> %s |%s " % (accession, description)
    while "ORIGIN" not in gb.readline():
        continue
    for line in gb:
        for char in line:
            if char in nucl:
                seq += char
    print(head)
    print(seq)
