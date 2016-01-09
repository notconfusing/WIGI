import pandas as pd
import scipy
import scipy.stats
import numpy as np

snap_dir = "/home/hargup/remotefs2/maximilianklein/snapshot_data"
wddob= dict()
wddob[2015] = pd.read_csv("{}/2015-07-28/property_indexes/dob-index.csv".format(snap_dir))
wddob[2016] = pd.read_csv("{}/2016-01-03/property_indexes/dob-index.csv".format(snap_dir))

h_pop = pd.read_csv("./historic_population.csv")

for key in wddob.keys():
    cols = list(wddob[key].columns)
    cols[0] = 'year'
    wddob[key].columns = cols

    df = wddob[key]

    year_start = -10000
    years = [year_start]
    pop = [1]

    for year_end in h_pop['year'][1:]:
        years.append(year_end)
        pop.append(df[(df['year'] > year_start) & (df['year'] < year_end)].sum()[1:].sum())
        year_start = year_end

    print(key)
    print(scipy.stats.pearsonr(pop, h_pop['pop']))
    print(scipy.stats.spearmanr(pop, h_pop['pop']))
