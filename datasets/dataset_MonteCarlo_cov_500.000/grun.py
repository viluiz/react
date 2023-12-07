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
#Ca_range = (0.,1.5)
#Cl_range = (0.,1.5)
#Na_range = (0.,1.5)
#K_range  = (0.,1.5)
#N5_range = (0.,1.5)
range_ = (0.,1.5)

# Covariance
                  #Ca          #Cl          #K           #N5          #Na
mean_ = np.array([0.22965704, 0.81094941, 0.23277808, 0.38792678, 0.49928428])

                  #Ca          #Cl          #K           #N5          #Na
cov_ = np.array([[ 0.08067956,  0.09004931, -0.04467115, -0.08979056, -0.11494764],  #Ca
                [ 0.09004931,  0.25947697,  0.0115803 , -0.25872864, -0.19360073],  #Cl
                [-0.04467115,  0.0115803 ,  0.07631076, -0.01155068,  0.0097226 ],  #K
                [-0.08979056, -0.25872864, -0.01155068,  0.25798257,  0.19304832],  #N5
                [-0.11494764, -0.19360073,  0.0097226 ,  0.19304832,  0.22017284]]) #Na


L = np.linalg.cholesky(cov_)

# files
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

    # SOLUTION 0     
    #0.Ca  #1.Cl  #2.K  #3.N5  #4.Na    
    aux_cov = mean_ + L@np.random.randn(len(mean_))
    aux_cov[aux_cov<range_[0]] = range_[0]
    aux_cov[aux_cov>range_[1]] = range_[1]
    #print(aux_cov)
       
    for i, line in enumerate(lines):
        # find Ca
        if 'Ca ' in line:
            aux = str(aux_cov[0])
            lines[i] = re.sub(line.split()[1], aux, line)
        # find Cl
        if 'Cl ' in line:
            aux = str(aux_cov[1])
            lines[i] = re.sub(line.split()[1], aux, line)
        # find Na
        if 'Na ' in line:
            aux = str(aux_cov[4])
            lines[i] = re.sub(line.split()[1], aux, line)
        # find K
        if 'K ' in line:
            aux = str(aux_cov[2])
            lines[i] = re.sub(line.split()[1], aux, line)
        # find N(5)
        if 'N(5) ' in line:
            aux = str(aux_cov[3])
            lines[i] = re.sub(line.split()[1], aux, line)
            
        if "SOLUTION 1" in line:
            end_sol_0 = i
            break
            
    # SOLUTION 1    
    #0.Ca  #1.Cl  #2.K  #3.N5  #4.Na    
    aux_cov = mean_ + L@np.random.randn(len(mean_))
    aux_cov[aux_cov<range_[0]] = range_[0]
    aux_cov[aux_cov>range_[1]] = range_[1]
    #print(aux_cov)
            
    for i, line in enumerate(lines[end_sol_0:]):
        # find Ca
        if 'Ca ' in line:
            aux = str(aux_cov[0])
            lines[end_sol_0+i] = re.sub(line.split()[1], aux, line)
        # find Cl
        if 'Cl ' in line:
            aux = str(aux_cov[1])
            lines[end_sol_0+i] = re.sub(line.split()[1], aux, line)
        # find Na
        if 'Na ' in line:
            aux = str(aux_cov[4])
            lines[end_sol_0+i] = re.sub(line.split()[1], aux, line)
        # find K
        if 'K ' in line:
            aux = str(aux_cov[2])
            lines[end_sol_0+i] = re.sub(line.split()[1], aux, line)
        # find N(5)
        if 'N(5) ' in line:
            aux = str(aux_cov[3])
            lines[end_sol_0+i] = re.sub(line.split()[1], aux, line)
                      

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
