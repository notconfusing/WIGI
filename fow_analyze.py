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


def ancestor_sort(DG):
    nodes = [(len(nx.ancestors(DG, n)), n) for n in DG.nodes()]
    nodes.sort(reverse=True)
    # nodes.sort(key=lambda n: len(nx.ancestors(DG, n)))
    return nodes


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


if __name__ == "__main__":
    import json
    ids_dict = json.load(open("./fow_ids.json"))

    DG = get_graph(ids_dict)
    DG.remove_nodes_from(useless_nodes)

    categories = get_categories_dict(DG, leaf_nodes(DG))
    id_categories_dict = get_id_categories_dict(categories)

    classified_nodes = set.union(*[set(val) for val in categories.values()])

    # DG.remove_nodes_from(classified_nodes)
    # top_nodes = ancestor_sort(DG)

    fow = pd.read_csv('./flatten_field_of_work-index.csv')
    fow.loc[:, 'field of work'] = list(map(lambda qid: ids_dict[qid].get('title', 'null'), fow.qid))
    category = list(map(lambda qid: get_category(qid, id_categories_dict), fow.qid))
    fow.loc[:, 'category'] = category

    unclassified = fow[fow.category == 'unclassified']
