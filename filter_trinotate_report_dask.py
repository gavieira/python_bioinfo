#!/usr/bin/env python3
# coding: utf-8

#import pandas as pd
import dask.dataframe as dd
import os, argparse

parser = argparse.ArgumentParser(description="This script removes annotationless genes/transcripts from Trinotate reports (that need to be converted from 'xls' to 'csv')")
parser.add_argument("trinotate_report", type=str, metavar="fasta", help="Trinotate report in .csv")
args = parser.parse_args()

df = dd.read_csv(args.trinotate_report, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

df_computed = df[(df.sprot_Top_BLASTX_hit != '.') | (df.sprot_Top_BLASTP_hit != '.') | (df.Pfam != '.') ].compute() #Retains only columns with valid hits

df_computed.to_excel("{}_filtered.xls".format(os.path.splitext(args.trinotate_report)[0]), index=False)
