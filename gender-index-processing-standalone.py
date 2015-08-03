#this file is supposed to ingest a gender-index-data-*.csv file and output, small CSVs for each plot maker to read.
import pandas
import numpy
import math
import datetime
import os
import json
import pywikibot
from collections import defaultdict
import time
import shutil

java_min_int = -2147483648

#Tranforming QIDs into English labels.
enwp = pywikibot.Site('en','wikipedia')
wikidata = enwp.data_repository()

retrieved = dict()

def english_label(qid):
    if type(qid) is float:
        if math.isnan(qid):
            return qid
    #first see if we've done it
    try:
        return retrieved[qid]
    except KeyError:
        try:
            page = pywikibot.ItemPage(wikidata, qid)
            data = page.get()
            lab = data['labels']['en']
            retrieved[qid] = lab
            return lab
        except:
            retrieved[qid] = qid
            return qid

def engify_labels(df):
    qids = [str(q) for q in df.columns]
    labels = [english_label(qid) for qid in qids]
    df.columns = labels
    return df

snap = '/home/maximilianklein/snapshot_data/'
java_place = '/home/maximilianklein/Wikidata-Toolkit/wdtk-examples/results'
snapshot_dates = os.listdir(java_place)
latest_file_name = max(snapshot_dates)
latest_date = '-'.join(latest_file_name.split('.')[0].split('-')[-3:])
latest = os.path.join(java_place,latest_file_name)
#cp file over here and make property index
new_snap_location = os.path.join(snap,latest_date)
if not os.path.exists(new_snap_location):
    os.makedirs(new_snap_location)
copy_dest = os.path.join(new_snap_location,latest_file_name)
shutil.copyfile(latest, copy_dest)

df = pandas.read_csv(copy_dest, na_values=[java_min_int])

def split_column(q_str):
    if type(q_str) is float:
        if numpy.isnan(q_str):
            return [q_str] #returning this way so we can gurantee that column contains list
    if type(q_str) is str:
        qs = q_str.split('|')
        return qs[:-1] #cos the format will always end with a |

for column in ['gender', 'ethnic_group', 'citizenship', 'place_of_birth', 'site_links']:
    column_plural = column+'s'
    df[column_plural] = df[column].apply(split_column)
    del df[column]

###
#CULTURES
###
pobs_map = json.load(open('helpers/aggregation_maps/pobs_map.json','r'))
country_map = pandas.DataFrame.from_csv('helpers/aggregation_maps/country_maps.csv')

ethnic_group_map = json.load(open('helpers/aggregation_maps/mechanical_turk/ethnic_groups_map.json','r'))
citizenship_map = json.load(open('helpers/aggregation_maps/mechanical_turk/citizenship_map.json','r')) 

unknown_countries = list()

def map_pob(qid):
    if not type(qid) is str:
        return None
    else:
        try:
            country_list = pobs_map[qid]
        except:
            unknown_countries.append(qid)
            return None
        if len(country_list) == 0:
            return None
        else:
            country = country_list[0] #assumption
            culture = country_map.ix[country]['culture_name']
            return culture

def map_wrapper(m):
    def return_fun(qid):
        try:
            return m[qid]
        except KeyError:
            return None
    return return_fun



#order is important because it determines the preference we will use
col_map_fun = zip(['ethnic_groups', 'citizenships', 'place_of_births'],
                  [map_wrapper(ethnic_group_map),map_wrapper(citizenship_map), map_pob])

mismatch = pandas.DataFrame()
def determine_culture(row):
    culture = None
    for col, map_fun in col_map_fun:
        val = row[col]
        #print val
        if isinstance(val,list):
            val = val[0]
        guess = map_fun(val)
        if (culture is not None) and (guess is not None):
            if culture != guess:
                mismatch.append(row,ignore_index=True)
        if guess:
            culture = guess    
    return str(culture).lower() if culture else culture #to return None properly


df['culture'] = df.apply(lambda x: determine_culture(x), axis=1)
    
###
#WORLD MAP
###

modrecs = df.copy(deep=True)

modrecs['country'] = modrecs.apply(lambda x: map_pob(x), axis=1)
map_cit = map_wrapper(citizenship_map)
modrecs['citizenship'] = modrecs.apply(lambda x: map_cit(x), axis=1)
cdf = modrecs[['country','citizenship','gender']]

def combine_economy(row):
    cit = row['citizenship']
    cunt = row['country']
    return cit if cit else cunt
cdf['Economy_qid'] = cdf.apply(combine_economy,axis=1)
edf = cdf[cdf['Economy_qid'].apply(lambda x: x is not None)]
bios_count = len(edf)

edf['Economy'] = edf['Economy_qid'].apply(english_label)


country_perc = defaultdict(dict)
country_groups= edf.groupby(by='Economy')

for country, group in country_groups:
    nonmale = group[group['gender'] != 'Q6581097']['gender'].count()
    total = group['gender'].count()
    nm_perc = nonmale / float(total)
    country_perc[country]['Economy'] = country #for later on joining
    country_perc[country]['Score'] = nm_perc #for later on joining
    country_perc[country]['total']= total

wdf = pd.DataFrame.from_dict(country_perc, orient='index')

###
#REINDEX
###
def make_reindex(df):

    def int_dict_factory():
        return defaultdict(int)

    def nan_test(v):
        try:
            if math.isnan(v):
                return True
        except TypeError:
                return False
    #abstracted: we want year-gender, but also
    #gender-ethnicity -citizenship -place of birth, site-links

    params = list(df.columns)
    params.remove('qid')
    gender_param = {param:defaultdict(int_dict_factory) for param in params}

    for index, row in df.iterrows():
        row_data = {p : row[p] for p in params}
        for param in params:
            gender_dict = gender_param[param]
            vrs = row_data[param]
            genders = row_data['genders']
            if not nan_test(vrs):
                if not nan_test(genders):
                    for gender in genders:
                            if type(vrs) is list:
                                for var in vrs:
                                    gender_dict[gender][var] += 1
                            else: 
                                    gender_dict[gender][vrs] +=  1
                                    
    gender_dfs = {param: pandas.DataFrame.from_dict(gender_param[param], orient='columns') for param in params}
    return gender_dfs

reindexed_dfs = make_reindex(df)

for param, gender_df in reindexed_dfs.iteritems():
    engify_labels(gender_df)
    property_index_dir = os.path.join(new_snap_location, 'property_indexes')
    if not os.path.exists(property_index_dir):
        os.makedirs(property_index_dir)
    filename = '%s/%s-index.csv' % (property_index_dir, param)
    filepoint = open(filename, 'w')
    filepoint.write(gender_df.to_csv())
    filepoint.close()


