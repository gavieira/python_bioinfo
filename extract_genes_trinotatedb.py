#!/usr/bin/env python
# coding: utf-8

import sqlite3, re, argparse


class trinotate_sql_parser:
    '''Class that holds and parses info extracted from the Trinotate sqlite database. 
    
    Usage: trinotate_parser = trinontate_sql_parser(gene_name, sqlite_database_name) '''
    
    def __init__(self, gene, sqlite):
        '''All parsed info is available as attributes'''
        self.gene = gene
        self.sqlite = sqlite
        self.rawdata = self.database_query()
        self.data = self.database_parser()
        self.id = self.data['id']
        self.description = self.data['description']
        self.seq = self.data['seq']
        
        self.fasta = self.convert_to_fasta()

    def database_query(self):
        '''Method that queries the given database for the specified gene name.
        Returns a list of tuples: [(Transcript_id, annotation, sequence), (Transcript_id2, annotation2, sequence2), ... ]'''
        conn = sqlite3.connect(self.sqlite)
        with conn:
            c = conn.cursor()
            if self.gene:
                gene_name = "%{}%".format(self.gene)
                c.execute("""SELECT transcript_id, annotation, sequence
                            FROM Transcript
                            WHERE annotation LIKE ?;""", (gene_name,))
            else:
                c.execute("""SELECT transcript_id, annotation, sequence
                            FROM Transcript""")
        return c.fetchall()

    def database_parser(self):
        '''Method that parsers the info retrieved from the query (dependent on the 'database_query' method).
        Returns a dictionary of lists {id:[id1,id2,...], description:[desc1, desc2,...], seq:[seq1,seq2,...]}'''
        query = self.database_query()
        parsed_data_dict = {"id":[], "description": [], "seq": []}
        for rec in query:
            parsed_data_dict["id"].append(rec[0])
            parsed_data_dict["seq"].append(rec[2])
            try:
                parsed_data_dict["description"].append(re.search('^.+RecName: Full=(.+?);\^.+$', rec[1]).group(1))
            except:
                parsed_data_dict["description"].append('')
        return parsed_data_dict

    def convert_to_fasta(self):
        '''Uses the parsed info from database_parser to generate fasta entries.
        Returns a list of all sequences in fasta format'''
        parsed_data = self.database_parser()
        fasta_list = list()
        for i in range(len(parsed_data["id"])):
            fasta_list.append(">{} {}\n{}".format(parsed_data['id'][i], parsed_data['description'][i], parsed_data['seq'][i]))
        return fasta_list

        
    def print_fasta(self):
        '''Prints all sequences to STDOUT (fasta format)'''
        for i in self.fasta:
            print(i)        

def argparse_run():
    parser = argparse.ArgumentParser(description="This script searches and extracts all occurrences of a gene from a Trinotate sqlite database")
    parser.add_argument("-g", "--gene", type=str, metavar="gene", default='', help="Gene name. (i.e. 'COX1'). Will extract every seq from database if not specified")
    parser.add_argument("sqlite", type=str, metavar="sqlite", help="Database file")
    global args
    args = parser.parse_args()

if __name__ == "__main__":
    argparse_run()
    mygenes = trinotate_sql_parser(args.gene, args.sqlite)
    mygenes.print_fasta()
