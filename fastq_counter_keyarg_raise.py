#!/usr/bin/env python
# coding: utf-8

import argparse
from Bio import SeqIO

class fastq_parser():
    def __init__(self, fastq, quick=False):
        self.name = fastq
        self.quick = quick

    def seqio(self):
        ##As SeqIO.parse returns a generator, we have to recreate the generator object
        ##after it is exhausted
        return(SeqIO.parse(self.name, "fastq"))

    def readcount(self):
        ##Generators load a single record at a time to the RAM.
        ##So, they are better than many other data structures in memory efficiency, but are slower
        ##To speed up the process a little, we can convert the generator into, for instance, a list
        ##But this will take its toll on the machine, RAMwise speaking
        if self.quick:
            return len(list(self.seqio()))
        else:
            return sum(1 for i in self.seqio())
    
    def basecount(self):
        if self.quick:
            return sum(len(i.seq) for i in list(self.seqio()))
        else:
            return sum(len(i.seq) for i in self.seqio())
    
    def basecount_gbp(self):
        return self.basecount()/1000000000


def args():
    parser = argparse.ArgumentParser(description="This script prints to screen the number of reads and bases (in Gbp) of a fastq file")
    parser.add_argument("-q", "--quick", action="store_true", default=False, help="Loads fastq file into memory. A bit faster, but can consume a lot of RAM - DEPRECATED: IT ACTUALLY TAKES LONGER (AT LEAST FOR SMALLER DATASETS)")
    parser.add_argument("fastq", type=str, metavar="fastq", nargs='*', help="Fastq file(s)")
    global args
    args = parser.parse_args()


if __name__ == "__main__":
    args()
    if args.quick:
        print("\n--quick option is deprecated. Please use without this flag\n")
        raise Exception
    for i in args.fastq:
        fastq = fastq_parser(i, quick=args.quick)
        print("{}:\t{} reads;\t{} bases;\t{} Gbp".format(fastq.name, fastq.readcount(), fastq.basecount(), fastq.basecount_gbp()))
