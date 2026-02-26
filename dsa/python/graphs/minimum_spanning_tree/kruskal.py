"""
Minimum Spanning Tree 
===================================

- a Minimum Spanning Tree (MST) does not depend on a source node .
- a Shortest Path Tree (SPT) does .
- An MST is a global property of a graph, representing the minimum possible total edge weight to connect all vertices .
- works of negetive weights also , but not for negetive weight cycle .
- While algorithmically you may start building an MST from a specific vertex (e.g., Prim's algorithm), 
the resulting set of edges and the total weight of the MST will be the same regardless of which node is chosen as the starting point .

### Visualize :
- algorithms-visual.com/kruskal/?nodes=20_62_A~113_20_B~95_151_C~200_119_D~159_243_E~281_189_F~372_195_G~379_22_H~466_113_I&edges=0_1_6~1_3_2~0_2_4~2_3_10~3_5_0~2_4_4~4_5_7~4_6_1~5_6_6~6_7_1~6_8_33~7_8_44~1_7_3&directed=0

"""

# ---

# Reresentation of graph ( with cycle ) that we'll use for demonstration
GRAPH_REPRESENTATION = """
                                                            Graph :
                                                                - Un-Directed
                                                                - Connected
                                                                - Weighted

                                                            +---+              3                +---+
                                                          / | 1 | -----------------------------| 6 |            
                                                         /  +---+ \                            +---+\
                                                        /          \                             |   \  44
                                                    6  /            \                            |    \
                                                      /              \ 2                     1   |     \ +---+
                                                     /                \                          |      \| 8 |
                                                    /                  \                         |      /+---+
                                              +---+/                  +---+                      |     /
                                              | 0 |                   | 3 |\                     |    / 33
                                              +---+\                 /+---+ \                    |   /
                                                    \               /      0 \ +---+     6     +---+/
                                                     \             /          \| 5 |-----------| 7 |
                                                    4 \           /  10        +---+           +---+
                                                       \         /               /             /
                                                        \  +---+/               /             /
                                                         \ | 2 |               /             /
                                                           +---+ \            /  7          /  1
                                                                  \          /             /
                                                                   \        /             /
                                                                 4  \      /             /
                                                                     \    /             /
                                                                      \ +---+__________/
                                                                       \| 4 | 
                                                                        +---+ 

                                                                Edge Explaination
graph_data
                                                                        0 <--> 1
                                                                        0 <--> 2
                                                                        1 <--> 3
                                                                        2 <--> 3
                                                                        2 <--> 4                          
"""

# Resultant Minimum Spanning Tree
"""

```txt
                                                            +---+              3               +---+
                                                            | 1 | -----------------------------| 6 |            
                                                            +---+ \                            +---+ 
                                                                   \                             |      
                                                                    \                            |     
                                                                     \ 2                     1   |       +---+
                                                                      \                          |       | 8 |
                                                                       \                         |      /+---+
                                              +---+                   +---+                      |     /
                                              | 0 |                   | 3 |\                     |    / 33
                                              +---+\                  +---+ \                    |   /
                                                    \                      0 \ +---+           +---+/
                                                     \                        \| 5 |           | 7 |
                                                    4 \                        +---+           +---+
                                                       \                                       /
                                                        \  +---+                              /
                                                         \ | 2 |                             /
                                                           +---+ \                          /  1
                                                                  \                        /
                                                                   \                      /
                                                                 4  \                    /
                                                                     \                  /
                                                                      \ +---+__________/
                                                                       \| 4 | 
                                                                        +---+ 

```

> __minimum weight : 48__
"""

from typing import *
from dsa.python.graphs.ds import DisjointSet

# Custom Types

# - a node ( vertex ) type
Node = NewType('Node', int)

# - a weight/cost/priority type
Weight = NewType('Weight', int)

# - a weight/cost of edge type
EdgeWeight = NewType('EdgeWeight', Weight)

# - a cost of path type
PathCost = NewType('PathCost', Weight)

# - a graph type
Graph = NewType('Graph', Dict[Node, Set[Tuple[Node, EdgeWeight]]]) # Weighted Adjacency List

# ##### Graph [_undirected_] ( in adjacency list repr )
#   - undirected graphs contains two edge b/w nodes
#   - each for incoming and outgoing respectively
graph: Graph = {    
    0: { (1, 6), (2, 4)},
    1: { (0, 6), (3, 2), (6, 3),},
    2: { (0, 4), (3, 10), (4, 4),},
    3: { (1, 2), (2, 10), (5, 0),},
    4: { (2, 4), (5, 7), (7, 1),},
    5: { (3, 0), (4, 7), (7, 6),},
    6: { (1, 3), (7, 1), (8, 44),},
    7: { (4, 1), (5, 6), (6, 1), (8, 33),},
    8: { (6, 44), (7, 33),},
}

# ---

def span(graph: Graph):
    """
    Minimum Spanning Tree Implementation via Kruskal
    ------------------------------------------------
    """
    # Initialization
    edge_queue: List[Tuple[Node, Node, EdgeWeight]] = []
    min_spanning_tree: Graph = { k:set() for k in graph }
    sum_min_spanning_cost: PathCost = 0

    # convert to edge list representation
    for vertex, neighbours in graph.items():
        for neighbour in neighbours:
          neighbour_vertex, edge_weight = neighbour
          if (
              (vertex, neighbour_vertex, edge_weight) in edge_queue or
              (neighbour_vertex, vertex, edge_weight) in edge_queue
          ):
              continue # (a, b, W) and (b, a, W) are both same 
          edge_queue.append((vertex, neighbour_vertex, edge_weight))
    # sort edge queue
    edge_queue.sort(key=(lambda item: item[2]))
    # prepare disjoint set datastructure
    ds = DisjointSet(len(graph))
    # Start
    for edge in edge_queue:
        
        u, v, w = edge

        # check if cycle not exists
        if ds.find_ultimate_parent(u) == ds.find_ultimate_parent(v):
            continue
        # do Disjoint Set Union
        #   - required for maintaining disjoint set Datastructure
        ds.union(u, v)

        # create edge
        min_spanning_tree[u].add((v, w))
        min_spanning_tree[v].add((u, w))
        # update minimum cost
        sum_min_spanning_cost += w

    return min_spanning_tree, sum_min_spanning_cost

from pprint import pprint
if __name__ == '__main__':
    min_spanning_tree, sum_min_spanning_cost = span(graph)
    print(sum_min_spanning_cost)
    pprint(min_spanning_tree)