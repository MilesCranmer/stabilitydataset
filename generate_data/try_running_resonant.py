#!/usr/bin/env python
# coding: utf-8

# NOTES:
#  Workflow: 
#   - Run this file to get 1e4 sims
#     - Just do full set if it's short!
#     - Either guess whether it will be good, or if you calculate the full time, just do it then.
#   - Run the generate_data.py and generate_metadata.py in the MLstability folder to generate features and raw data, as well as the final instability time.

from runfunctions import run_resonant2, run_resonant, run_resonant_condition
import sys
sys.path.append('/mnt/ceph/users/mcranmer/MLstability/generate_training_data/')
from training_data_functions import gen_training_data, orbtseries, orbsummaryfeaturesxgb, ressummaryfeaturesxgb, normressummaryfeaturesxgb, ressummaryfeaturesxgb2
from warnings import filterwarnings
from icecream import ic
filterwarnings('ignore')
from collections import OrderedDict

kwargs = OrderedDict()
kwargs['Norbits'] = 1e4
kwargs['Nout'] = 1000

def hook(sim):
    """Gets the sim at 0 orbits."""

    #features = ressummaryfeaturesxgb(sim, list(kwargs.values()))
    return True

# !rm ../data/resonant/simulation_archives/*runs/* 

filenames = []

start = int(sys.argv[1])
step_size = 10*1000
end = start + step_size

new_seeds = list(range(start + 121000, end + 121000))

base = 'short_resonant_%.12d' % (start,)
folder_root = '../data/' + base 
import os
os.makedirs(folder_root, exist_ok=True)  # succeeds even if directory exists.
os.makedirs(folder_root + '/simulation_archives/runs/', exist_ok=True)
os.makedirs(folder_root + '/simulation_archives/shadowruns/', exist_ok=True)

from multiprocessing import Pool

from subprocess import call

explicitly_find_max_stability = True
max_stable_orbs = 1e5

def run_sim(seed):
    if explicitly_find_max_stability:
        maxorbs = max_stable_orbs
    else:
        maxorbs = 5
    initial_filename = 'test%.12d.bin'%(seed,)
    sim, filename = run_resonant2(seed, initial_filename, base=base, maxorbs=maxorbs, hook=hook, verbose=False)

    good_sim = True
    
    if sim is None:
        good_sim = False
    
    stable = sim.t > 0.999 * maxorbs
    too_unstable = sim.t < 1e4
    
    if stable or too_unstable:
        good_sim = False
        
    #sim.simulationarchive_snapshot(filename)
    if not good_sim:
        call(["rm", filename])
        return None
    
    ic("Nice system to test!")
    if good_sim:
        ic("Doing shadow test")
        sim_shadow, filename_shadow = run_resonant2(seed, initial_filename, base=base, maxorbs=5, hook=hook, verbose=False, shadow=True)
        ic("Done shadow test")
    return filename

pool = Pool(35)
new_filenames = pool.map(run_sim, new_seeds)

