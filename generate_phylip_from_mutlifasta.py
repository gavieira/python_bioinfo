#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser(description="Generates a 'phylip' alignment for PartitionFinder2")
parser.add_argument("-t", "--type", type=str, metavar="", default="DNA", help="Type of data: {Protein, RNA or DNA(default)}")
parser.add_argument("infile", type=str, metavar="infile", help="Path to fasta file")
args = parser.parse_args()

import subprocess
import re

clustal_alignment = "%s.clustal" % (args.infile.rsplit(".", 1)[0])
phylip_alignment = "%s.phylip" % (args.infile.rsplit(".", 1)[0])


def generate_alignment(multifasta, clustal_alignment):
    subprocess.run("clustalo-1.2.4-Ubuntu-x86_64 -i %s -t %s --infmt=fa -o %s --outfmt=clu --force --wrap=999999999" % (args.infile, args.type, clustal_alignment), shell=True) #Aligns sequences (clustal format, in order to convert to relaxed phylip and keep full sequence header)

def number_of_sequences(multifasta):
    with open(multifasta) as fasta:
        count = 0
        for line in fasta:
            if line.startswith(">"):
                count += 1
        return count

def alignment_seq_length(clustal_alignment):
    with open(clustal_alignment) as clustal:
        clustal.readline()
        clustal.readline()
        clustal.readline()
        return len(clustal.readline().split()[1].strip())

def generate_phylip(clustal_alignment, phylip_alignment, number_of_sequences, alignment_seq_length):
    with open(clustal_alignment) as clustal, open(phylip_alignment, "w") as phylip:
        phylip.write(" %d %s\n" % (number_of_sequences, alignment_seq_length))
        clustal.readline()
        for line in clustal:
            if re.search("^\S+\s+", line):
                phylip.write(line)

generate_alignment(args.infile, clustal_alignment)
generate_phylip(clustal_alignment, phylip_alignment, int(number_of_sequences(args.infile)), alignment_seq_length(clustal_alignment))

#print(format_phylip(phylip_alignment, number_of_sequences(args.infile)))
