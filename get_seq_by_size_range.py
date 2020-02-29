#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import argparse

class fasta_parser():
    def __init__(self, fasta):
        self.fasta = fasta
        
    def create_seqio_object(self):
        return SeqIO.parse(self.fasta, 'fasta')
        
    def get_seq_by_size_range(self, min_seqsize, max_seqsize):
        for record in self.create_seqio_object():
            seqsize = len(record.seq)
            if seqsize >= min_seqsize and seqsize <= max_seqsize:
                yield record.format('fasta')


def arguments():
    parser = argparse.ArgumentParser(description="This script gets all fasta sequences contained within a length interval")
    required = parser.add_argument_group("required arguments:")
    required.add_argument("--min", type=int, required=True, help="Minimum sequence length")
    required.add_argument("--max", type=int, required=True, help="Maximum sequence length")
    required.add_argument("fasta", type=str, nargs="*", metavar="fasta", help="Fasta file(s)")
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    for fasta in args.fasta:
        parser = fasta_parser(fasta)
        for rec in parser.get_seq_by_size_range(min_seqsize=args.min, max_seqsize=args.max):
            print(rec, end='')
