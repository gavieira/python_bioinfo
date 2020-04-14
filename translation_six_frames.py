#!/usr/bin/env python
# coding: utf-8


from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import os, argparse


parser = argparse.ArgumentParser(description="This script translates a nt sequence into six aa sequences, one for each frame")
parser.add_argument("-g", "--gencode", type=int, default=1, help="Genetic code table (Default: 1)")
parser.add_argument("fasta", type=str, metavar="fasta", help="Fasta file")
args = parser.parse_args()

output_file = "{}_sixframes.fasta".format(os.path.splitext(args.fasta)[0])

def remove_incomplete_codon(seq_obj):
    '''Removes incomplete codons when translating the frames'''
    remainder = len(seq_obj)%3
    if remainder == 0:
        return seq_obj
    else:
        return seq_obj[:-remainder]

with open(output_file, 'w+') as aa_fa:
    for dna_record in SeqIO.parse(args.fasta, 'fasta'):
        # use both fwd and rev sequences
        dna_seqs = [dna_record.seq, dna_record.seq.reverse_complement()]

        # generate all translation frames
        aa_seqs = (remove_incomplete_codon(s[i:]).translate(table=args.gencode) for s in dna_seqs for i in range(3))
        #aa_seqs = (s[i:].translate() for i in range(3) for s in dna_seqs)

        # select the longest one
        frame = 0
        for counter, orf in enumerate(aa_seqs, start=1):
            frame =  counter
            # write new record
            #Frame as description (1-3: forward; 4-6: reverse)
            aa_record = SeqRecord(orf, id=dna_record.description, description="Frame{}".format(frame))
            SeqIO.write(aa_record, aa_fa, 'fasta')