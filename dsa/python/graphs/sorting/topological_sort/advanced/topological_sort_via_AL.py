"""
Topological Sort on adjacency list

python3 -m sorting.topological_sort.advanced.topological_sort_via_AL
"""

from graph_representation import Graph, RepresentationOption, Utilities, Types
from typing import *

def sort(graph: Graph) -> List[Types.Node]:

    # get graph ( adjacancy list map )
    _graph: Dict[Types.Node, List[Types.Node]] = graph.adjacency_list
    
    # + ------------------------ +
    # | Create In-degree mapping |
    # + ------------------------ +
    # # 1. get neighbours of a node
    # # 2. logically each neighbour is having an edge from this node
    # # 3. increment the in-degree count of each neighbour node
    # # - repeat steps 1. to 3. for each node 
    
    # initializing in-degree map
    in_degree_map: dict = { node: int() for node in _graph }
    # populating in-degree map
    for node in _graph:
        node_neighbours: List[Types.Node] = _graph[node] # fetching neighbours
        for __node in node_neighbours:
            in_degree_map[__node] += 1 # increment in-degree in map
        
    # + ------------------- +
    # | zero In-degree List |
    # + ------------------- +

    zero_in_degree_nodes: List[Types.Node] = []
    for node in in_degree_map:
        if in_degree_map[node] == 0:
            zero_in_degree_nodes.append(node)

    # + ---- +
    # | Main |
    # + ---- +
    sorted_order: List[Types.Node] = [] 
    while len(zero_in_degree_nodes) > 0:
        node: Types.Node = zero_in_degree_nodes.pop()
        sorted_order.append(node)
        for node_neighbour in _graph[node]:
            in_degree_map[node_neighbour] -= 1
            if in_degree_map[node_neighbour] == 0:
                zero_in_degree_nodes.append(node_neighbour)
    
    if len(sorted_order) == len(_graph):
        return sorted_order
    else:
        raise Exception('Cycle Exists!! in the graph.')

if __name__ == '__main__':

    graph: Graph = Graph()
    meta: dict = graph.meta
    meta['diagram'] = """

    Graph Representation:

            [2]o-------*[6]o-------------:
           *             *               |
          /              |               *
         /               |              [0]
        /                |               *
       o                 o               |
    [1] o---[3]--------*[5]o-------------:
       o             -*    
        \          -/       
         \       -/         
          \    -/
           *  o
           [4]

    """

    representation = RepresentationOption.ADJACENCY_LIST

    # add nodes
    graph.add_node(0, to_representation=representation)
    graph.add_node(1, to_representation=representation)
    graph.add_node(2, to_representation=representation)
    graph.add_node(3, to_representation=representation)
    graph.add_node(4, to_representation=representation)
    graph.add_node(5, to_representation=representation)
    graph.add_node(6, to_representation=representation)

    #add edges
    graph.add_edge((1,2), to_representation=representation)
    graph.add_edge((1,3), to_representation=representation)
    graph.add_edge((1,4), to_representation=representation)
    graph.add_edge((3,5), to_representation=representation)
    graph.add_edge((4,5), to_representation=representation)
    graph.add_edge((2,6), to_representation=representation)
    graph.add_edge((5,6), to_representation=representation)
    graph.add_edge((6,0), to_representation=representation)
    graph.add_edge((5,0), to_representation=representation)
    
    print("\nRepresentation :\n")
    print(graph.meta['diagram'])

    Utilities.print_adjacency_list(graph)

    sorted_topological_order: List[Types.Node] = sort(graph)
    print(f"\n{sorted_topological_order=}\n")

    # suppose you want to name the nodes
    visualization: dict = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 0: 'G'}
    print('\nsorted_topological_order : ', ' -> '.join([visualization[v] for v in sorted_topological_order]), '\n')