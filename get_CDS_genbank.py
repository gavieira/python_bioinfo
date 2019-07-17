#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import re
import argparse

parser = argparse.ArgumentParser(description="This script extracts CDS sequences from genbank files")
parser.add_argument("genbank", type=str, metavar="genbank", nargs='*', help="Genbank file(s)")
args = parser.parse_args()

def write_CDSs_to_file():
    for i in args.genbank:
        with open ("{}.CDS.fa".format(i.rsplit(".", 1)[0]), "w") as CDS:
            coding_list = extract_CDS(i)
            for i in coding_list:
                CDS.write(i)

def extract_CDS(genbank):
    CDS_list = list()
    for record in SeqIO.parse(genbank, "genbank"):
        for FEATURE in record.features:
            if FEATURE.type == "CDS":
                header = FEATURE.qualifiers.get("gene")[0]
                sequence = FEATURE.location.extract(record).seq
                CDS_list.append(">{}\n{}\n".format(header, sequence))
    return(CDS_list)

if __name__ == "__main__":
    write_CDSs_to_file()
    if len(args.genbank) == 0:
        parser.print_help()
