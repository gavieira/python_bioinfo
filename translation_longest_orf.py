#!/usr/bin/env python
# coding: utf-8


from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import os, argparse


parser = argparse.ArgumentParser(description="This script translates a nt sequence into six aa sequences, keeping only the longest ORF for each record")
parser.add_argument("-g", "--gencode", type=int, default=1, help="Genetic code table (Default: 1)")
parser.add_argument("-m", "--minlen", type=int, default=0, help="Minimum aa sequence length (Default: 0)")
parser.add_argument("fasta", type=str, metavar="fasta", help="Fasta file")
args = parser.parse_args()

output_file = "{}_longestorfs.fasta".format(os.path.splitext(args.fasta)[0])

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
        aa_seqs = (remove_incomplete_codon(s[i:]).translate(table=args.gencode, to_stop=True) for s in dna_seqs for i in range(3))

        # select the longest one
        max_aa_num = 0
        frame = 0
        ##print(type(max_aa))
        for counter, orf in enumerate(aa_seqs, start=1):
            if len(orf) > max_aa_num:
                max_aa_num = len(orf)
                max_aa = orf
                frame = counter

        # write new record
        #If no ORF has identified (virtually impossible, but just in case), will not add that record to output file
        #Frame as description (1-3: forward; 4-6: reverse)
        if max_aa_num > args.minlen:
            aa_record = SeqRecord(max_aa, id=dna_record.description, description="Frame{} - length {}".format(frame, max_aa_num))
            SeqIO.write(aa_record, aa_fa, 'fasta')




