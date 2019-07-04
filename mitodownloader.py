#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mitodownloader.py

"""Download all RefSeq mitogenomes available for a taxon"""

__author__ = "Gabriel Alves Vieira"
__contact__ = "gabrieldeusdeth@gmail.com"


#https://www.ncbi.nlm.nih.gov/genome/browse#!/organelles - Use this URL to search manually for mitogenomes of a specific taxon

#This script:
#Downloads the csv containing the species and accession (other metadata included) of all RefSeq mitogenomes for the taxon
#Uses that information to download all mitogenomes (Using the Entrez module from Biopython)



import requests, argparse, csv, re
from Bio import Entrez



parser = argparse.ArgumentParser(description="Downloads all RefSeq mitogenome records available for a given taxon")
parser.add_argument("-f", "--fasta", action="store_true", default=False, help="Downloads records in fasta format (default: genbank)")
parser.add_argument("taxon", type=str, metavar="TAXON", help="Name of taxon of interest (only name, taxid won't work)")
args = parser.parse_args()



#def get_mitogenome_csv(taxon):
url = "https://www.ncbi.nlm.nih.gov/genomes/solr2txt.cgi?q=%5Bdisplay()%5D.from(GenomeAssemblies).usingschema(%2Fschema%2FGenomeAssemblies).matching(tab%3D%3D%5B%22Organelles%22%5D%20and%20type%3D%3D%5B%22mitochondrion%22%5D%20and%20q%3D%3D%22{0}%22)&fields=organism%7COrganism%20Name%2Clineage%7COrganism%20Groups%2Cstrain%7CStrain%2Cbiosample%7CBioSample%2Cbioproject%7CBioProject%2Csize%7CSize(Mb)%2Cgc_content%7CGC%25%2Ctype%7CType%2Creplicons%7CReplicons%2Cproteins%7CCDS%2Crelease_date%7CRelease%20Date&filename={0}_mitogenomes.csv&nolimit=on".format(args.taxon)
mitos_request = requests.get(url, allow_redirects=True)
mitos_csv = '{}.csv'.format(args.taxon)
records_dict = dict()

with open( mitos_csv, 'wb') as csvfile:
    csvfile.write(mitos_request.content)



#def extract_records_from_csv(mitos_csv):
with open(mitos_csv) as csvfile:
    readCSV = csv.reader(csvfile)
    next(readCSV, None)  # skip the headers
    for line in readCSV:
        species = line[0].replace(" ", "_")
        accession = line[8].split("/")[0] #There may be unformatted accessions (e.g. "MT:NC_014672.1")
        formatted_accession = re.search('^.*(NC_\d+\.\d).*$', accession)
        if formatted_accession:
            accession = formatted_accession.group(1)#So the valid accession will be pulled out using a regex extration group
            records_dict[species] = accession



def entrez_download(output_filename, accession, seq_format = "gb"):
    '''Downloads records from NCBI's nucleotide database.
    seq_format can be either "fasta" or "gb"(default)'''
    with open(output_filename, "w+") as record:
        handle = Entrez.efetch(db='nucleotide', id=accession, rettype=seq_format, retmode='text')
        record.write(handle.read())

#def download_mitogenomes(record_name, accession):
for k, v in records_dict.items():
    try:
        record_name_preffix = "{}_{}".format(k, v)
        if args.fasta:
            entrez_download(record_name_preffix + ".fa", v, "fasta")
        else:
            entrez_download(record_name_preffix + ".gb", v )        
        print("{} mitogenome downloaded succesfully".format(record_name_preffix))
    except:
        print("{} mitogenome could not be downloaded".format(record_name_preffix))
