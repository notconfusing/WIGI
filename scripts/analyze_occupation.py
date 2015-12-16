#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pandas as pd
from wikidata_graph import *
import numpy as np


# these occupation nodes are too vague to directly convey any information
# in our analysis
useless_nodes = [('Q35120', 'entity'),
                 ('Q488383', 'object'),
                 ('Q223557', 'physical object'),
                 ('Q830077', 'subject'),
                 ('Q18336849', 'item with given name property'),
                 ('Q215627', 'person'),
                 ('Q16686022', 'natural physical object'),
                 ('Q7239', 'organism'),
                 ('Q2944660', 'lexical item'),
                 ('Q8171', 'word'),
                 ('Q82799', 'name'),
                 ('Q2382443', 'Biota'),
                 ('Q19088', 'eukaryote'),
                 ('Q964455', 'unikont'),
                 ('Q129021', 'opisthokont'),
                 ('Q729', 'animal'),
                 ('Q171283', 'Homo'),
                 ('Q164509', 'omnivore'),
                 ('Q5', 'human'),
                 ('Q7184903', 'abstract object'),
                 ('Q3249551', 'process'),
                 ('Q5127848', 'class'),
                 ('Q16889133', 'class'),
                 ('Q151885', 'concept'),
                 ('Q16686448', 'artificial object'),
                 ('Q1914636', 'activity'),
                 ('Q246672', 'mathematical object'),
                 ('Q217594', 'class'),
                 ('Q17008256', 'collection'),
                 ('Q36161', 'set'),
                 ('Q6671777', 'structure'),
                 ('Q4164871', 'position'),
                 ('Q390066', 'object composition'),
                 ('Q18844919', 'group'),
                 ('Q17519152', 'group of objects'),
                 ('Q16334298', 'living thing group'),
                 ('Q386724', 'work'),
                 ('Q15222213', 'artificial physical object'),
                 ('Q336', 'science'),
                 ('Q853614', 'identifier'),
                 ('Q216353', 'title'),
                 ('Q28877', 'good'),
                 ('Q2424752', 'product'),
                 (u'Q2996394', 'biological process'),
                 ('Q16334295', 'group of humans'),
                 (u'Q39546', u'tool'),
                 (u'Q327055', u'worker'),
                 (u'Q15296531', u'position of authority'),
                 (u'Q223973', u'godparent'),
                 (u'Q2500638', u'creator'),
                 (u'Q43229', u'organization'),
                 (u'Q6765918', u'wrong'),
                 (u'Q874405', 'social group'),
                 (u'Q82604', u'design'),
                 (u'Q286583', u'manifestation'),
                 (u'Q851587', u'business process'),
                 (u'Q43445', u'female creature'),
                 (u'Q43229', u'organization'),
                 (u'Q483247', u'phenomenon'),
                 (u'Q6023923', u'List of Internet phenomena'),
                 (u'Q2353296', u'List of military commanders'),
                 (u'Q702269', u'professional'),
                 (u'Q7569', u'child'),
                 (u'Q6422240', u'property'),
                 (u'Q157146', u'French Resistance'),
                 (u'Q18706712', u'ice cross downhiller'),
                 (u'Q349', u'sport'),
                 (u'Q11028', u'information'),
                 (u'Q48282', u'student'),
                 (u'Q3809586', u'Wikipedian in Residence'),
                 (u'Q368758', u'white-collar worker'),
                 (u'Q1005490', u'self-employment'),
                 (u'Q126552', u'business informatics'),
                 (u'Q7810129', u'title of authority'),
                 (u'Q204686', u'winter sport'),
                 (u'Q602884', u'social phenomenon'),
                 (u'Q11862829', u'academic discipline'),
                 (u'Q31629', u'type of sport'),
                 (u'Q618779', u'award'),
                 (u'Q216353', u'title'),
                 (u'Q15619164', u'abstract being'),
                 (u'Q451967', u'action'),
                 (u'Q735', u'art'),
                 (u'Q2500638', u'creator'),
                 (u'Q8425', u'society'),
                 (u'Q49848', u'document'),
                 (u'Q340169', u'communication medium'),
                 (u'Q17584038', u'oral media'),
                 (u'Q93184', u'drawing'),
                 (u'Q1209283', u'electronic media'),
                 (u'Q732577', u'publication'),
                 (u'Q11033', u'mass media'),
                 (u'Q15610833', u'internet-based work'),
                 (u'Q234460', u'text'),
                 (u'Q1186952', u'interactive media'),
                 (u'Q571', u'book'),
                 (u'Q6581072', u'female'),
                 (u'Q901', u'scientist'),  # Not useless exactly but we need finer classes here
                 (u'Q203066', u'relation'),
                 (u'Q5410500', u'faith'),
                 (u'Q4830453', u'business'),
                 (u'Q17991810', u'corporate title'),
                 (u'Q1190554', u'event'),  # Why does the event category appears again and again
                 (u'Q362482', u'operation'),
                 (u'Q216048', u'team sport'),
                 (u'Q36649', u'visual arts'),
                 (u'Q739302', u'production'),
                 (u'Q451967', u'action'),
                 (u'Q1331793', u'media company'),
                 (u'Q703534', u'employee'),
                 (u'Q467', u'woman')
                 ]


def cat_to_id_dict(ids_dict):
    cat_dict = dict()
    for id in ids_dict.keys():
        if 'title' in ids_dict[id].keys():
            cat = ids_dict[id]['title']
            cat_dict[cat] = (id, cat)

    return cat_dict


if __name__ == "__main__":
    ids_dict = json.load(open("./occ_ids.json"))
    occ = pd.read_csv('./occupation-index.csv')

    cat_dict = cat_to_id_dict(ids_dict)


    # generate graph and filter nodes
    DG = get_graph(ids_dict)
    DG.remove_nodes_from(useless_nodes)

    # for more insight into data
    top_nodes = ancestor_sort(DG)
    null_nodes = [node for node in DG.nodes() if node[1] == 'null']

    # generate categories
    categories = get_categories_dict(DG, leaf_nodes(DG))
    id_categories_dict = get_id_categories_dict(categories)

    classified_nodes = set.union(*[set(val) for val in categories.values()])

    # classify data
    occ.loc[:, 'occupation'] = list(map(lambda qid: ids_dict[qid].get('title'),
                                        occ.qid))
    category = list(map(lambda qid: get_category(qid, id_categories_dict),
                        occ.qid))
    occ.loc[:, 'category'] = category
    unclassified = occ[occ.category == 'unclassified']

    occ['total'] = occ[occ.columns[2:]].sum(axis=1)
    category_wise_data = occ.groupby('category').aggregate(sum)
    category_wise_data.loc[:, 'male/female ratio'] = category_wise_data.male/category_wise_data.female
    category_wise_data.loc[:, 'female/male ratio'] = 1/category_wise_data['male/female ratio']

    fm = category_wise_data[category_wise_data['female/male ratio'] < np.inf]
    fm = fm[fm['total'] > 10]  # Removed categories with very low number of people
    fm.sort_values(by='total', ascending=False)
    fm = fm.iloc[:, [12, 13, 15, 17]]
    fm.to_csv('../data/fm_occupation.csv')

    # Wikidata is messed up, there are categories like "Archimedes"
    # Then is also a Female prince :/
