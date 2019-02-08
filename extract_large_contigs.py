#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser(description="Prints contigs larger than a specified length in bp", epilog="'With great power comes great responsibility' -- Stan Lee (1922-2018)")
group = parser.add_mutually_exclusive_group()
#group.add_argument("-m", "--minlen", type=int, metavar="", default=False, help="Get all contigs longer than this value")
group.add_argument("-c", "--count", action="store_true", default=False, help="Get a list of all contigs and their size")
group.add_argument("-a", "--acc", type=str, metavar="", default=False, help="Get a single contig by ID (please provide description line without '>')")
group.add_argument("-r", "--range", type=str, metavar="", default=False, help="Get sequence of all contigs inside a min-max length. Please provide the lower and upper limits such as '12000-18000'")
parser.add_argument("infile", type=str, metavar="infile", help="Path to multifasta file")
args = parser.parse_args()

def split_multifasta(infile): ###Splits multifasta into a list of tuples containing header and sequence, respectively
    with open(infile) as f:
        header = [] #Collects the header line
        seq = "" #Temporary variable. Goes through all the lines collecting bases, until it reaches the next header
        seq_final = [] #When seq reaches the next header, it dumps the sequence into seq_final and has is reset to an empty string (to collect the next sequence)
        for line in f:
            if line[0] == ">":
                if seq != "": #seq only gets here two times: in the first it is empty. In the second, it has the whole sequence
                    seq_final.append(seq)
                header.append(line.strip()[1:]) ###Without the ">"
                seq = ""
            if line[0] != ">" and len(line) != 0:
                seq += line.strip()
        seq_final.append(seq) #Gets the last seq, that does not encounter another header line
    fasta_list = list(zip(header, seq_final)) ###Packs the two lists into a list of tuples "[(header1,seq1), (header2,seq2)]"
    fasta_list = sorted(fasta_list, key = lambda x: len(x[1]), reverse=True) #Sorts fasta_list by sequence length (decreasing order)
    return fasta_list

def count_multifasta(infile): ###Counts the number of nucleotides for all sequences
    fasta_list = (split_multifasta(infile))
    fasta_len = []
    for i in range(len(fasta_list)):
        fasta_len.append((fasta_list[i][0], len(fasta_list[i][1]))) ##Creates a new list of tuples, this time with the header and
    return fasta_len                                                ##sequence length in each tuple "[(header1,len1), (header2,len2)]"

def get_seq_by_acc(header): ###Gets a sequence from the multifasta using its header
    fasta_list = dict(split_multifasta(args.infile)) ##Converts list into dictionary
    return [header, fasta_list.get(header)]     ##Returns a list with the key-value pair. A "try - except" here would be nice.

'''
def get_seq_by_length(minlen): ###Gets all sequences longer than integer value of "--minlen" flag
    fasta_len = split_multifasta(args.infile)
    fasta_greater = []
    i = 0
    while len(fasta_len[i][1]) > minlen and i < len(fasta_len):
        fasta_greater.append(fasta_len[i])
        i += 1
    return fasta_greater
'''

def get_seq_in_range(contig_length_range): ###Generates a list of tuples with all contigs in the delimited size range
    fasta_len = split_multifasta(args.infile)
    contig_range = contig_length_range.split("-")
    contig_range = [ int(x) for x in contig_range ] ###Obtains a list with the upper and lower contig size limits
    lower_limit = min(contig_range)
    upper_limit = max(contig_range)
    contigs_in_range = []
    for i in range(len(fasta_len)): ###Obtains list of all contigs with size in range
        if int(len(fasta_len[i][1])) > upper_limit:
            continue
        elif int(len(fasta_len[i][1])) < upper_limit and int(len(fasta_len[i][1])) > lower_limit:
            contigs_in_range.append(fasta_len[i])
        elif int(len(fasta_len[i][1])) < lower_limit:
            return contigs_in_range ###Output = [(header_in_range1,seq_in_range1), (header_in_range2,seq_in_range2)]

if args.count:
    fasta_len = count_multifasta(args.infile)
    for i in reversed(range(len(fasta_len))): ####To display contigs in increasing order has proved to be more useful
        print(fasta_len[i][0], fasta_len[i][1], sep = "\t")

if args.acc:
    seq = get_seq_by_acc(args.acc)
    print(">%s\n%s" % (seq[0], seq[1]))

'''
if args.minlen:
    fasta_greater = get_seq_by_length(args.minlen)
    for i in range(len(fasta_greater)):
        print(">%s\n%s" % (fasta_greater[i][0], fasta_greater[i][1]))
'''

if args.range:
    contigs_in_range = get_seq_in_range(args.range)
    for i in range(len(contigs_in_range)):
        print(">%s\n%s" % (contigs_in_range[i][0], contigs_in_range[i][1]))
    

if args.count == args.acc == args.range ==  False and args.infile:
    print("Please provide one of the '-c', '-a' or '-r' flags")
