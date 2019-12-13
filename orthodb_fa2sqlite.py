#!/usr/bin/env python
# coding: utf-8

from Bio import SeqIO
import sqlite3, os, argparse


class orthodb_fa2sqlite:
    def __init__(self, fasta):
        self.fasta = fasta
        self.seqio = SeqIO.parse(self.fasta, 'fasta')
        self.db = "{}.db".format(os.path.splitext(self.fasta)[0])
        self.columns = ['fasta_id', 'description', 'pub_gene_id', 'pub_og_id', 'og_name', 'seq_size', 'level', 'seq']
    
    
    def seqio_parser(self):
        for rec in self.seqio:
            description = rec.description.split(" ", 1)[1]
            if not description.startswith("{"):
                description = "{{{}}}".format(description) #Need to add curly brackets to some lines. When using 'format', it is possible to escape the brackets using double brackets. Thus, we have three sets of brackets in order to add them to records missing them.
            seqio_dict = eval(description)
            seqio_dict.update({"fasta_id":rec.id, "seq":str(rec.seq), "seq_size":len(rec.seq)})
            yield(seqio_dict)
    
    
    def extract_values(self, dictionary):
        values = list()
        for key in self.columns:
            try: values.append(dictionary[key])
            except: values.append(None)
        return values
    
    def create_database(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS orthodb (\
                        fasta_id TEXT UNIQUE NOT NULL,\
                        description TEXT,\
                        pub_gene_id TEXT,\
                        pub_og_id TEXT,\
                        og_name TEXT,\
                        seq_size INTEGER,\
                        level INTEGER,\
                        seq TEXT NOT NULL\
                        );")
        for rec in self.seqio_parser():
            values = self.extract_values(rec)
            cursor.execute("INSERT INTO orthodb                        (fasta_id, description, pub_gene_id, pub_og_id, og_name, seq_size, level, seq)                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
        cursor.close()
        connection.commit()
        connection.close()                       


def argparse_run():
    parser = argparse.ArgumentParser(description="This script converts a orthodb (https://www.orthodb.org/) fasta file into a local database")
    parser.add_argument("fasta", type=str, metavar="fasta", help="Orthodb's fasta file")
    return parser.parse_args()


if __name__ == '__main__':
    args = argparse_run()
    ortho_data = orthodb_fa2sqlite(args.fasta)
    ortho_data.create_database()