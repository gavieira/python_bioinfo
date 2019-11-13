#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import os
import argparse

parser = argparse.ArgumentParser(description="This script converts an ace file into a fasta containing the assembly consensus")
parser.add_argument("ace", type=str, metavar="ace", nargs='*', help="Ace file(s)")
args = parser.parse_args()

for i in args.ace:
    consensus = os.path.splitext(i)[0] + ".fasta"
    with open(consensus, "w") as consensus:
        for seq in SeqIO.parse(i, "ace"): #This script assumes that each ace has a single contig assembly
            consensus.write(seq.format("fasta").replace("-", "")) #The assembly generally contains gap characters "-" that need to be removed
