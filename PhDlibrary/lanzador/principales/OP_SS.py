
#Parametros

import os

os.system("cp /home/savins/jero/optipharm/OPTIPHARM/bin/OPShapeSimilarity .".format(
    os.environ['SPM_SAVINSPHD_PATH']))
os.system("chmod +x OPShapeSimilarity")
os.system("cp /home/savins/jero/optipharm/OPTIPHARM/bin/OPini.FMOL .".format(
    os.environ['SPM_SAVINSPHD_PATH']))

#os.system("cp {}/savinsPhD/lanzador/exe/OptiPharm/shapeSimilarity/OPShapeSimilarity .".format(os.environ['SPM_SAVINSPHD_PATH']))
#os.system("chmod +x OPShapeSimilarity")
#os.system("cp {}/savinsPhD/lanzador/exe/OptiPharm/shapeSimilarity/OPini.FMOL .".format(os.environ['SPM_SAVINSPHD_PATH']))
