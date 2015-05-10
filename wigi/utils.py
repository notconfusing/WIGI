import pywikibot
import math
import numpy as np
import pandas


def english_label(qid, wikidata, retrieved=dict()):
    # TODO: write docstring
    if type(qid) is float:
        if math.isnan(qid):
            return qid
    # first see if we've done it
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


def engify_labels(df, wikidata, retrieved=dict(), index=False):
    # TODO: write docstring
    if index:
        axis = df.index
    else:
        axis = df.columns
    qids = [str(q) for q in axis]
    labels = [english_label(qid) for qid in qids]
    axis = labels


def split_column(q_str):
    # TODO: write docstring
    if type(q_str) is float:
        if np.isnan(q_str):
            return [q_str]
        # returning this way so we can gurantee that column contains list

    if type(q_str) is str:
        qs = q_str.split('|')
        return qs[:-1]  # cos the format will always end with a |


def is_or_has_country(qid, wikidata):
    # TODO: write docstring
    countries = list()
    page = pywikibot.ItemPage(wikidata, qid)
    data = page.get()
    claims = data['claims']
    for pid, claimlist in claims.iteritems():
        if pid == 'P17':
            # TODO: give some explainatory name to such magic numbers
            for claim in claimlist:
                countries.append(claim.target.title())
        if pid == 'P31':
            # TODO: give some explainatory name to such magic numbers
            for claim in claimlist:
                    if claim.target.title() == 'Q6256':
                        # TODO: give some explainatory name to such magic
                        # numbers
                        countries.append(qid)  # this actually is a  country
    return countries


def qid_to_country(qid, qid_countryqid):
    # TODO: write docstring
    if type(qid) is float:
        if math.isnan(qid):
            return 'no_data'
    else:
        return qid_countryqid[qid]


def aggregate_culture(qid_list, country_culture):
    # TODO: write docstring
    if not type(qid_list) is list and qid_list == 'no_data':
                return 'no_data'
    if len(qid_list) > 0:
        culture_name = country_culture[qid_list[0]]
        return culture_name
    else:
        return 'not_easily_aggregatable'


def export_for_crowd_aggregate(df, savename):
    crowd_source_export = pandas.DataFrame()
    crowd_source_export['qid'] = df.index
    crowd_source_export['en_label'] = \
            crowd_source_export['qid'].apply(lambda x: english_label(x).encode('utf-8'))
    crowd_source_export['aggregate_group'] = ''
    crowd_source_export.to_csv('helpers/%s_map.csv' % savename)
