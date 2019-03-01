import numpy as np
import pandas as pd
import rebound

path = '/mnt/ssd/workspace/stability/stabilitydataset/data/random/'
pathtofc = path+'final_conditions/runs/'
df = pd.read_csv(path+'random.csv', index_col=0)

def metadata(row):
    fc = rebound.Simulation.from_file(pathtofc+'fc'+row['runstring'])
    row['instability_time'] = fc.t
    row['m1'] = fc.particles[1].m
    row['m2'] = fc.particles[2].m
    row['m3'] = fc.particles[3].m
    row['Stable'] = fc.t > 9.99e8
    return row

df = df.apply(metadata, axis=1)
df.to_csv(path+'metadata.csv', encoding='ascii')
