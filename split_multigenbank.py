#!/usr/bin/env python3

import sys
filename = sys.argv[1]
organism_name = list()
gb_record = list()


with open(filename) as multigb:
    mgb = (multigb.read().split("//")) #Reads the entire file, separating the records using the "//" line
    gb_record = mgb 
    multigb.seek(0) #Resets position to the start of file
    for line in multigb:
        if line.lstrip().startswith("ORGANISM"):
            line = line.strip().split(" ", 1)
            organism_name.append("{}.gb".format(line[1].strip().replace(" ", "_")))            

for i in range(len(organism_name)):
    with open(organism_name[i], "w") as gb:
        gb.write(gb_record[i].lstrip())
        gb.write("//")
