import pandas
import os


def diff(fa, fb):
    dfa = pandas.DataFrame.from_csv(fa)
    dfb = pandas.DataFrame.from_csv(fb)

    removed_columns = dfa.columns.difference(dfb.columns)
    added_columns = dfb.columns.difference(dfa.columns)
    
    change = dfb - dfa
    return change


def find_folders():
    snapfolder = '/home/maximilianklein/snapshot_data'
    dates = os.listdir(snapfolder)
    sdates = sorted(dates)
    latest = sdates[-1]
    prev = sdates[-2]
    print os.path.join(os.path.join(snapfolder,latest),'property_indexes')

find_folders()
