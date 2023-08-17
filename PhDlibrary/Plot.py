"""
PETA pero si usas python2 main_pymol.py plotMolecules funciona.
"""
print(__doc__)
#!/usr/bin/env python2
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

import pymol
from argparse import ArgumentParser
# IMPORTS
import os
import os.path
import datetime
import pandas as pd
import glob 
import Search





from subprocess import Popen, PIPE, STDOUT
import time


def plot_pymol_a_couple_of_compounds(query, variable, rta):
    """
    This method evaluates a pair of compounds in a given position (passed by parameter)
    with another target function.
    It is passed the query path and the variable molecule,
    an array (rta, rotation_translation_array) of the form:
    [angle, x1,y1,z1,x2,y2,z2, deltax, deltay,deltaz].
    and the executable to be evaluated with
    """
    #The query is checked for existence
    if not os.path.exists(query):
        print("There is no query")
        return False
    
    #The query is checked for existence
    if not os.path.exists(variable):
        print("There is no variable")
        return False
    #The array is checked for 10 elements
    if not len(rta) == 10:
        print("Check the rotation and translation array:\n{}".format(rta))
        return False
    #It is checked that the rotation and translation script is in place.
    if not os.path.exists("OP_MRMS"):
        print("The rotation and translation script is not found.")
        return False
    
    #The variable molecule is rotated
    comando = "./OP_MRMS {} {} {} {} {} {} {} {} {} {} {}".format(variable,rta[0],rta[1],rta[2],rta[3],rta[4],rta[5],rta[6],rta[7],rta[8],rta[9])
    os.system(comando)
    new_name = "Rotated{}-{}.mol2".format(os.path.splitext(os.path.basename(query))[0],os.path.splitext(os.path.basename(variable))[0])
    os.rename("MolRotated.mol2", new_name)
    return plot_pymol(query,variable,new_name)
    
def plot_pymol(query,target, rotated):
    """Paints two molecules and rotates it using pymol
    
    Arguments:
        query {string} -- Path of the query molecule
        target {string} -- Path of the target molecule
        rotated {string} -- Path of the rotated molecule
    """
    print(query,target,rotated)
    pymol.cmd.load(query, "query")
    pymol.cmd.color("red", "query")
    pymol.cmd.load(target, "target")
    pymol.cmd.color("green", "target")
    pymol.cmd.load(rotated, "rotated")
    pymol.cmd.color("yellow", "rotated")
    configuration()
    query_name  = os.path.splitext(os.path.basename(query))[0]
    target_name = os.path.splitext(os.path.basename(target))[0]
    pymol.cmd.png("{}-{}.png".format(query_name,target_name), width="10cm", height="10cm", dpi=300)
    time.sleep(1)
    #addtext("{}.png".format(sinHS_sinmol2),"SS: {}".format(dict[ligando][0]), "bottom_mid")
    pymol.cmd.save("{}-{}.pse".format(query_name,target_name),'','pse',quiet=0)
    pymol.cmd.reinitialize()
    return True


def configuration():
    pymol.cmd.bg_color('white')
    pymol.cmd.show_as("sticks")
    pymol.cmd.orient("all")
    pymol.cmd.zoom("all", 1,  1, 0)
    pymol.cmd.clip("near", 0)
    pymol.cmd.color("white", "elem h")


def plot_pymol_N_compounds(path, numberofconsiderations):
    """Paint the top N compounds given a ranking and without considering yourself.
    
    Arguments:
        path {string} -- Folder where the rankings are stored *ranking.csv
        numberofconsiderations {int} -- Number of N first elements to be plotted
    """

    for ranking in sorted(glob.glob("{}/*ranking.csv".format(path))):
        df = pd.read_csv(ranking)
        
        query = ""
        target = ""
        for index, row in df.iterrows():
        
            if(index  == numberofconsiderations):
                break
            query = row["query"]
            target = row["target"]
            if query == target:
                continue
            print(query,target)
            #The full path of the compounds
            fullquery = Search.search_compound_path(query, database = "fda", formato= "mol2")
            fulltarget = Search.search_compound_path(target, database= "fda", formato = "mol2")
            array_parameters = [row["angle"], row["x1"], row["y1"], row["z1"], row["x2"], row["y2"], row["z2"], row["deltax"], row["deltay"], row["deltaz"]]
            
            plot_pymol_a_couple_of_compounds(fullquery,fulltarget,array_parameters)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-path', required=True,help='Input directory')
    parser.add_argument('-numbers',required = True, type=int,help='Ranking number')
    args = parser.parse_args()
    plot_pymol_N_compounds(args.path, args.numbers)