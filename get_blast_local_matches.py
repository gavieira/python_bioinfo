#!/usr/bin/env python3

'''This script takes all matches from a BLAST search against a local database and uses the matches id to filter them.
One multifasta is generated for each query sequence.

Usage:

/path/to/get_blast_local_matches.py blast_result fasta file

'''

import sys
from Bio import SeqIO

blast_results = sys.argv[1] ##Has to be the "TABULAR" output ('-outfmt 6' flag in blastn 2.9.0)
fasta = sys.argv[2]


seqids = list()
with open("rrna18s.jararaca1.blast.txt") as blast:
    for line in blast:
        seqids.append(line.split("\t")[1])
               

with open("filtered_blast_matches.fa", "w") as matches:
    for record in SeqIO.parse("SRR1596063.Bjararaca_venom_transcript1.fasta", "fasta"):
        if record.id in seqids:
            matches.write(">{}\n{}\n".format(record.id, record.seq))

#Make this script store the query names on another list and save a single multifasta to each.
