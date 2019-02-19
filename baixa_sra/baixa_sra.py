#!/usr/bin/env python3

#accession = SRR5437752 (length 10)
#ftp://ftp.sra.ebi.ac.uk/vol1/srr/SRR543/002/SRR5437752
#Pattern = ftp://ftp.sra.ebi.ac.uk/vol1/accession[0:3].lower()/accession[0:6]/00accession[-1]/accession

#accession = ERR020102 (length 9)
#ftp://ftp.sra.ebi.ac.uk/vol1/err/ERR969/ERR969522
#Pattern = ftp://ftp.sra.ebi.ac.uk/vol1/accession[0:3].lower()/accession[0:6]//accession

import argparse
parser = argparse.ArgumentParser(description="Downloads sra files" )
parser.add_argument("filename", type=str, metavar="FILENAME", help="Path to file with multiple accessions (one per line)")
args = parser.parse_args()

import wget

def generate_ftp_link(accession):
    url = ""
    if len(accession) == 10:
        url = "ftp://ftp.sra.ebi.ac.uk/vol1/%s/%s/00%s/%s" % (accession[:3].lower(), accession[:6], accession[-1], accession)
    if len(accession) == 9:
        url = "ftp://ftp.sra.ebi.ac.uk/vol1/%s/%s/%s" % (accession[:3].lower(), accession[:6], accession)
    return url

if args.filename:
    with open(args.filename) as filename:
        for line in filename:
            try:    
                accession = line.split("\t")[0].strip()
                species = line.split("\t")[1].strip()
                print("Downloading ",accession,":", sep="")
                filename = wget.download(generate_ftp_link(accession), out="%s.%s.sra" % (accession, species))
                print()
            except:
                print("The",accession,"dataset could not be downloaded")
                continue

def get_max_read_length():
    pass
    #use sratoolkit's fastq-dump to generate a subset(or not) of reads with header
    #use regex to extract list of read sizes "length=([0-9]+)$"
    #identify max read length and use it as parameter for fastq-dump

