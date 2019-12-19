#!/usr/bin/env python3
# coding: utf-8

import sqlite3, os, argparse


class blast_to_fasta:
    def __init__(self, fasta, overwrite=False):
        self.blast = fasta
        self.overwrite = overwrite
        self.db = "{}.db".format(os.path.splitext(self.blast)[0])
        self.columns = ('query_id', 'subject_id', 'identity', 'alignment_size', 'mismatches', 'gaps', 'query_begin', 'query_end', 'subject_begin', 'subject_end', 'evalue', 'score')    
    
    def extract_blast_fields(self):
        with open(self.blast) as blast:
            for line in blast:
                yield line.strip().split('\t')
    
    def create_database(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        if self.overwrite:
            cursor.execute("DROP TABLE IF EXISTS blast;")
        cursor.execute("CREATE TABLE blast (\
        query_id TEXT,\
        subject_id TEXT,\
        identity NUMERIC,\
        alignment_size INTEGER,\
        mismatches INTEGER,\
        gaps INTEGER,\
        query_begin INTEGER,\
        query_end INTEGER,\
        subject_begin INTEGER,\
        subject_end INTEGER,\
        evalue NUMERIC,\
        score NUMERIC\
        );")
        for field in self.extract_blast_fields():
            cursor.execute("INSERT INTO blast\
            {}\
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(self.columns), field)
        cursor.close()
        connection.commit()
        connection.close()                       


def argparse_run():
    parser = argparse.ArgumentParser(description="This script converts a blast search (needs -outfmt 6 flag)")
    parser.add_argument("-o", "--overwrite", action="store_true", default=False, help="Overwrite local database if it exists. Default:false")
    parser.add_argument("blast", type=str, metavar="blast", help="Blast results")
    return parser.parse_args()


if __name__ == '__main__':
    args = argparse_run()
    blast_data = blast_to_fasta(args.blast, overwrite=args.overwrite)
    blast_data.create_database()