#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
#import dask.dataframe as dd
import os, argparse

parser = argparse.ArgumentParser(description="This script removes annotationless genes/transcripts from Trinotate reports (that need to be converted from 'xls' to 'xlsx')")
parser.add_argument("trinotate_report", type=str, metavar="fasta", help="Trinotate report in .xlsx")
args = parser.parse_args()

df = pd.read_excel(args.trinotate_report, sep='\t')

df_filtered = df[(df.sprot_Top_BLASTX_hit != '.') | (df.sprot_Top_BLASTP_hit != '.') | (df.Pfam != '.') ]#Retains only columns with valid hits

df_filtered.to_excel("{}_filtered_report.xlsx".format(os.path.splitext(args.trinotate_report)[0]), index=False)
