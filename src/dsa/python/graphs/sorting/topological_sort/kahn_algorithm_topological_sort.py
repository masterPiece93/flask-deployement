"""
Topological Sort
    - using Kahn's Algorithm

`one day, a guy named Kahn wanted to sort some tasks in logical order using graph , 
he came up with a concept of In-Degree, that suited the writing of efficient 
computer program , and was successful in making a set of steps (an algorithm) .

Hence , we named - Kahn's Algorithm .
`

NOTE
    - we have represented nodes as integers
    - we have used adjacency list representation for representing a graph

Study Link

    - https://www.interviewcake.com/concept/python3/topological-sort
"""
import copy
from typing import NewType, Dict, Set, List

Node = NewType('Node', int)
Graph = NewType('Graph', Dict[Node, Set]) # Adjacency List

GRAPH_REPRESENTATION = """

                            +---+             
                          -*| 1 |             
                         /  +---+o            
                        /    o    \           
                       /     |     \          
                      /      |      \         
                     /       |       \        
                    /        |        \       
              +---+o         |         *      
   -          | 0 |          |          +---+
              +---+o         |       /-*| 3 |
                    \        |      /   +---+
                     \       |     /      o  
                      \      |    /       |  
                       \     *   /        |  
                        \  +---+o         |  
                         -*| 2 |o         |  
                           +---+ \        |  
                                  \       |  
                                   \      |  
                                    \     |  
                                     \    *  
                                      \ +---+ 
                                       *| 4 | 
                                        +---+ 

            Edge Explaination

                    0 --> 1
                    0 --> 2
                    1 --> 2
                    1 --> 3
                    2 --> 4
                    3 --> 2
                    3 --> 4                            
"""

# Graph ( in adjacency list repr )
graph: Graph = {
    0: { 1, 2 },
    1: { 2, 3 },
    2: { 4 },
    3: { 2, 4 },
    4: set()
}


def get_in_degree_map(graph: Graph) -> Dict[Node, int]:
    """Specifies in-degree for each node of graph"""
    in_degree_map: Dict[Node, int] = { node: 0 for node in graph}
    for node in graph:
        directed_neighbours: Set = graph[node]
        for neighbour_node in directed_neighbours:
            in_degree_map[neighbour_node] += 1
    return in_degree_map

def get_nodes_with_in_degree_zero(graph: Graph, in_degree_map: Dict[Node, int]) -> List[Node]:
    """..."""
    nodes: List[Node] = []
    for node in graph:
        in_degree: int = in_degree_map[node]
        if in_degree == 0:
            nodes.append(node)
    return nodes

# --------------
# Run Algorithm
# --------------

def topological_sort(graph: Graph):

    in_degree_map: Dict[Node, int] = get_in_degree_map(graph)
    nodes_with_no_incomming_edge: List[Node] = get_nodes_with_in_degree_zero(graph, in_degree_map)
    graph_copy: Graph = copy.deepcopy(graph)
    topological_sorted_order = []

    # loop unitil no node with zero incoming edge is left
    while len(nodes_with_no_incomming_edge) > 0:

        in_degree_zero_node = nodes_with_no_incomming_edge.pop()
        topological_sorted_order.append(in_degree_zero_node)
        del graph_copy[in_degree_zero_node] # redundant
        nodes_with_no_incomming_edge: List[Node] = get_nodes_with_in_degree_zero(graph_copy, get_in_degree_map(graph_copy))     # redundant

    if len(topological_sorted_order) == len(graph):
        return topological_sorted_order
    else:
        raise Exception('Graph has a cycle! No topological ordering exists.')

def topological_sort_v2(graph: Graph):
    """
    - removed redundant steps
    """
    in_degree_map: Dict[Node, int] = get_in_degree_map(graph)
    nodes_with_no_incomming_edge: List[Node] = get_nodes_with_in_degree_zero(graph, in_degree_map)
    topological_sorted_order = []

    # loop unitil no node with zero incoming edge is left
    while len(nodes_with_no_incomming_edge) > 0:

        in_degree_zero_node = nodes_with_no_incomming_edge.pop()
        topological_sorted_order.append(in_degree_zero_node)

        for node in graph[in_degree_zero_node]:

            in_degree_map[node] -= 1
            if in_degree_map[node] == 0:
                nodes_with_no_incomming_edge.append(node)
            
    if len(topological_sorted_order) == len(graph):
        return topological_sorted_order
    else:
        raise Exception('Graph has a cycle! No topological ordering exists.')

if __name__ == '__main__':

    print("topological_sort ( basic ) : ", topological_sort(graph))
    print("topological_sort ( v2    ) : ", topological_sort_v2(graph))