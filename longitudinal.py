import pandas as pd
import numpy as np
import os
import pickle as pkl


def read_data(usepkl=True):

    try:
        pkl_file = open('./data.pkl', 'r')
        data = pkl.load(pkl_file)
    except (IOError, EOFError):
        # snap_dir = "/home/hargup/snapshot_data/snapshot_data"
        snap_dir = "/home/hargup/remotefs2/maximilianklein/snapshot_data"

        dates = os.listdir(snap_dir)
        dates.remove('newest')
        dates.remove('newest-changes')

        # date_used = []
        dataframes = []
        data = dict()
        for date in dates:
            filepath = "{}/{}/property_indexes/site_linkss-index.csv".format(snap_dir, date)
            try:
                df = pd.read_csv(filepath)
                # date_used.append(date)
                data[date] = df

                dataframes.append(df)
            except IOError:
                print("{} not found".format(filepath))

        pkl_file = open('./data.pkl', 'w')
        pkl.dump(data, pkl_file)

    return data


data = read_data()

# Processing
for date in data.keys():
    df = data[date]
    columns = list(df.columns)
    columns[0] = "site"
    if "female.1" in columns:
        columns[columns.index('female')] = 'female creature'
        columns[columns.index('female.1')] = 'female'

    df.columns = columns
    data[date] = df

# If we have to read from the server then it is better if I pickle the data

# Only choosing wiki's which are present in all dates
sites = list(set.intersection(*[set(x.iloc[:, 0]) for x in data.values()]))

sitedata = dict()
for site in sites:
    sitedf = pd.DataFrame()
    sitedf['date'] = list(data.keys())
    for gender in ['male', 'female']:
        sitedf[gender] = [float(data[date][data[date].site == site][gender]) for date in sitedf['date']]
    # We have to convert date to date time after the above line because date in
    # data is a string not a datetime object, and in above line we are
    # iterating on dates because I'm not sure if the order of data.keys() and
    # data.values() is same
    sitedf['date'] = pd.to_datetime(sitedf['date'])
    sitedf.index = sitedf['date']
    sitedf.sort_values('date')
    sitedata[site] = sitedf

male = pd.DataFrame()
female = pd.DataFrame()
male['date'] = pd.to_datetime(data.keys())
female['date'] = pd.to_datetime(data.keys())
for site in sites:
    male[site] = sitedata[site]['male']
    female[site] = sitedata[site]['female']

male.index = male['date']
female.index = female['date']
male.sort_values('date')
female.sort_values('date')
