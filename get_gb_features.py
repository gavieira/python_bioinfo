#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import argparse, itertools, subprocess, os

parser = argparse.ArgumentParser(description="This script extracts features from genbank files and puts each feature as a record in a multifasta file")
parser.add_argument("-f", "--features", type=str, default="CDS", help="Comma-separated feature types with no spaces between them (e.g. 'CDS,tRNA,rRNA') to be extracted from the genbank files. (Default: extracts CDS)")
parser.add_argument("genbank", type=str, metavar="genbank", nargs='*', help="Genbank file(s)")
args = parser.parse_args()

def write_concatenated_features_to_file():
    for i in args.genbank:
        with open ("{}.features.fa".format(i.rsplit(".", 1)[0]), "w+") as features:
            features.write(str(extract_features(i)))


def extract_features(genbank):
    feature_seq = ""
    wanted_features = args.features.split(",")
    #print("Trying to recover the following features: ", wanted_features, "\n")
    for i in SeqIO.parse(genbank, "genbank"):
        feature_count_dict = {i : 0 for i in wanted_features}
        for feature in i.features:
            if feature.type in wanted_features:
                feature_count_dict[feature.type] += 1
                feature_seq += ">{} - {}\n".format(feature.qualifiers.get('product')[0], i.annotations.get("organism").replace(" ", "_"))
                feature_seq += feature.location.extract(i.seq) + "\n"
        print("\n{}:".format(genbank))
        for i in wanted_features:
            print("{} {}".format(feature_count_dict.get(i), i))
    return(feature_seq)

if __name__ == "__main__":
    write_concatenated_features_to_file()
    if len(args.genbank) == 0:
        parser.print_help()