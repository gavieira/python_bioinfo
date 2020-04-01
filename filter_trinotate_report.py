#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import os, argparse

parser = argparse.ArgumentParser(description="This script removes annotationless genes/transcripts from Trinotate reports (that need to be converted from 'xls' to 'xlsx')")
parser.add_argument("trinotate_report", type=str, metavar="fasta", help="Trinotate report in .xlsx")
args = parser.parse_args()


rawdata = pd.read_excel(args.trinotate_report)

df = pd.DataFrame(rawdata)
df = df[(df.sprot_Top_BLASTX_hit != '.') | (df.sprot_Top_BLASTP_hit != '.') | (df.Pfam != '.') ] #Retains only columns with valid hits

df.to_excel("{}_filtered.xlsx".format(os.path.splitext(args.trinotate_report)[0]), index=False)



