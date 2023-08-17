
# Parametros

import os

os.system(
    "ln -s {}/savinsPhD/lanzador/exe/MOSES/MOEAD_main .".format(os.environ['SPM_SAVINSPHD_PATH']))
os.system("chmod +x MOEAD_main")
os.system(
    "ln -s {}/savinsPhD/lanzador/exe/MOSES/calc_et .".format(os.environ['SPM_SAVINSPHD_PATH']))
os.system("chmod +x calc_et")
