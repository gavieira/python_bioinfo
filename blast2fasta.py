#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
from Bio import SearchIO
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
    
    def get_seq_in_blast_by_id(self, blast_result):
        for hit in SearchIO.parse(blast_result, 'blast-tab'):
            for record in self.create_seqio_object():
                if hit.id == record.id:
                    yield record.format('fasta')


def arguments():
    parser = argparse.ArgumentParser(description="This script gets all queries with hits in a blast search")
    required = parser.add_argument_group("required arguments:")
    required.add_argument("-b", "--blast", type=str, required=True, help="Blast ouput file (-outfmt 6)")
    required.add_argument("-f", "--fasta", required=True, type=str, metavar="fasta", help="Fasta file")
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    parser = fasta_parser(args.fasta)
    for record in parser.get_seq_in_blast_by_id(args.blast):
        print(record, end='')
