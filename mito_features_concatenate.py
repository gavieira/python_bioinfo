#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description="This script concatenates each CDS, rrna and trna feature in a genbank file into a new fasta sequence")
#parser.add_argument("-d", "--dloop", action="store_true", default=False, help="Adds D-loop region(s) to the concatamer")
parser.add_argument("-f", "--fasta", action="store_true", default=False, help="Automatically saves each concatamer in a fasta file (Default: Print multifasta to screen)")
parser.add_argument("-s", "--split", action="store_true", default=False, help="Splits each feature into a sequence instead of concatenating them")
parser.add_argument("genbank", type=str, metavar="genbank", nargs='*', help="Genbank file(s)")
args = parser.parse_args()

def write_concatenated_features_to_file():
    for i in args.genbank:
        features = str(concat_features(i))
        if args.fasta:
            with open ("{}.features.fa".format(i.rsplit(".", 1)[0]), "w") as fasta:
                fasta.write(features)
        else:
            print(features)
            

def concat_features(genbank):
    concat = ""
    wanted_features = ["CDS", "tRNA", "rRNA"]
#    if args.dloop: #
#        wanted_features.append("D-loop") #The annotation of the d-loop can be done in multiple ways (e.g. through a "D-loop" or misc_feature"), so this d-loop concatenation feature is not a trivial one.  
    for i in SeqIO.parse(genbank, "genbank"):
        organism = i.annotations.get("organism").replace(" ", "_")
        if not args.split:
            concat += ">{}\n".format(organism)
        for feature in i.features:
            if feature.type in wanted_features:
                seq = feature.location.extract(i.seq)
                if args.split:
                    feature_type = feature.qualifiers.get('product')[0]
                    concat += ">{} - {}\n{}\n".format(feature_type, organism, seq)
                else:
                    concat += seq
                    
    return(concat)

if __name__ == "__main__":
    write_concatenated_features_to_file()
    if len(args.genbank) == 0:
        parser.print_help()