#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python3

import sys
from Bio import SeqIO

files = sys.argv[1:]

records = []

def get_name_and_seqlen(files):
    for genbank in files:
        with open(genbank) as gb:
                if gb.readline().startswith("LOCUS"):
                    print('The file {} already has a header.'.format(genbank))
                else:
                    
                    count = 0
                    nucl = ("a", "c", "g", "t", "n")
                    while "ORIGIN" not in gb.readline():
                        continue
                    for line in gb:
                        for char in line:
                            if char in nucl:
                                count += 1
                    records.append((genbank, genbank.split(".gb")[0], count))

def create_and_prepend_header(records):
    for record in records:
        with open(record[0], "r+") as gb:
            content = gb.read()
            gb.seek(0, 0)
            header = '''LOCUS       XXXXXXXX               {0} bp    DNA     circular INV 17-OCT-2017
SOURCE      mitochondrion {1}
  ORGANISM  {1}
FEATURES             Location/Qualifiers
     source          1..{0}
                     /organism="{1}"
                     /organelle="mitochondrion"
                     /mol_type="genomic DNA"'''.format(record[2], record[1])
            gb.write(header + '\n' + content)
            print('Header succesfully added to file {}.'.format(record[0]))

get_name_and_seqlen(files)
create_and_prepend_header(records)




