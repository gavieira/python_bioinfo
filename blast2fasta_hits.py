#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
#from Bio import SearchIO ##SearchIO only storees up to 500 hits. Did not use it because of this limitation
import argparse


class fasta_parser():
    def __init__(self, fasta):
        self.fasta = fasta
        
    def create_seqio_object(self):
        return SeqIO.parse(self.fasta, 'fasta')
        
    def get_seq_by_size_range(self, min_seqsize, max_seqsize):
        for record in self.create_seqio_object():
            seqsize = len(record.seq)
            if seqsize >= min_seqsize and seqsize <= max_seqsize:
                yield record.format('fasta')
    
    def get_hit_ids(self, blast_result):
        hitlist = []
        with open(blast_result) as blast:
            for line in blast:
                hitlist.append(line.split("\t")[1]) #Second column (subjectid) 
        return hitlist

    def extract_hits_unordered(self, blast_result):
        hits = self.get_hit_ids(blast_result)
        for record in self.create_seqio_object():
            if record.id in hits:
                yield record.format('fasta')
                hits.remove(record.id)

    def extract_hits(self, blast_result):
        hits = self.get_hit_ids(blast_result)
        index = SeqIO.index(self.fasta, "fasta")
        for hit in hits:
            yield index[hit].format("fasta")

    def get_seq_in_blast_by_id(self, blast_result):
        for query in SearchIO.parse(blast_result, 'blast-tab'):
            for hit in query:
                for record in self.create_seqio_object():
                    if hit.id == record.id:
                        #print(hit.id, record.id)
                        yield record.format('fasta')


def arguments():
    parser = argparse.ArgumentParser(description="This script gets all hits in a blast search sorted by decreasing score")
    required = parser.add_argument_group("required arguments:")
    required.add_argument("-b", "--blast", type=str, required=True, help="Blast ouput file (-outfmt 6)")
    required.add_argument("-f", "--fasta", required=True, type=str, metavar="fasta", help="Fasta file")
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    parser = fasta_parser(args.fasta)
    #for record in parser.get_seq_in_blast_by_id(args.blast):
    for record in parser.extract_hits(args.blast):
    #for record in parser.extract_hits_unordered(args.blast):
        print(record, end='')
