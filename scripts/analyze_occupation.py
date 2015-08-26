#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pandas as pd
from wikidata_graph import *


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
                 ('Q1190554', 'event'),
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
                 ('Q16334295', 'group of humans')]


if __name__ == "__main__":
    ids_dict = json.load(open("./occ_ids.json"))
    occ = pd.read_csv('./occupation-index.csv')

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

    # DG.remove_nodes_from(classified_nodes)

    # classify data
    occ.loc[:, 'occupation'] = list(map(lambda qid: ids_dict[qid].get('title'),
                                        occ.qid))
    category = list(map(lambda qid: get_category(qid, id_categories_dict),
                        occ.qid))
    occ.loc[:, 'category'] = category
    unclassified = occ[occ.category == 'unclassified']

    print(occ.head(10))
    # occ.to_csv('classified_occupation-index.csv')
