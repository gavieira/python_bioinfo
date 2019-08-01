#!/usr/bin/env python3

import sys

#@C00127:104:HLMCVBCXY:1:1108:16133:2000 1:N:0:GAATTCGT+ATAGAGGC
#@C00127:104:HLMCVBCXY:1:1108:16133:2000 2:N:0:GAATTCGT+ATAGAGGC

files = sys.argv[1:]

for fastq in files:
    with open(fastq) as fastq:
        for line in fastq:
            if line.startswith("@"):
                line = line.strip().split()
                new_header = line[0] + "/" + line[1].split(":")[0]
                print(new_header)
            else:
                print(line.strip())
