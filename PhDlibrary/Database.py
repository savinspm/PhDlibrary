""" 
This file contains some methods to process some databases 
"""

import os

def splitDatabase(input, output):
    file = open(input, "r")
    line = file.readline()
    foutput = open("temp.txt", "w")
    contador = 0
    while(line):
        if "@<TRIPOS>MOLECULE" in line:
            print(contador)
            foutput.close()
            contador += 1
            foutput = open ("{}chembl_{}.mol2".format(output,contador), "w")
        foutput.write(line)
        line = file.readline()
    foutput.close()
    os.remove("temp.txt")

