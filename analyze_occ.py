from __future__ import print_function
import networkx as nx
import pandas as pd


# these nodes are too vague to have any use in our analysis
useless_nodes = [(u'Q35120', u'entity'),
                 (u'Q488383', u'object'),
                 (u'Q223557', u'physical object'),
                 (u'Q830077', u'subject'),
                 (u'Q18336849', u'item with given name property'),
                 (u'Q215627', u'person'),
                 (u'Q16686022', u'natural physical object'),
                 (u'Q7239', u'organism'),
                 (u'Q2944660', u'lexical item'),
                 (u'Q8171', u'word'),
                 (u'Q82799', u'name'),
                 (u'Q2382443', u'Biota'),
                 (u'Q19088', u'eukaryote'),
                 (u'Q964455', u'unikont'),
                 (u'Q129021', u'opisthokont'),
                 (u'Q729', u'animal'),
                 (u'Q171283', u'Homo'),
                 (u'Q164509', u'omnivore'),
                 (u'Q5', u'human'),
                 (u'Q7184903', u'abstract object'),
                 (u'Q1190554', u'event'),
                 (u'Q3249551', u'process'),
                 (u'Q5127848', u'class'),
                 (u'Q16889133', u'class'),
                 (u'Q151885', u'concept'),
                 (u'Q16686448', u'artificial object'),
                 (u'Q1914636', u'activity'),
                 (u'Q246672', u'mathematical object'),
                 (u'Q217594', u'class'),
                 (u'Q17008256', u'collection'),
                 (u'Q36161', u'set'),
                 (u'Q6671777', u'structure'),
                 (u'Q4164871', u'position'),
                 (u'Q390066', u'object composition'),
                 (u'Q18844919', u'group'),
                 (u'Q17519152', u'group of objects'),
                 (u'Q16334298', u'living thing group'),
                 (u'Q386724', u'work'),
                 (u'Q15222213', u'artificial physical object'),
                 (u'Q336', u'science'),
                 (u'Q853614', u'identifier'),
                 (u'Q216353', u'title'),
                 (u'Q28877', u'good'),
                 (u'Q2424752', u'product'),
                 (u'Q16334295', u'group of humans')]


def get_graph(ids_dict):
    """
    Get the neworkx digraph from the ids_json where two id A is connected to B
    if A is a subclass of B
    """
    def node(_id):
        if "title" in ids_dict[_id].keys():
            return (_id, ids_dict[_id]['title'])
        else:
            return (_id, 'null')

    DG = nx.DiGraph()

    for _id in ids_dict.keys():
        id_node = node(_id)
        DG.add_node(id_node)
        # deleted pages exist as singular node with title 'null'
        if ids_dict[_id]:
            DG.add_edges_from([(id_node, node(subclass_id))
                            for subclass_id in ids_dict[_id]['subclass']])

    return DG


def ancestor_sort(DG):
    nodes = [(len(nx.ancestors(DG, n)), n) for n in DG.nodes()]
    nodes.sort(reverse=True)
    return nodes


def leaf_nodes(DG):
    """ Returns all nodes who have no successor.

    These nodes will act as our 'top level categories'. Invariably, it will
    also include nodes which are single and are not connected to any other node
    in the graph.
    """

    def sort(x, y):
        if x[0] == y[0]:
            if x[1] >= y[1]:
                return 1
            else:
                return -1
        elif x[0] > y[0]:
            return -1
        else:
            return 1

    nodes = [[len(DG.successors(node)), len(DG.predecessors(node)), node] for node in DG.nodes()]

    # Sort with increasing number of succesor nodes and decreasing number of
    # predecessors. This is not necessary but helps in quickly visualizing
    # important nodes.
    nodes.sort(sort, reverse=True)
    return [node[2] for node in nodes if node[0] == 0]


def get_categories_dict(DG, category_nodes):
    def subclasses_of(*nodes):
        ancestors = set.union(*list(map(lambda node: nx.ancestors(DG, node), [node for node in nodes])))
        ancestors = ancestors.union(set(nodes))
        return ancestors

    categories = dict()

    for node in category_nodes:
        categories[node[1]] = subclasses_of(node)

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


if __name__ == "__main__":
    import json
    ids_dict = json.load(open("./occ_ids.json"))

    DG = get_graph(ids_dict)
    null_nodes = [node for node in DG.nodes() if node[1] == 'null']

    DG.remove_nodes_from(useless_nodes)

    top_nodes = ancestor_sort(DG)
    categories = get_categories_dict(DG, leaf_nodes(DG))
    id_categories_dict = get_id_categories_dict(categories)
    classified_nodes = set.union(*[set(val) for val in categories.values()])

    #DG.remove_nodes_from(classified_nodes)

    occ = pd.read_csv('./flatten_occupation-index.csv')
    occ.loc[:, 'occupation'] = list(map(lambda qid: ids_dict[qid].get('title'),
                                    occ.qid))

    category = list(map(lambda qid: get_category(qid, id_categories_dict),
        occ.qid))
    occ.loc[:, 'category'] = category
    unclassified = occ[occ.category == 'unclassified']
