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

java_min_int = -2147483648
gender_ordered = [u'female', u'male', u'transgender female', u'intersex', u"fa'afafine", u'transgender male', u'female animal', u'male animal', u'woman', u'genderqueer', u'kathoey']

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

snap = 'snapshot_data/'
snapshot_dates = os.listdir(snap)
latest = os.path.join(snap,max(snapshot_dates))
csvs = filter(lambda x: x.endswith('.csv'), os.listdir(latest))
if not len(csvs) == 1:
    raise Exception
else:
    index_data_file = os.path.join(latest,csvs[0])
df = pandas.read_csv(index_data_file, na_values=[java_min_int])

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
    


def make_reindex(snap_df):

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
    property_index_dir = latest + '/property_indexes'
    if not os.path.exists(property_index_dir):
        os.makedirs(property_index_dir)
    filename = '%s/%s-index.csv' % (property_index_dir, param)
    filepoint = open(filename, 'w')
    filepoint.write(gender_df.to_csv())
    filepoint.close()
