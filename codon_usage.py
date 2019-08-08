#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import csv
import argparse

parser = argparse.ArgumentParser(description="This script calculates codon usage for CDSs in genbank files")
parser.add_argument("genbank", type=str, metavar="genbank", nargs='*', help="Genbank file(s)")
args = parser.parse_args()

codon_table = dict() ##How to put the different genetic codes in here? Does Biopython allow using these tables out of the box, without the need to create a dictionary?

def main_func():
    for i in args.genbank:
        raw_coding_list = extract_CDS(i)
        complete_coding_list = fix_truncated(raw_coding_list)
        print(complete_coding_list)
        codon_usage(complete_coding_list)

def extract_CDS(genbank):
    CDS_list = list()
    for record in SeqIO.parse(genbank, "genbank"):
        accession = record.id
        species_name = record.annotations.get("organism").replace(" ", "_")
        for FEATURE in record.features:
            if FEATURE.type == "CDS":
                gene = FEATURE.qualifiers.get("gene")[0]
                sequence = FEATURE.location.extract(record).seq
                CDS_list.append([accession, species_name, gene, sequence])
    return(CDS_list)

def fix_truncated(coding_list):
    not_trunc_cds_list = list()
    for i in coding_list:
        truncated_nucs = len(i[3]) % 3
        if truncated_nucs:
            #print("Truncated stop codon for gene {}".format(i[2]))
            #print("Before:{} truncated_nucs".format(len(i[3]) % 3))
            #print("Before: {}".format(i[3]))
            i[3] = i[3][:-truncated_nucs] + 'TAA'
            #print()
            #print("After: {}".format(i[3]))
            #print("After:{} truncated_nucs".format(len(i[3]) % 3))
            not_trunc_cds_list.append(i)
        else:
            not_trunc_cds_list.append(i)
    return(not_trunc_cds_list)
            
def codon_usage(not_truncated_cds_list):
    pass

    
if __name__ == "__main__":
    if len(args.genbank) == 0:
        parser.print_help()
    else:
        main_func()