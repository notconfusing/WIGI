from __future__ import print_function
import networkx as nx


# XXX
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

useful_nodes = [
    ('Q336', 'science'),
    ('Q11862829', 'academic discipline'),
    ('Q7748', 'law'),
    ('Q309', 'history'),
    ('Q34749', 'social science'),
    ('Q11190', 'medicine'),
    ('Q11023', 'engineering'),
    ('Q735', 'art'),
    ('Q838948', 'work of art'),
    ('Q80083', 'humanities')
]


def get_categories(DG):
    categories = dict()
    # XXX: these categories don't have the category labels themselve add it.
    art = set.union(nx.ancestors(DG, ('Q735', 'art')),
            nx.ancestors(DG, ('Q838948', 'work of art')))
    history = nx.ancestors(DG, ('Q309', 'history'))
    social_sciences = nx.ancestors(DG, ('Q34749', 'social science'))
    law = nx.ancestors(DG, ('Q7748', 'law'))
    science = nx.ancestors(DG, ('Q336', 'science')) - art - history
    sports = nx.ancestors(DG, ('Q349', 'sport'))

    categories["art"] = art
    categories["history"] = history
    categories["social sciences"] = social_sciences
    categories["law "] = law
    categories["science"] = science
    categories["sports"] = sports
    return categories


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
    categories = get_categories(DG)
    classified_nodes = set.union(*[set(val) for val in categories.values()])
    DG.remove_nodes_from(classified_nodes)
    top_nodes = ancestor_sort(DG)
