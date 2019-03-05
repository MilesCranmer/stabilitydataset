import numpy as np
import sys
from subprocess import call
import time
import pandas as pd

i = 11003

runstring = "{0:0=7d}.bin".format(i)
with open("sunnyvale.sh", "w") as of:
    of.write("#!/bin/bash -l\n")
    of.write("#PBS -l nodes=1:ppn=1\n")
    of.write("#PBS -q workq\n")
    of.write("#PBS -r n\n")
    of.write("#PBS -l walltime=48:00:00\n")
    of.write("#PBS -N stab{0}\n".format(i))
    of.write("# EVERYTHING ABOVE THIS COMMENT IS NECESSARY, SHOULD ONLY CHANGE nodes,ppn,walltime and my_job_name VALUES\n")
    of.write("cd $PBS_O_WORKDIR\n")
    of.write("module load gcc/5.4.0\n")
    of.write("source /mnt/raid-cita/dtamayo/stability/bin/activate\n")
    of.write("python runrandom.py {0} {1}\n".format(i, runstring))

call("chmod u=rwx sunnyvale.sh", shell=True)
call("qsub sunnyvale.sh", shell=True)
