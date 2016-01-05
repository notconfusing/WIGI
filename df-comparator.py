import pandas
import os


def changes_between(fa, fb):
    dfa = pandas.DataFrame.from_csv(fa)
    dfb = pandas.DataFrame.from_csv(fb)

    removed_columns = dfa.columns.difference(dfb.columns)
    added_columns = dfb.columns.difference(dfa.columns)
    
    change_df = dfb - dfa
    return change_df


def find_dirs():
    snapdir = '/home/maximilianklein/snapshot_data'
    dates = os.listdir(snapdir)
    sdates = sorted(dates)
    latest = sdates[-1]
    prev = sdates[-2]
    latest_dir = os.path.join(os.path.join(snapdir,latest),'property_indexes')
    prev_dir = os.path.join(os.path.join(snapdir,prev),'property_indexes')
    latest_files = os.listdir(latest_dir)
    prev_files = os.listdir(prev_dir)
    changedir = os.path.join(latest_dir,'changes-since-{}'.format(prev))
    if not os.path.exists(changedir):
        os.makedirs(changedir)
   
    
    for ind_file in latest_files:
        if ind_file in prev_files:
            p_f = os.path.join(prev_dir, ind_file)
            l_f = os.path.join(latest_dir, ind_file)
            change_df = changes_between(p_f, l_f)
            
find_dirs()
