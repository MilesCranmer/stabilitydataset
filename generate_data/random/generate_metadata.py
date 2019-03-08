import numpy as np
import pandas as pd
import rebound

path = '/mnt/ssd/workspace/stability/stabilitydataset/'

if rebound.__githash__ != 'db3ae2cea8f3462463d3e0c5788a34625bb49a9c':
    print('Need to checkout commit above for this to run correctly')
    exit()

pathtofolder = path+'data/random/'
pathtofc = pathtofolder+'final_conditions/runs/'
pathtosfc = pathtofolder+'final_conditions/shadowruns/'
df = pd.read_csv(pathtofolder+'random.csv', index_col=0)

df['m1'] = -1
df['m2'] = -1
df['m3'] = -1
df['instability_time'] = -1
df['shadow_instability_time'] = -1
df['Stable'] = -1

def metadata(row):
    fc = rebound.Simulation.from_file(pathtofc+'fc'+row['runstring'])
    row['m1'] = fc.particles[1].m
    row['m2'] = fc.particles[2].m
    row['m3'] = fc.particles[3].m
    row['instability_time'] = fc.t
    sfc = rebound.Simulation.from_file(pathtosfc+'fc'+row['runstring'])
    row['shadow_instability_time'] = sfc.t
    row['Stable'] = fc.t > 9.99e8
    return row

df = df.apply(metadata, axis=1)
df.to_csv(pathtofolder+'metadata.csv', encoding='ascii')
