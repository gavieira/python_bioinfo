#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser(description="Extracts fastq from sam files")
parser.add_argument("-P", "--paired", action="store_true", default=False, help="Generates two paired-end data files (unpaired reads included)")
parser.add_argument("infile", type=str, metavar="infile", help="Path to sam file")
args = parser.parse_args()

import re

def get_seq_and_qual_sam(sam):
    with open(sam) as sam:
        data = list()
        for line in sam:
            if line.startswith("@"): continue
            line = line.split("\t")
            data.append(tuple([line[0],line[9],line[10]])) ## generates a list of tuples: [(header,seq,qual),(header,seq,qual)]
        return data

def format_reads(sam):
    data = get_seq_and_qual_sam(sam)
    reads = list()
    for item in data:
        reads.append("@%s\n%s\n+\n%s" % (item[0],item[1],item[2])) ## prints in fastq file format
    return reads

def split_pairs(sam):
    reads1 = list()
    reads2 = list()
    for item in format_reads(args.infile):
        if re.search("^@.+[/.]1\n", item): #If the header ends with ".1" or "/1", the sequence goes to the list reads1 and vice-versa
            reads1.append(item)
        if re.search("^@.+[/.]2\n", item):
            reads2.append(item)
        else:
            continue
    return [reads1, reads2]

def write_pairs_to_files(sam):
    filename = args.infile.split("/")[-1]
    prefix = filename[:-4]
    paired1 = prefix+"_filtered_1.fastq" ## Creating the name of the filtered dataset
    paired2 = prefix+"_filtered_2.fastq"
    number_of_reads = len(format_reads(args.infile))
    with open(paired1, 'a') as fastq1, open(paired2, 'a') as fastq2: ##Creates two files and adds the reads to them
        for read1, read2 in zip(split_pairs(args.infile)[0], split_pairs(args.infile)[1]):
            fastq1.write(read1 + '\n' )
            fastq2.write(read2 + '\n')
    return ("All %s reads were written to the following files:\n'%s'\n'%s'" % (number_of_reads, paired1, paired2))

if args.paired:
    print(write_pairs_to_files(args.infile))

else:    
    for item in format_reads(args.infile):
        print(item)
