#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO, AlignIO
import pandas
import argparse, itertools, subprocess, os

parser = argparse.ArgumentParser(description="This script runs all pairwise alignments for sequences in a multifasta file")
parser.add_argument("-u", "--unambiguous", action="store_true", default=False, help="Automatically replaces ambiguous characters with gap symbols ('-')")
parser.add_argument("multifasta", type=str, metavar="multifasta", help="Multifasta file")
args = parser.parse_args()

def main_func(multifasta):
    seqs_dict = split_sequences(multifasta)
    permutations_list = pairwise_permutations(seqs_dict)
    clustal_list = pairwise_clustalo(seqs_dict, permutations_list)
    if args.unambiguous:
        ambiguous_sites_as_gaps(clustal_list)
        unambiguous_check_length(clustal_list)
    excel_output_dict = clustal_parser(clustal_list)
    generate_excel_aln_summary(excel_output_dict)    

def split_sequences(multifasta):
    '''Receives a multifasta file, splits and stores each record in a dictionary, that is then returned by the function'''
    seqs_dict = dict()
    for rec in SeqIO.parse(args.multifasta, "fasta"):
        seqs_dict.update({rec.id : rec.seq.upper()}) ##Saves the sequence as uppercase
    print(seqs_dict)
    print("This multifasta contains {} sequences.".format(len(seqs_dict)))        
    return(seqs_dict)

def pairwise_permutations(seqs_dict):
    '''Receives a dictionary of multiple sequence entries (e.g. {header1 : seq1, header2 : seq2, ... headerN : seqN}) and returns a list of all possible pairwise permutations between the dictionary's keys.'''
    permutations = list()
    for a, b in itertools.combinations(seqs_dict.keys(), 2):
        permutations.append([a, b])
    print(permutations)
    return(permutations)

def pairwise_clustalo(seqs_dict, permutations_list):
    '''Uses the list of permutations and dictionary of sequences to generate a temporary fasta file for each pair of sequences. Then uses this temporary file as input for clustalo (needs to be installed in $PATH), outputing an alignment file in fasta format. Finally, it returns a list with the pairwise alignment filenames'''
    clustal_list = list()
    number_of_permutations = len(permutations_list)
    print("There are {} pairwise combinations for the alignment of these sequences".format(number_of_permutations))
    for i, seq_id in enumerate(permutations_list, 1):
        basename = "{}_vs_{}".format(seq_id[0], seq_id[1])
        clustal_output = "{}.fa".format(basename)
        clustal_error = "{}.err".format(basename)
        print("Running alignment {} ({} of {})".format(basename, i, number_of_permutations))
        with open("tempfile", "w") as tempfile, open(clustal_output, "w") as clustal_out, open(clustal_error, "w") as clustal_err:
            tempfile.write(">{}\n{}\n>{}\n{}".format(seq_id[0], seqs_dict[seq_id[0]], seq_id[1], seqs_dict[seq_id[1]]))
            alignment = subprocess.Popen(["clustalo", "-i", "tempfile"], stdout=clustal_out, stderr=clustal_err)
            alignment.wait()
            os.remove("tempfile")
            if os.path.getsize(clustal_output) !=0 and os.path.getsize(clustal_error) == 0:
                clustal_list.append(clustal_output)
                os.remove(clustal_error)
            else:
                print("There was a problem with the {} alignment. Check the file {}".format(basename, clustal_error))
    return(clustal_list)

def ambiguous_sites_as_gaps(clustal_list):
    print("Replacing ambiguous sites with gap characters...")
    data = str()
    for aln in clustal_list:
        data = str()
        data2 = str()
        print(aln)
        alignment = AlignIO.read(aln, "fasta")
        for index in [0, 1]: ##Index of each fasta record in the alignment - in this case, 0 and 1 (pairwi)
            valid_nucs = ["A", "T", "G", "C"]
            unambiguous_seq = str()
            for nuc in alignment[index].seq:
                if nuc in valid_nucs:
                    unambiguous_seq += nuc
                else:
                    unambiguous_seq += "-"
            data += ">{} : {}\n".format(alignment[index].id, len(unambiguous_seq))
            data2 += ">{}\n{}\n".format(alignment[index].id, unambiguous_seq)
        print(data)
        with open(aln, "w") as unambiguous_aln:
            unambiguous_aln.write(data2)          

def unambiguous_check_length(clustal_list):
    for file in clustal_list:
        length = set()
        aln = AlignIO.read(file, "fasta")
        for i in range(len(aln)):
            length.update([len(aln[i])])
        if len(length) == 1:
            print("The sequences in {} have the same length - {} - Conversion to unambiguous SUCCESSFUL!".format(file, length))
        else:
            print("The sequences in {} have different lengths - {} - Conversion to unambiguous FAILED!".format(file, length))
            
        
