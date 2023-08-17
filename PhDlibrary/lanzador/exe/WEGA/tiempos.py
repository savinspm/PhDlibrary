import time
import os
from sys import argv

command = ""
for i in range(2,len(argv)):
	command = command + argv[i] + " "

print command
start_time = time.time()

os.system(command)
outfile = open(argv[1], 'a') # Indicamos el valor 'w'.
outfile.write('{}\n'.format("%s" % (time.time()-start_time)))
outfile.close()
print("%s" % (time.time() - start_time))
