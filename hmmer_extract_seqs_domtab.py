#!/usr/bin/env python
# coding: utf-8

from Bio import SeqIO, SearchIO
import argparse

class domtab_parser():
    def __init__(self, domtab, program):
        self.domtab = domtab
        self.program = program   
    
    def get_domtab_dict(self):
        '''Generates a dictionary with the hit's id as key and its domains as a value'''
        domtab_dict = {hit.id:'|'.join(hit.hit_keys) for hit in SearchIO.parse(self.domtab, '{}3-domtab'.format(self.program))}
        return domtab_dict


def arguments():
    parser = argparse.ArgumentParser(description="This script gets all queries with hits in a blast search")
    parser.add_argument("-p", "--program", type=str, default="hmmscan", help='Hmmer3 program used (Default: hmmscan)')
    parser.add_argument("domtab", type=str, help="Table of per-domain hits")
    parser.add_argument("fasta", type=str, metavar="fasta", help="Fasta file")
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    seqs = SeqIO.parse(args.fasta, 'fasta')
    parser = domtab_parser(args.domtab, args.program)
    domtab_dict = parser.get_domtab_dict()
    for record in seqs:
        if record.id in domtab_dict: ##If there is a hit with that id...
                print(">{} {}\n{}".format(record.id, domtab_dict.pop(record.id), record.seq)) #Print seq's id, domains and sequence. Removes that seq from the domtab_dict (pop method).