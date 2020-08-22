#!/usr/bin/env python3

from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description="This script converts genbank file(s) to fasta")
parser.add_argument("genbank", type=str, nargs='*', help="genbank file(s)")
args = parser.parse_args()

for gb in args.genbank:
    for i in SeqIO.parse(gb, "genbank"):
        print(i.format("fasta"))
