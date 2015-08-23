#! /usr/bin/env python

import json
import pandas as pd
from wikidata_graph import *


# These nodes are too vague to have any use in our analysis
useless_nodes = [('Q35120', 'entity'),
    ('Q488383', 'object'),
    ('Q7184903', 'abstract object'),
    ('Q1190554', 'event'),
    ('Q151885', 'concept'),
    ('Q3249551', 'process'),
    ('Q223557', 'physical object'),
    ('Q16686448', 'artificial object'),
    ('Q386724', 'work'),
    ('Q5127848', 'class'),
    ('Q16889133', 'class'),
    ('Q1914636', 'activity'),
    ('Q9081', 'knowledge'),
    ('Q217594', 'class'),
    ('Q17008256', 'collection'),
    ('Q830077', 'subject'),
    ('Q18336849', 'item with given name property'),
    ('Q178706', 'institution'),
    ('Q43229', 'organization'),
    ('Q16334295', 'group of humans'),
    ('Q16334298', 'living thing group'),
    ('Q17519152', 'group of objects'),
    ('Q18844919', 'group'),
    ('Q36161', 'set'),
    ('Q853614', 'identifier'),
    ('Q2500638', 'creator'),
    ('Q28877', 'good'),
    ('Q171283', 'Homo'),
    ('Q5', 'human')]


if __name__ == "__main__":
    ids_dict = json.load(open("./fow_ids.json"))
    fow = pd.read_csv('./flatten_field_of_work-index.csv')

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
    fow.loc[:, 'field of work'] = list(map(lambda qid: ids_dict[qid].get('title'),
                                           fow.qid))
    category = list(map(lambda qid: get_category(qid, id_categories_dict),
                        fow.qid))
    fow.loc[:, 'category'] = category

    # DG.remove_nodes_from(classified_nodes)
    unclassified = fow[fow.category == 'unclassified']

    print(fow.head(10))
    # fow.to_csv('classified_occupation-index.csv')
