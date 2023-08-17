import time
import os
from sys import argv

command = ""
for i in range(2,len(argv)):
	command = command + argv[i] + " "

outfile = open(argv[1], 'a')

start_time = time.time()
os.system(command)
total_time = time.time()-start_time

outfile.write('{}\n'.format("%s" % (total_time)))
outfile.close()

