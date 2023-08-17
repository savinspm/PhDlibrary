

#Parametros

import os

#os.system("cp {}/savinsPhD/lanzador/exe/OptiPharm/electrostaticSimilarity/OPElectrostatic .".format(os.environ['SPM_SAVINSPHD_PATH']))
os.system("cp /home/savins/repositorios/old_optipharm/optipharm/OPTIPHARM/bin/OPElectrostatic .".format(
    os.environ['SPM_SAVINSPHD_PATH']))
os.system("chmod +x OPElectrostatic")
os.system("cp /home/savins/repositorios/old_optipharm/optipharm/OPTIPHARM/bin/OPini.BEST .".format(
    os.environ['SPM_SAVINSPHD_PATH']))
#os.system("cp {}/savinsPhD/lanzador/exe/OptiPharm/electrostaticSimilarity/OPini.FMOL .".format(os.environ['SPM_SAVINSPHD_PATH']))
os.system("cp {}/.OpenEye/oe_license.txt .".format(os.environ['SPM_SAVINSPHD_PATH']))
