import rebound
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import dask.dataframe as dd
import datetime
from subprocess import call
import sys

Norbits = sys.argv[1]
Nout = sys.argv[2]
name = sys.argv[3]

if name == 'random':
    if rebound.__githash__ != 'db3ae2cea8f3462463d3e0c5788a34625bb49a9c':
        print('Need to checkout commit above for this to run correctly')
        exit()
    
    pathtofolders = '/mnt/ssd/workspace/stability/stabilitydataset/data/random/'

tseriesfolder = pathtofolders+'shortruntseries'+str(datetime.datetime.now().date())+'Norbits'+Norbits+'Nout'+Nout
safolder = pathtofolders+'simulation_archives/runs/'

call('mkdir ' + tseriesfolder, shell=True)
call('cp ' + pathtofolders + 'metadata.csv ' + tseriesfolder + '/', shell=True)

Norbits = float(Norbits)
Nout = int(Nout)
times = np.linspace(0, Norbits, Nout)
np.save(tseriesfolder+'/times.npy', times)

def collision(reb_sim, col):
    reb_sim.contents._status = 5
    return 0

def runorbtseries(sa, times):
    sim = sa[0]
    sim.collision_resolve = collision

    val = np.zeros((Nout, 18))
    for i, time in enumerate(times):
        orbits = sim.calculate_orbits()
        for j, o in enumerate(orbits):
            val[i,6*j+0] = o.a
            val[i,6*j+1] = o.e
            val[i,6*j+2] = o.inc
            val[i,6*j+3] = o.Omega
            val[i,6*j+4] = o.pomega
            val[i,6*j+5] = o.M
        sim.integrate(time, exact_finish_time=0)
    return val

def orbtseries(row):
    if row['instability_time'] < 1.e4:
        return np.zeros((Nout, 18))

    sa = rebound.SimulationArchive(safolder+'sa'+row['runstring'])
    val = runorbtseries(sa, times)
    return val


def applyorbtseries(df):
    return df.apply(orbtseries, axis=1)

df = pd.read_csv(tseriesfolder+"/metadata.csv", index_col = 0)
ddf = dd.from_pandas(df, npartitions=24)
res = ddf.map_partitions(applyorbtseries, meta = (None, 'i8')).compute(scheduler='processes') 

Nsys = df.shape[0]
matrix = np.concatenate(res.values).ravel().reshape((Nsys, Nout, 18))
np.save(tseriesfolder+'/timeseries.npy', matrix)
