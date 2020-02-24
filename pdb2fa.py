#!/usr/bin/env python3
# coding: utf-8

from Bio.SeqUtils import seq1
import os, argparse

class pdb_atom_2_fasta():
    def __init__(self, pdb):
        self.pdb = pdb
        self.prefix = os.path.splitext(self.pdb)[0]
        self.parsed = self.pdb_parser()
        
    def pdb_parser(self):
        with open(self.pdb) as pdb:
            header = self.prefix
            seq = ''
            for line in pdb:
                if line.startswith("ATOM") and line.split()[2] == 'N':
                    seq += line.split()[3][:3].capitalize() #Ignore signals after 3rd aa letter
            return(header, seq)
    
    def check_seq(self):
        if self.parsed[1]:
            return True

    def generate_fasta1(self):
        return(">{}\n{}".format(self.parsed[0], seq1(self.parsed[1])))
    
    def generate_fasta3(self):
        return(">{}\n{}".format(self.parsed[0], self.parsed[1]))
        

def getArgs():
    parser = argparse.ArgumentParser(description="Extracts aa sequence from pdb (atom) files")
    parser.add_argument("--three-letter", action="store_true", default=False, help="Displays three-letter aminoacid code")
    parser.add_argument("pdb", type=str, metavar="pdb", nargs='*', help="Path to pdb file(s)")
    return parser.parse_args()


if __name__=='__main__':
    args = getArgs()
    for i in args.pdb:
        pdb_parser = pdb_atom_2_fasta(i)
        if pdb_parser.check_seq():
            if args.three_letter:
                print(pdb_atom_2_fasta(i).generate_fasta3())
            else:
                print(pdb_atom_2_fasta(i).generate_fasta1())
