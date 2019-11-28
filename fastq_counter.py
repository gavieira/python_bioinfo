#!/usr/bin/env python
# coding: utf-8

import argparse
from Bio import SeqIO

class fastq_parser():
    def __init__(self, fastq):
        self.name = fastq

    def seqio(self):
        ##As SeqIO.parse returns a generator, we have to recreate the generator object
        ##after it is exhausted
        return(SeqIO.parse(self.name, "fastq"))

    def readcount(self):
        return sum(1 for i in self.seqio())
    
    def basecount(self):
        return sum(len(i.seq) for i in self.seqio())
    
    def basecount_gbp(self):
        return self.basecount()/1000000000




def args():
    parser = argparse.ArgumentParser(description="This script prints to screen the number of reads and bases (in Gbp) of a fastq file")
    parser.add_argument("fastq", type=str, metavar="fastq", nargs='*', help="Fastq file(s)")
    global args
    args = parser.parse_args()


if __name__ == "__main__":
    args()
    for i in args.fastq:
        fastq = fastq_parser(i)
        print("{}:\t{} reads;\t{} bases;\t{} Gbp".format(fastq.name, fastq.readcount(), fastq.basecount(), fastq.basecount_gbp()))



