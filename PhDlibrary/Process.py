
import os
import glob
from tabulate import tabulate
import subprocess
import os.path as path
import sys
import time
import csv
import pandas as pd
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import shutil
import savinsPhD as savins
from tqdm import tqdm
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
import numbers




##################
#COMPRESS
##################s
def experimentsToCSV(folder, software):
	"""
		Compact the files in the errorJob, outputJob, txt and scripts.sh folder into 4 single files. 
	"""
	
	#Save the home directory and move to the working directory.
	currentdirectory = os.getcwd()
	os.chdir(folder)
	
	#if os.path.isfile("outputJob.csv"):
		
	#	return
	
	#ErrorJob
	file = "errorJob.txt"
	with open(file, 'w') as outfile:
		for fname in tqdm(sorted(glob.glob("errorJob/*"))):
			
			outfile.write("####################")
			outfile.write(fname)
			outfile.write("####################\n")
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)
			
			#os.remove(fname)
	
	#Output
	file = "outputJob.txt"
	with open(file, 'w') as outfile:
		for fname in tqdm(sorted(glob.glob("outputJob/*"))):
			with open(fname, "r") as infile:	
				outfile.writelines(infile.readlines())
			#os.remove(fname)
	with open("outputJob.txt", "r") as input_file, open("outputJob.csv", "w") as output_file, open("output_errorJob.csv", "w") as errorOutput_file:
		data = input_file.readlines()
		output_file.write("query,target,evals,poses,seconds,angle,x1,y1,z1,x2,y2,z2,deltax,deltay,deltaz,initscore,finalscore\n")
		for row in data:
			values = row.split()
			if len(values) != 17:
				line = ",".join(values)
				line += "\n"
				errorOutput_file.write(line)
				continue
			line = ",".join(values)
			output_file.write("{}\n".format(line))

	if os.path.isfile("outputJob.csv"):
		df = pd.read_csv("outputJob.csv")
		df = df.sort_values(by='finalscore', ascending=False)

	#Output
	file = "jobs.txt"
	with open(file, 'w') as outfile:
		for fname in tqdm(sorted(glob.glob("job-*.sh"))):
			outfile.write("####################")
			outfile.write(fname)
			outfile.write("####################\n")
			with open(fname) as infile:	
				for line in infile:
					outfile.write(line)
		
			
			#os.remove(fname)
	#txt

	file = "results.csv"
	error = open("error.txt","a") 
	with open(file, 'w') as outfile:
		writer = csv.writer(outfile)
		if software == "WEGA":
			writer.writerow(('filename','target', 'query', 'finalscore'))
			for fname in glob.glob("txt/*.txt"):
				name = os.path.splitext(os.path.basename(fname))[0]
				df = pd.read_csv(fname)
				a = df.iloc[0]
				fila = a.values.tolist()
				fila.insert(0, name)
				writer.writerow(fila)
				os.remove(fname)

		elif software == "ROCS":								
			writer.writerow(('Time','FullFilename','Name','ShapeQuery', 'Rank', 'TanimotoCombo', 'ShapeTanimoto','ColorTanimoto','FitTverskyCombo','FitTversky','FitColorTversky','RefTverskyCombo','RefTversky','RefColorTversky','ScaledColor','ComboScore','ColorScore','Overlap'))
			for fname in glob.glob("txt/*.rpt"):
				name = os.path.splitext(os.path.basename(fname))[0]
				#The tab-separated file is read
				df = pd.read_csv(fname, sep="\t")
				# The first row is obtained
				a = df.iloc[0]
				
				fila = a.values.tolist()
				#Delete the last row, which I don't know why it appears as NAN.
				fila = fila[:-1]
				# We write the name of the file
				fila.insert(0, os.path.abspath(fname))
				# We read the time that is in another file
				timefile = os.path.splitext(os.path.basename(fname))[0]
				timefile = timefile.split("_")[0]
				time = 0
				timefile = os.path.abspath("txt/{}.txt".format(timefile))
				with open(timefile) as f:
					time = float(f.readline().rstrip())
				fila.insert(0, time)
				# Once we have the complete list, we write to the summary file
				writer.writerow(fila)
				#os.remove(fname)
	error.close()
	#Back to the home directory
	os.chdir(currentdirectory)



###########
# SAVE
###########
def saveTable(table, path, headers):
	"""
	Stores in a txt, tex and csv file the data of a table. 
	You have to pass it the table, the path or file name and the table header.
	"""
	fout = open (path+".txt", "w")
	fout2 = open (path+".tex", "w")
	fout.write(tabulate(table, headers=headers, tablefmt="pipe"))
	fout.close()
	fout2.write(tabulate(table, headers=headers, tablefmt="latex"))
	fout2.close()
	df = pd.DataFrame(table, columns=headers)
	df.to_csv(path+".csv", index=False)

############
# FDA
############
def process_FDA_ROCS(inputPath):
	"""
	In a folder with the same name as the one being analysed but with the extension 
	_output, a ranking is generated for each
	ordered by value of the final objective function.
	In addition another file is created with a summary of all the data:
		name | files | errors | errors-nan | score(mean) | maxValue | minValue 
	"""
    
	tableSummary =[]

	#The output folder is created and the log files are deleted.
	outputPath = inputPath[:-1]
	outputPath = "{}_output/".format(outputPath)
	if not path.exists(outputPath):
		os.mkdir(outputPath)
	else:
		for i in glob.glob(outputPath+"log_*"):
			os.remove(i)


	folders = sorted(glob.glob(inputPath+'*'))
	#We go through the folders
	for ligand in savins.Constant.PROTEINSFDA40:
		for folder in folders:
			if folder.find("_{}_".format(ligand)) >= 0:
				print (folder)
				#We group the experiments and output files together.
				experimentsToCSV(folder, "ROCS")
				#We read all the results
				dffull = pd.read_csv(folder+'/results.csv')
				dferror = dffull[pd.isnull(dffull["ShapeTanimoto"]) | (dffull.ShapeTanimoto == 0)]
				dferror.to_csv("{}fda{}_error.csv".format(outputPath,ligand), index=False)
				#You remove the nan and the 0
				df1 = dffull[pd.notnull(dffull["ShapeTanimoto"])]
				df = df1[df1.ShapeTanimoto != 0]
				#Sort by value of the objective function and we obtain the values
				dfsort = df.sort_values(by=['ShapeTanimoto'], ascending=[False])
				dfsort.to_csv("{}{}_ranking.csv".format(outputPath,ligand), index=False)
				maxValue = df["ShapeTanimoto"].max()
				minValue = df["ShapeTanimoto"].min()
				#timeSeconds = df["time"].sum()
				archivos = len(df.index)
				meanValue = df["ShapeTanimoto"].mean()
				time = df["Time"].sum()
				errors = len(dffull.index) - len(df.index)
				#We save the data in the table
				row = [ligand,archivos,errors, time/60, minValue, meanValue, maxValue]
				tableSummary.append(row)
				break

	saveTable(tableSummary, "{}stats".format(outputPath), ["name", "filesOK", "nan-zero", "timeMIN",  "minscore", "meanscore", "maxscore"])

