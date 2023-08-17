# IMPORTS
import os
import glob
import PhDlibrary
from tqdm import tqdm
import time 
import pandas as pd 

ROOT_DIRECTORY = os.environ["SPM_ROOT_PATH"]

def getPartition():
	"""
	Partition in which to launch the jobs
	"""
	if os.environ["SPM_machine"] == "bullxual":
		return "cpu_sandybridge"
	
	
def generate_FDA_ROCS():

	script = "ROCS"
	database = "DB/test1"
	partition = getPartition()
	jobs = 2
	IDname = "FDA"
	# Creating a folder to store experiments.
	metaFolderExperiment = "{}_{}_{}_{}".format(PhDlibrary.Constant.timename(), script, (database.split("DB/", 1)[1]).split("/")[0], partition)
	os.mkdir(metaFolderExperiment)

	for protein in PhDlibrary.FDA5PROTEINS:
		print (protein)
		
		query = "DB/test1/{}.mol2".format(protein)
		
		lanzador(metaFolderExperiment,script, IDname, query, database, partition,jobs, "mol2")
		
##############################
###    GENERATION SCRIPTS EXPERIMENTS - LANZADOR
##############################

def lanzador(metaFolderExperiment, script, IDname, molQuery, folderDatabase, partition, nJobs, formatFile):

	#Get molecule format
	formatMol = formatFile
	
	#Name of the query molecule and of the database folder
	nombreMolQuery, ext = os.path.splitext(os.path.basename(molQuery))
	nombreDirectorioDatabase = os.path.basename(folderDatabase)
	
	# We define the folder where the whole experiment will be stored.
	carpetaExperimento = "{}/{}_{}_{}_{}".format(metaFolderExperiment, script,IDname, nombreMolQuery, nombreDirectorioDatabase)
	#carpetaExperimento = "{}_{}_{}".format("OP_SS", nombreMolQuery, nombreDirectorioDatabase)

	#If the folder with the experiment exists, we delete it and then create it.
	if(os.access(carpetaExperimento,os.F_OK)):
		os.system("rm -r {}".format(carpetaExperimento))
	
	#The directories are created
	os.mkdir(carpetaExperimento)
	os.mkdir("{}/outputJob".format(carpetaExperimento))
	os.mkdir("{}/errorJob".format(carpetaExperimento))
	os.mkdir("{}/txt".format(carpetaExperimento))
	os.mkdir("{}/molecules".format(carpetaExperimento))
	
	
	#we obtain the list of molecules to be executed
	print ("{}/{}/*.{}".format(ROOT_DIRECTORY, folderDatabase, formatMol))
	listFiles  = sorted(glob.glob("{}/{}/*.{}".format(ROOT_DIRECTORY, folderDatabase, formatMol))) 
	for i in range(0,len(listFiles)):
		listFiles[i], temp = os.path.splitext(os.path.basename(listFiles[i]))
	
	nlistFiles = len(listFiles)
	
	#We get all the files
	
	if (nJobs > nlistFiles):
		nJobs = nlistFiles

	racion = nlistFiles / nJobs
	# We distribute the files among the number of jobs.
	for i in range(0,nJobs):
		limiteInferior = racion*i
		limiteSuperior = limiteInferior+racion
		if(i == nJobs -1):
			limiteSuperior = nlistFiles

		# We create the SBATCH script
		namejob="{}_{}_j{}".format(script,nombreMolQuery.split("-")[0],i)#time.time())
		expfile = "{}/job-{}.sh".format(carpetaExperimento, i)
		outfile = open(expfile, 'w')

		outfile.write("#!/bin/bash -l\n")
		outfile.write("\n")
		#outfile.write("#SBATCH --mem-per-cpu=2GB\n")
		#outfile.write("#SBATCH -N 1						# Number of nodes\n")
		outfile.write("#SBATCH --partition={}			# Partition name\n".format(partition))
		#outfile.write("#SBATCH --exclusive=user			# it does not share with other users \n".format(partition))
		#outfile.write("#SBATCH --exclude=bullxual[01-04]\n")
		outfile.write("#SBATCH --job-name={}					# Job name\n".format(namejob))
		outfile.write("#SBATCH --output={}/outputJob/{}.o       # Log Folder\n".format(carpetaExperimento,namejob))
		outfile.write("#SBATCH --error={}/errorJob/{}.e         # Error folder\n".format(carpetaExperimento,namejob))
		outfile.write("\n")
		
		#outfile.write("ulimit -n 32768\n")
		outfile.write("cd {}\n".format(carpetaExperimento))
		outfile.write("\n")
	
		
		for j in range(int(limiteInferior),int(limiteSuperior)):
			if(script == "ROCS"):	
				comando = "{0} -query ../{1} -dbase {2}/{4}.{5} -prefix txt/RES{3}-fda -shapeonly".format("rocs", molQuery,folderDatabase, nombreMolQuery, listFiles[j],formatMol)		
			outfile.write(comando)
			outfile.write("\n")
				
		outfile.close()
	
	
		# Save the executable to a file
		jobfile = open("{}/joblist".format(metaFolderExperiment), "a")
	
		jobfile.write(expfile)
		jobfile.write("\n")
		jobfile.close()

