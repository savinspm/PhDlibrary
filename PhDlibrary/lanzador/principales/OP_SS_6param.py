
#Parametros

import os

os.system("cp {}/repositorios/optipharm_6param/OPTIPHARM_6params/bin/OPShapeSimilarity .".format(
    os.environ['SPM_SAVINSPHD_PATH']))
os.system("chmod +x OPShapeSimilarity")
os.system("cp {}/repositorios/optipharm_6param/OPTIPHARM_6params/bin/OPini.Million .".format(
    os.environ['SPM_SAVINSPHD_PATH']))

#os.system("cp {}/savinsPhD/lanzador/exe/OptiPharm/shapeSimilarity/OPShapeSimilarity .".format(os.environ['SPM_SAVINSPHD_PATH']))
#os.system("chmod +x OPShapeSimilarity")
#os.system("cp {}/savinsPhD/lanzador/exe/OptiPharm/shapeSimilarity/OPini.FMOL .".format(os.environ['SPM_SAVINSPHD_PATH']))
