#!/usr/bin/env python3

import sys, re
filename = sys.argv[-1]
with open(filename) as gb:
    seq = ""
    accession = gb.readline().split()[1]
    description = gb.readline().rstrip().split(" ", 1)[-1]
    head = "> %s |%s " % (accession, description)
    while "ORIGIN" not in gb.readline():
        continue
    for line in gb:
        nucl_match = re.search('^\s+\d+\s+(.+)$', line, re.IGNORECASE)
        if nucl_match:
            nucl = nucl_match.group(1).replace(" ", "")
            seq += nucl + "\n"
    print(head)
    print(seq)
