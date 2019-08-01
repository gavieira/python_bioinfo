#!/usr/bin/env python3

from Bio import SeqIO
import sys
filename = sys.argv[-1]

for i in SeqIO.parse(filename, "genbank"):
    print(i.format("fasta"))