#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import re, sys

def write_CDSs_to_file():
    for i in sys.argv[1:]:
        with open ("{}.CDS.fa".format(i.rsplit(".", 1)[0]), "w") as CDS:
            coding_list = extract_CDS("Allenopithecus_nigroviridis_NC_023965.1.gb")
            for i in coding_list:
                CDS.write(i)

def extract_CDS(genbank):
    CDS_list = list()
    for record in SeqIO.parse(genbank, "genbank"):
        if record.features:
            for FEATURE in record.features:
                if FEATURE.type == "CDS":
                    raw_header = FEATURE.qualifiers.get("gene")
                    formatted_header = re.search("\[\'(\S+)\'\]", str(raw_header))
                    CDS_list.append(">{}\n{}\n".format(formatted_header.group(1), FEATURE.location.extract(record).seq))
    return(CDS_list)


write_CDSs_to_file()



