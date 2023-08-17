import os
import sys
import os.path
import time
import subprocess 

LIMIT  = 600
TIME =  120 #seconds
joblist = ""
content = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Checks that at least one parameter is passed as a parameter
if not (len(sys.argv)> 1):
    print("You have not indicated an archive of experiments [joblist]")
    sys.exit()

#Check that the first parameter exists
joblist = sys.argv[1]
if not (os.path.isfile(joblist)): 
    print("File does not exist ")
    sys.exit()

#Read the jobs
with open(joblist) as f:
    content = f.readlines()

#Execute one by one
CONDITION = ["squeue", "-u", "savins", "-p", "cpu_sandybridge,cpu_zen2,cpu_haswell,cpu_ivybridge"]
contador = 0
total = len(content)
for line in content:
    job = line.rstrip()

    p1 = subprocess.Popen( CONDITION, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["wc", "-l"], stdin=p1.stdout, stdout=subprocess.PIPE)

  
    tasks = int((p2.communicate()[0]).rstrip())
    
    while tasks > LIMIT:
        print("{}[{}] Running {}/{}. Retry in {} s.".format(bcolors.FAIL,time.strftime("%c"), int(os.popen("squeue -u savins | wc -l").read().rstrip()), LIMIT, TIME))
        time.sleep(TIME)
        p1 = subprocess.Popen(
            CONDITION, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["wc", "-l"], stdin=p1.stdout, stdout=subprocess.PIPE)
  
        tasks = int((p2.communicate()[0]).rstrip())
    
    print("{}[{}] Launching jobs {}/{}. Name: {}{}".format(bcolors.OKGREEN,time.strftime("%c"), contador, total, job,bcolors.OKBLUE))
    proc = subprocess.Popen( ["sbatch", line.rstrip()]).wait()
    #os.system("sbatch {}".format(line.rstrip()))
    
    contador = contador + 1

