#!/usr/bin/env python3

import sys
from functools import reduce
import re

subs = {
        "Name=":"",
        "gene":"CDS",
        "cox1":"gene=COX1; product=cytochrome c oxidase subunit I",
        "cox2":"gene=COX2; product=cytochrome c oxidase subunit II",
        "atp8":"gene=ATP8; product=ATP synthase F0 subunit 8",
        "atp6":"gene=ATP6; product=ATP synthase F0 subunit 6",
        "cox3":"gene=COX3; product=cytochrome c oxidase subunit III",
        "nad3":"gene=ND3; product=NADH dehydrogenase subunit 3",
        "nad5":"gene=ND5; product=NADH dehydrogenase subunit 5",
        "nad4l":"gene=ND4L; product=NADH dehydrogenase subunit 4L",
        "nad4":"gene=ND4; product=NADH dehydrogenase subunit 4",
        "nad6":"gene=ND6; product=NADH dehydrogenase subunit 6",
        "cob":"gene=CYTB; product=cytochrome b",
        "nad1":"gene=ND1; product=NADH dehydrogenase subunit 1",
        "nad2":"gene=ND2; product=NADH dehydrogenase subunit 2",
        "trnL2(taa)":"gene=trnL2-uua; product=tRNA-Leu; note=anticodon:uua",
        "trnK(ctt)":"gene=trnK-uug; product=tRNA-Lys; note=anticodon:uug",
        "trnD(gtc)":"gene=trnD-guc; product=tRNA-Asp; note=anticodon:guc",
        "trnG(tcc)":"gene=trnG-ggu; product=tRNA-Gly; note=anticodon:ggu",
        "trnS1(aga)":"gene=trnS1-ucu; product=tRNA-Ser; note=anticodon:ucu",
        "trnE(ttc)":"gene=trnE-guu; product=tRNA-Glu; note=anticodon:guu",
        "trnF(gaa)":"gene=trnF-ttc; product=tRNA-Phe; note=anticodon:ttc",
        "trnH(gtg)":"gene=trnH-cuc; product=tRNA-His; note=anticodon:cuc",
        "trnT(tgt)":"gene=trnT-ucu; product=tRNA-Thr; note=anticodon:ucu",
        "trnP(tgg)":"gene=trnP-ccu; product=tRNA-Pro; note=anticodon:ccu",
        "trnS2(tga)":"gene=trnS2-uca; product=tRNA-Ser; note=anticodon:uca",
        "trnL1(tag)":"gene=trnL1-ctu; product=tRNA-Leu; note=anticodon:ctu",
        "trnV(tac)":"gene=trnV-gtu; product=tRNA-Val; note=anticodon:gtu",
        "trnM(cat)":"gene=trnM-utg; product=tRNA-Met; note=anticodon:utg",
        "trnQ(ttg)":"gene=trnQ-cuu; product=tRNA-Gln; note=anticodon:cuu",
        "trnW(tca)":"gene=trnW-tgu; product=tRNA-Trp; note=anticodon:tgu",
        "trnC(gca)":"gene=trnC-gca; product=tRNA-Cys; note=anticodon:gca",
        "rrnL":"gene=rrnL; product=large subunit ribosomal RNA",
        "rrnS":"gene=rrnS; product=small subunit ribosomal RNA",
        "trnI(gat)":"gene=trnW-tgu; product=tRNA-Trp; note=anticodon:tgu",
        "trnN(gtt)":"gene=trnC-gca; product=tRNA-Cys; note=anticodon:gca",
        "trnA(tgc)":"gene=trnC-gca; product=tRNA-Cys; note=anticodon:gca",
        "trnR(tcg)":"gene=trnC-gca; product=tRNA-Cys; note=anticodon:gca"
        }
        
if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as gff:
        for line in gff:
            line = line.split()
            last_collumn = re.sub("-[0-9]$", "",line[8]) #Removes "-0" and "-1" from duplicated features
            last_collumn = reduce(lambda a, kv: a.replace(*kv), subs.items(), last_collumn) #Formats last collumn substituting key/values pairs
            print(line[0],
                    line[1],
                    line[2].replace("gene","CDS"),
                    line[3],
                    line[4],
                    line[5],
                    line[6],
                    line[7],
                    last_collumn, sep= "\t")
else:
    print("This script converts .gff files generated by MitosWebServer to a modified .gff that can be exported to the Artemis Annotation tool\nUsage: python3 mitos_to_artemis.py filename.gff")
