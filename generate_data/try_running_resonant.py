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

    q = ressummaryfeaturesxgb(sim, list(kwargs.values()))
    print(q)

    return True

# !rm ../data/resonant/simulation_archives/*runs/* 

filenames = []

new_seeds = list(range(10000+120000, 10005+120000))

from multiprocessing import Pool

from subprocess import call

def run_sim(seed):
    maxorbs = 1e5 #Set to small number like 5 if only relying on hook!
    initial_filename = 'test%.12d.bin'%(seed,)
    sim, filename = run_resonant2(seed, initial_filename, maxorbs=maxorbs, hook=hook, verbose=False)

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
        sim_shadow, filename_shadow = run_resonant2(seed, initial_filename, maxorbs=5, hook=hook, verbose=False, shadow=True)
        ic("Done shadow test")
    return filename

pool = Pool(35)
new_filenames = pool.map(run_sim, new_seeds)

