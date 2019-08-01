#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO

parser = argparse.ArgumentParser(description="This script runs all pairwise alignments for sequences in a multifasta file")
parser.add_argument("multifasta", type=str, metavar="multifasta", help="Multifasta file")
args = parser.parse_args()


