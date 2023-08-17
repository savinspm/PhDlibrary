"""
    Different constant values and methods to be used in the rest of the files.
"""

import time 

FDA5PROTEINS = ["DB00014","DB00035","DB00050","DB00091","DB00093"]

DIRECTORIO_NFS = "/nfs/savins"

DUD_DB=["ace", "ache", "ada", "alr2", "ampc", "ar", "cdk2", "comt", "cox1", "cox2", "dhfr", "egfr", "er_agonist", "er_antagonist", "fgfr1", "fxa", "gart", "gpb", "gr", "hivpr", "hivrt", "hmga", "hsp90", "inha", "mr", "na", "p38", "parp", "pde5", "pdgfrb", "pnp", "ppar_gamma", "pr", "rxr_alpha", "sahh", "src", "thrombin", "tk", "trypsin", "vegfr2"]
DUDE_DB=["aa2ar","abl1","ace","aces","ada","ada17","adrb1","adrb2","akt1","akt2","aldr","ampc","andr","aofb","bace1","braf","cah2","casp3","cdk2","comt","cp2c9","cp3a4","csf1r","cxcr4","def", "dhi1","dpp4","drd3","dyr","egfr","esr1","esr2","fa7","fa10","fabp4","fak1","fgfr1","fkb1a","fnta","fpps","gcr","glcm","gria2","grik1","hdac2","hdac8","hivint","hivpr","hivrt","hmdh","hs90a","hxk4","igf1r","inha","ital","jak2", "kif11","kit","kith","kpcb","lck","lkha4","mapk2","mcr","met","mk01","mk10","mk14","mmp13","mp2k1","nos1","nram","pa2ga","parp1","pde5a","pgh1","pgh2","plk1","pnph","ppara","ppard","pparg","prgr","ptn1","pur2","pygm","pyrd","reni","rock1","rxra","sahh","src","tgfr1","thb","thrb","try1","tryb1","tysy","urok","vgfr2","wee1","xiap"]
LIG_DEC_DUDE = [ "decoys", "actives"]


def timename():
    """
    Returns the current time in the format 'YYYYMMDD-HHMMSS'.
    """
    return time.strftime("%Y%m%d-%H%M%S")