def clustal_parser(clustal_list):
    fields = ["Query MT", "Subject MT", "Total Alignment Sites", "Gapped Sites", "Valid Sites", "Identical Sites", "Variant Sites", "Identity Percentage"]
    excel_output_dict = {k : list() for k in fields}
    for file in clustal_list: ##First, we need to get each information from the alignment and assign it to a variable
        aln = AlignIO.read(file, "fasta")
        query_seq = aln[0].id
        subject_seq = aln[1].id
        total_aln_sites = aln.get_alignment_length()
        gap_sites = list()
        gap_sites_count = 0
        identical_sites = list()
        identical_sites_count = 0
        variant_sites = list()
        variant_sites_count = 0
        collumns = dict()
        for i in range(1, total_aln_sites + 1):
            collumns.update({i : aln[:, i-1]})
        for k, v in collumns.items(): ##Get number of gapped sites
            if "-" in v:
                gap_sites_count += 1
                gap_sites.append([k, v])
                #print(k, v)
                continue
            nucs_in_collumn = set()
            for i in [0,1]: ##Get number of identical and variable sites for pairwise alignment
                nucs_in_collumn.update([v[i]])
            if len(nucs_in_collumn) == 1:
                identical_sites_count += 1
                identical_sites.append([k, v])
            if len(nucs_in_collumn) > 1:
                variant_sites_count += 1
                variant_sites.append([k, v])
                #print(k, v)        
        valid_sites = total_aln_sites - gap_sites_count
        identity_percentage = round((identical_sites_count / valid_sites) * 100, 2)
        
        
        ##After getting the variables, the script generates a file for each pairwise alignment, with a summary of the alignment's data
        
        parser_output = "{}.clustalparser".format(file[:-3])        
        with open(parser_output, "w+") as cluparser:
            cluparser.write("Query sequence: {} - A {} \t T {} \t G {} \t C {} \t gaps {}\n".format(query_seq, aln[0].seq.count("A"), aln[0].seq.count("T"), aln[0].seq.count("G"), aln[0].seq.count("C"), aln[0].seq.count("-")))
            cluparser.write("Subject sequence: {} - A {} \t T {} \t G {} \t C {} \t gaps {}\n".format(subject_seq, aln[1].seq.count("A"), aln[1].seq.count("T"), aln[1].seq.count("G"), aln[1].seq.count("C"), aln[1].seq.count("-")))
            cluparser.write("Total alignment size: {}\n".format(total_aln_sites))
            cluparser.write("Gapped columns: {}\n".format(gap_sites_count))
            cluparser.write("Valid columns (Total - Gapped): {}\n".format(valid_sites))
            cluparser.write("Identical columns: {}\n".format(identical_sites_count))
            cluparser.write("Variant columns: {}\n".format(variant_sites_count))
            cluparser.write("Identity percentage - ((Identical collumns / Valid collumns) * 100): {} %\n".format(identity_percentage))
            cluparser.write("VARIANT SITES:\n")
            cluparser.write("Number\tAlignment_site\t{}_nt\t{}_nt\n".format(query_seq, subject_seq))
            [cluparser.write("{}\t{}\t{}\t{}\n".format(i, v[0], v[1][0], v[1][1])) for i, v in enumerate(variant_sites, 1)]
            cluparser.write("GAP SITES:\n")
            cluparser.write("Number\tAlignment_site\t{}_nt\t{}_nt\n".format(query_seq, subject_seq))
            [cluparser.write("{}\t{}\t{}\t{}\n".format(i, v[0], v[1][0], v[1][1])) for i, v in enumerate(gap_sites, 1)]
            cluparser.write("IDENTICAL SITES:\n")
            cluparser.write("Number\tAlignment_site\t{}_nt\t{}_nt\n".format(query_seq, subject_seq))
            [cluparser.write("{}\t{}\t{}\t{}\n".format(i, v[0], v[1][0], v[1][1])) for i, v in enumerate(identical_sites, 1)]

        ##Lastly, the script will save all data to a dictionary and return it. This dict will be used to create a pandas dataframe and write a excel spreadsheet
            
        excel_output_dict.get("Query MT").append(query_seq)
        excel_output_dict.get("Subject MT").append(subject_seq)
        excel_output_dict.get("Total Alignment Sites").append(total_aln_sites)
        excel_output_dict.get("Gapped Sites").append(gap_sites_count)
        excel_output_dict.get("Valid Sites").append(valid_sites)
        excel_output_dict.get("Identical Sites").append(identical_sites_count)
        excel_output_dict.get("Variant Sites").append(variant_sites_count)
        excel_output_dict.get("Identity Percentage").append(identity_percentage)
            
        #if (gap_sites_count + identical_sites_count + variant_sites_count) == total_aln_sites:
         #   print("The sum is correct")
        #else:
        #    print("There was a problem with the parsing")
        #print(aln[1].seq.count("-"))
        
    return(excel_output_dict)

def generate_excel_aln_summary(excel_output_dict):
    aln_summary = pandas.DataFrame(excel_output_dict)
    aln_summary.to_excel("Pairwise_alignment_summary.xlsx", index=False, sheet_name="Aln_summary")    

main_func(args.multifasta)