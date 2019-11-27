#!/usr/bin/env python
# coding: utf-8


import argparse, os
from Bio import SeqIO

parser = argparse.ArgumentParser(description="This script converts nt seqs from multifasta files into aa seqs")
parser.add_argument("-f", "--frames", action="store_true", default=False, help="Convert all 3 frames into aa seqs")
parser.add_argument("fasta", type=str, metavar="fasta", nargs='*', help="Fasta file(s)")
args = parser.parse_args()

for i in args.fasta:
    fasta_file = SeqIO.parse(i, "fasta")
    print(i)
    if args.frames:
        output = "{}_aa_3frames.fa".format(os.path.splitext(i)[0])
    else:
        output = "{}_aa.fa".format(os.path.splitext(i)[0])
    with open(output, 'w+') as out:
        for rec in fasta_file:
            out.write(">" + rec.id + rec.description + '\n')
            out.write(str(rec.seq.translate() + '\n'))
            if args.frames:
                out.write(">" + rec.id + rec.description.strip() + ' - frame2\n')
                out.write(str(rec.seq[1:].translate() + '\n'))
                out.write(">" + rec.id + rec.description.strip() + ' - frame3\n')
                out.write(str(rec.seq[2:].translate() + '\n'))
