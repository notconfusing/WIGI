#! /usr/bin/env python

from __future__ import print_function
import networkx as nx


def get_graph(ids_dict):
    """ Generate the neworkx digraph from the ids JSON file.

    A node with id A is connected to B iff A is a subclass of B.
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
    """ Sort nodes based on the number of ancestors they have.

    Returns a list of tuples having number of ancestors as the first element
    and node as the second element, sorted in decreasing order of number of
    ancestors.
    """
    nodes = [(len(nx.ancestors(DG, n)), n) for n in DG.nodes()]
    nodes.sort(reverse=True)
    return nodes


def leaf_nodes(DG):
    """ Return all nodes who have no successor.

    These nodes will act as our 'top level categories'. Invariably, it will
    also include nodes which are single and are not connected to any other node
    in the graph.

    Note that having no successor or predecessor doesn't imply that the node
    will have no data associated with it.
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

    nodes = [[len(DG.successors(node)), len(DG.predecessors(node)), node]
             for node in DG.nodes()]

    # Sort with increasing number of succesor nodes and decreasing number of
    # predecessors. This is not necessary but helps in quickly visualizing
    # important nodes.
    nodes.sort(sort, reverse=True)
    return [node[2] for node in nodes if node[0] == 0]


def get_categories_dict(DG, category_nodes):
    """ Return a dictionary of nodes belonging to different categories.

    The categories are generated from the list of nodes accepted as an
    argument. All the ancestors of each node (obtained from graph) in this
    list are caterogized under the title of that node as label.
    """
    def subclasses_of(*nodes):
        ancestors = set.union(*list(map(lambda node: nx.ancestors(DG, node),
                                        [node for node in nodes])))
        ancestors = ancestors.union(set(nodes))
        return ancestors

    categories = dict()

    for node in category_nodes:
        categories[node[1]] = subclasses_of(node)

    return categories


def get_id_categories_dict(categories):
    """ Return a set of Wikidata QIDs for node in a category dictionary."""
    id_categories_dict = dict()
    for cat in categories.keys():
        id_categories_dict[cat] = set(_id for (_id, title) in categories[cat])
    return id_categories_dict


def get_category(qid, id_categories_dict):
    """ Return the cateogory to which a particular Wikidata QID belongs.

    In case no category is found, 'unclassified' is returned.
    """
    for key in id_categories_dict.keys():
        if qid in id_categories_dict[key]:
            return key
    return "unclassified"


if __name__ == "__main__":
    pass
