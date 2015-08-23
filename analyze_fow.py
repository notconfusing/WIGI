from __future__ import print_function
import networkx as nx
import pandas as pd


def get_graph(ids_dict):
    """
    Get the neworkx digraph from the ids_json where two id A is connected to B
    if A is a subclass of B
    """
    def node(_id):
        if "title" in ids_dict[_id].keys():
            return (_id, ids_dict[_id]["title"])
        else:
            return (_id, "null")

    DG = nx.DiGraph()

    for _id in ids_dict.keys():
        id_node = node(_id)
        DG.add_node(id_node)
        DG.add_edges_from([(id_node, node(subclass_id)) for subclass_id in ids_dict[_id]['subclass']])

    return DG


def ancestor_sort(DG):
    nodes = [(len(nx.ancestors(DG, n)), n) for n in DG.nodes()]
    nodes.sort(reverse=True)
    # nodes.sort(key=lambda n: len(nx.ancestors(DG, n)))
    return nodes

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


def get_categories_dict(DG):
    def subclasses_of(*nodes):
        ancestors = set.union(*list(map(lambda node: nx.ancestors(DG, node), [node for node in nodes])))
        ancestors = ancestors.union(set(nodes))
        return ancestors

    categories = dict()
    # XXX: these categories don't have the category labels themselve add it.
    # XXX: The category labels are potentially overlapping
    art = subclasses_of(('Q735', 'art'),
            ('Q838948', 'work of art'),
            ('Q483501', 'artist'),
            ('Q191163', 'landscape art'),
            ('Q17279581', 'floral painting'),
            ('Q134307', 'portrait'),
            ('Q170571', 'still life'))
    history = subclasses_of(('Q309', 'history'))
    social_sciences = subclasses_of(('Q34749', 'social science'))
    law = subclasses_of(('Q7748', 'law'))
    science = subclasses_of(('Q336', 'science'),
                            ('Q901', 'scientist'),
                            ('Q2996394', 'biological process'),
                            ('Q39286', 'entomology')) - art - history
    mathematics = subclasses_of(('Q395', 'mathematics'),
                                ('Q21198', 'computer science'),  # XXX: This can be little controversial
                                ('Q131476', 'graph theory'),
                                ('Q188444', 'differential geometry'),
                                ('Q12482', 'set theory'),
                                ('Q1166618', 'mathematical logic'),
                                ('Q271977', 'partial differential equation'),
                                ('Q847526','queueing theory'),
                                ('Q467606', 'model theory'),
                                ('Q595364', 'lattice'))
    sports = subclasses_of(('Q349', 'sport'))
    engineering = subclasses_of(('Q11023', 'engineering'))
    software = subclasses_of(('Q7397', 'software'))
    language_study = subclasses_of(('Q771861', 'Eurasiatic languages'))
    # NOTE: maybe we should seperate out islam from religion
    religion = subclasses_of(('Q9174', 'religion'),
                             ('Q12818349', 'Islamic theology'),
                             ('Q484181', 'fiqh'),
                             ('Q2737409', 'Hadith studies'),
                             ('Q335414', 'tafsir'),
                             ('Q34178', 'theology'))
    # Islamic theology has more number of biographies than theology is
    # definitely an anamoly, also Islamic Theology is not a subclass of
    # theology
    illegal_drug_trade = subclasses_of(('Q844924', 'illegal drug trade'))
    politics = subclasses_of(('Q82955', 'politician'))
    literature_and_poetry = subclasses_of(('Q36180', 'writer'),
                                          ('Q482', 'poetry'))
    medicine = subclasses_of(('Q39631', 'physician'))
    journalism = subclasses_of(('Q11030', 'journalism'))
    feminism = subclasses_of(('Q223569', 'women\'s rights'),
                                 ('Q7252', 'feminism'),
                                 ('Q205204', 'women\'s suffrage'))

    # There are disproportionately large number of mathematicians in wikipedia,
    # the number of biographies in journalism is less than number of
    # biographies in queuing theory

    # Add Language Study

    categories["art"] = art
    categories["history"] = history
    categories["social sciences"] = social_sciences
    categories["law "] = law
    categories["science"] = science
    categories["mathematics"] = mathematics
    categories["sports"] = sports
    categories["engineering"] = engineering
    categories["software"] = software
    categories["language study"] = language_study
    categories["religion"] = religion
    categories["illegal drug trade"] = illegal_drug_trade
    categories["politics"] = politics
    categories["literature and poetry"] = literature_and_poetry
    categories["medicine"] = medicine
    categories["journalism"] = journalism
    categories["feminism"] = feminism
    return categories


def get_id_categories_dict(categories):
    id_categories_dict = dict()
    for cat in categories.keys():
        id_categories_dict[cat] = set(_id for (_id, title) in categories[cat])
    return id_categories_dict


def get_category(qid, id_categories_dict):
    for key in id_categories_dict.keys():
        if qid in id_categories_dict[key]:
            return key
    return "unclassified"


# It is kinda strange to see that "art" and "work or art" are different
# subclasses

# We have some interesting thins here: node "mathematical object" is also
# connected to Shia Islam here's the link:
#
# [('Q9585', 'Shia Islam'),
#  ('Q432', 'Islam'),
#  ('Q47280', 'Abrahamic religion'),
#  ('Q19842652', 'monotheistic religion'),
#  ('Q9174', 'religion'),
#  ('Q178706', 'institution'),
#  ('Q43229', 'organization'),
#  ('Q16334295', 'group of humans'),
#  ('Q16334298', 'living thing group'),
#  ('Q17519152', 'group of objects'),
#  ('Q18844919', 'group'),
#  ('Q36161', 'set'),
#  ('Q246672', 'mathematical object')]
# We don't want to to connect I'm removing everying in between religion,
# including set, otherwise "everything" is a set

# This can serve as a very good science label
# nx.ancestors(DG, ('Q336', 'science')) - nx.ancestors(DG, ('Q309', 'history'))
# Also we need to sperate out social science ('Q34749', 'social science')



if __name__ == "__main__":
    import json
    ids_dict = json.load(open("./fow_ids.json"))

    DG = get_graph(ids_dict)

    DG.remove_nodes_from(useless_nodes)
    categories = get_categories_dict(DG)
    id_categories_dict = get_id_categories_dict(categories)
    classified_nodes = set.union(*[set(val) for val in categories.values()])
    # DG.remove_nodes_from(classified_nodes)
    # top_nodes = ancestor_sort(DG)


    fow = pd.read_csv('./flatten_field_of_work-index.csv')
    fow.loc[:, 'field of work'] = list(map(lambda qid: ids_dict[qid].get('title', 'null'), fow.qid))
    category = list(map(lambda qid: get_category(qid, id_categories_dict),
        fow.qid))
    fow.loc[:, 'category'] = category

    unclassified = fow[fow.category == 'unclassified']
