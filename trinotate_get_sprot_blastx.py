#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os, argparse

parser = argparse.ArgumentParser(description="This script gets 3 columns (geneid, transcript_id, and a modified sprot_blastx_hit - containing only the id that ends at the first '^') from filtered Trinotate reports (which can be obtained using the script available at: https://github.com/gavieira/python_bioinfo/blob/master/filter_trinotate_report.py)")
parser.add_argument("trinotate_report", type=str, metavar="fasta", help="Filtered Trinotate report")
args = parser.parse_args()


df = pd.read_excel(args.trinotate_report, usecols=['#gene_id', 'transcript_id', 'sprot_Top_BLASTX_hit'])
df = df[df.sprot_Top_BLASTX_hit != '.']


frame = {'geneid': df.iloc[:,0], \
         'transcript_id': df.iloc[:,1], \
         'sprot_modified': df.sprot_Top_BLASTX_hit.map(lambda x: x.split('^')[0])}

result = pd.DataFrame(frame, columns=['geneid', 'transcript_id', 'sprot_modified'])

result.to_excel("{}_sprotmod.xls".format(os.path.splitext(args.trinotate_report)[0]), index=False)
