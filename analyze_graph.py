from __future__ import print_function
import networkx as nx


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
        DG.add_edges_from([(id_node, node(subclass_id)) for subclass_id in
            ids_dict[_id]['subclass']])

    return DG

def top_nodes(DG):


if __name__ == "__main__":
    import json
    ids_dict = json.load(open("./fow_ids.json"))

    DG = get_graph(ids_dict)

    # Trying to analyze connected components
    G = DG.to_directed()
    X = list(nx.connected_component_subgraphs(G))
    X.sort(key=lambda g: len(g.nodes()), reverse=True)
    graphs_len = [len(g.nodes()) for g in X]
    # X = [i for (y,i) in sorted(zip(graphs_len, X), key=lambda)]

    no_successors = set([node for node in DG.nodes_iter() if len(DG.successors(node)) == 0])
    no_predecessors = set([node for node in DG.nodes_iter() if len(DG.predecessors(node)) == 0])
    lone_wolves = no_successors.intersection(no_predecessors)
