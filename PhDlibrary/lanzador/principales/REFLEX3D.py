
import os


os.system("cp {}/savinsPhD/lanzador/exe/Reflex3D/* .".format(os.environ["SPM_SAVINSPHD_PATH"]))
#Incluido en el anterior
os.system("cp {}/savinsPhD/lanzador/exe/ROCS/tiempos.py .".format(os.environ["SPM_SAVINSPHD_PATH"]))