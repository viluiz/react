print('---------------------------------------------------------------')
print('Program developed by Vinicius L S Silva (vs1819) - 12.04.2022')
print('---------------------------------------------------------------')

import os, sys
import numpy as np
import shutil
import subprocess
#import libspud
import re
import time

# ==============================================================================
# Input parameters
# ==============================================================================
nparalel = 60
runs = 500000

# Ranges for the uniform distribution
Ca_range = (-0.35,0.7)
Cl_range = (-0.7,1.4)
Na_range = (-0.6,1.2)
K_range  = (-0.65,1.3)
N5_range = (-0.7,1.4)

base_file = 'cation_exchange.pqi'
copy_files = ['phreeqc.dat']
rundir = 'runs/'
# ==============================================================================
# Input parameters - End
# ==============================================================================

# Copy files to folder
for fl in copy_files:
    print('Copying ' + fl + ' to ' + rundir + ' ...', end='')
    shutil.copy(fl, rundir)
    print('Done!')
    
processes = []
filenames = []
logfile = []
for j in range(runs):

    filenames.append('cation_exchange_' + str(j) + '.pqi')

    if os.path.exists(filenames[-1]):
        #sys.exit('Error: directory already exists! \n dir: ' + os.path.abspath(dirnames[-1]))
        print('File already exists: ' + os.path.abspath(file_pqi))
        break 
    shutil.copy(base_file, rundir+filenames[-1])    
        
    print('Creating file '+rundir+filenames[-1]+' ... ', end='')
    
    with open(rundir+filenames[-1], 'r') as f:
        lines = f.readlines()
            
    for i, line in enumerate(lines):
        # find Ca
        if 'Ca ' in line:
            aux = np.random.uniform(Ca_range[0],Ca_range[1])
            aux = 0.0 if aux < 0.0 else aux
            lines[i] = re.sub(line.split()[1], str(aux), line)
        # find Cl
        if 'Cl ' in line:
            aux = np.random.uniform(Cl_range[0],Cl_range[1])
            aux = 0.0 if aux < 0.0 else aux
            lines[i] = re.sub(line.split()[1], str(aux), line)
        # find Na
        if 'Na ' in line:
            aux = np.random.uniform(Na_range[0],Na_range[1])
            aux = 0.0 if aux < 0.0 else aux
            lines[i] = re.sub(line.split()[1], str(aux), line)
        # find K
        if 'K ' in line:
            aux = np.random.uniform(K_range[0],K_range[1])
            aux = 0.0 if aux < 0.0 else aux
            lines[i] = re.sub(line.split()[1], str(aux), line)
        # find N(5)
        if 'N(5) ' in line:
            aux = np.random.uniform(N5_range[0],N5_range[1])
            aux = 0.0 if aux < 0.0 else aux
            lines[i] = re.sub(line.split()[1], str(aux), line)

    with open(rundir+filenames[-1], 'w') as f:
        lines = f.writelines(lines)


    print('Done!')

    # Check for finished jobs and write output to file
    while not len(processes) < nparalel:
        #time.sleep(10)
        for i, p in enumerate(processes):
            if p.poll() != None:
                print('Run '+rundir+filenames[i]+' finished! status:' + str(p.poll()))
                #subprocess.Popen(['rm','*.vtu'], cwd=dirnames[i])
                os.remove(rundir+filenames[i] + '.log')
                os.remove(rundir+filenames[i])                   
                processes.pop(i)
                filenames.pop(i)
                logfile[i].close()
                logfile.pop(i)
                break
     
    # Run case 
    logfile.append(open(rundir+filenames[-1] + '.log','w'))
    processes.append(subprocess.Popen(['phreeqc', filenames[-1]], cwd=rundir, stdout=logfile[-1], stderr=logfile[-1], close_fds=True))


# Check for finished jobs and write output to file
while len(processes) > 0:
    #time.sleep(10)
    for i, p in enumerate(processes):
        if p.poll() != None:
            print('Run '+rundir+filenames[i]+' finished! status:' + str(p.poll()))
            processes.pop(i)
            filenames.pop(i)
            logfile[i].close()
            logfile.pop(i)
            break
print('Finished!')
# ==============================================================================
# End
# ==============================================================================        
