#!/usr/bin/env python2.7
#Parametros

import os

DIRECTORIO_RAIZ = "/home/savins/scratch/"
os.system("cp {}/savinsPhD/lanzador/exe/WEGA/wega2016 .".format(os.environ['SPM_SAVINSPHD_PATH']))
os.system("cp {}/savinsPhD/lanzador/exe/WEGA/tiempos.py .".format(os.environ['SPM_SAVINSPHD_PATH']))

