"""
Dijkstra Shortest Path Alogithm
===============================

> _This algorithm gives us the shortest path from a `source` node to all the other nodes_

> Discovered By : `Edsger Wybe Dijkstra (1930–2002)`

### Problem Statement :

- I want to reach from `delhi` to `banglore`
- There are multiple fares ( based on flight/bus/car etc )
- There are multiple stops ( like maharashtra, pune, orrisa in between )
- for e.g :
    
    - `.delhi.` = via road => `.lucknow.` = via flight => `.pune.` = via train => `.Banglore.`

    - similarly there cane be multiple permutation and combinations

- so we use Graph Theory ( a branch of mathemetics ) to solve these problems .

### Coverting Problem Statement to Graph :

```txt
               +--------------+               Car              +--------------+ 
               |    Bihar     |o------------------------------*|    Orrisa    |
               +--------------+           ( 7000 Rs )          +--------------+
              *       o                                               *        o      car
   Train     /        |                                               |         \  ( 1000 Rs )
( 2000 Rs ) /         |                                               |          \ 
           o          |                                               |           *
+---------+           |                                               |            +----------+
|  Delhi  |           |    Flight                           Flight    |            | Banglore |
+---------+           | ( 1000 Rs )                       ( 2000 Rs ) |            +----------+
           o          |                                               |          *
            \         |                                               |         /   Flight
   Flight    \        |                                               |        /   ( 5000 Rs ) 
( 4000 Rs )   \       *                                               o       o
               +--------------+              Flight            +--------------+ 
               |    Lucknow   |o------------------------------*|     Pune     |
               +--------------+            ( 3000 Rs )         +--------------+
```



> __Dijkstra Result__ : `Delhi` -> `Banglore` :  9000 Rs

Route : `Delhi` -> `Bihar` -> `Lucknow` -> `Pune` -> `Orrisa`  -> `Banglore` 

_So this is how we solve Real-Life Problems with Dijkstra's Algorithm_

    Dijkstra Alogithm KeyPoints :

    - It follows greedy approach
    - It uses following datastructures
        - priority queue

    - Note
        - we are using weighted adjacency list representation ( for this example )
        - this algo only works for positive weighted graphs
            - for negetive weighted graphs we have `Bellman Ford's Algorithm`


---
"""

# Graph Representation
# --------------------
# > Edge Explaination
#
#     0 --> 1 , weight/cost : 2
#     0 --> 2 , weight/cost : 4
#     1 --> 2 , weight/cost : 1
#     1 --> 3 , weight/cost : 7
#     2 --> 4 , weight/cost : 3
#     3 --> 5 , weight/cost : 1
#     4 --> 5 , weight/cost : 5
#     4 --> 3 , weight/cost : 2

GRAPH_REPRESENTATION = """

                           +---+             7             +---+            
                          *| 1 |o-------------------------*| 3 |o           
                         / +---+                           +---+ \          
                        /    o                               *    \         
                     2 /     |                               |     \  1      
                      /      |                               |      \       
                     /       |                               |       \      
                    o        |                               |        *     
               +---+         |                               |         +---+
 -             | 0 |         | 1                             | 2       | 5 |
               +---+         |                               |         +---+
                    o        |                               |        *     
                     \       |                               |       /      
                      \      |                               |      /       
                     4 \     |                               |     /  5      
                        \    *                               o    /         
                         \ +---+                           +---+ /          
                          *| 2 |o-------------------------*| 4 |o           
                           +---+             3             +---+             
"""

# ## Graph Tracing with Dijkstra
"""

- Lets Trace the paths manually as dijikstra would
    - we need to specify our `source` first
    - dijkstra would find all shortest paths from this `source` to all nodes

> Let's select source node as `0`

##### Path `0` to `0`
* 0 ➤ 0 __:__ ✗

##### Path `0` to `1`
* 0 ➤ 1 __:__ _2_    ✓

##### Path `0` to `2`
*  0 ➤ 2 __:__ _4_ 
*  0 ➤ 1 ➤ 2 __:__ _3_  ✓

##### Path `0` to `3`
*  0 ➤ 2 ➤ 4 ➤ 3 __:__ _9_
*  0 ➤ 1 ➤ 2 ➤ 4 ➤ 3 __:__ _8_
*  0 ➤ 1 ➤ 3 __:__ _9_  ✓

##### Path `0` to `4`
*  0 ➤ 2 ➤ 4 __:__ _7_
*  0 ➤ 1 ➤ 2 ➤ 4 __:__ _6_ ✓

##### Path `0` to `5`
*  0 ➤ 2 ➤ 4 ➤ 5 __:__ _12_
*  0 ➤ 1 ➤ 3 ➤ 5 __:__ _10_ ✓
*  0 ➤ 1 ➤ 2 ➤ 4 ➤ 5 __:__ _11_


"""


# Imports
from typing import *
from queue import PriorityQueue

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

# Graph ( in adjacency list repr )
# 
# - Terminology :
#       - _`Key` is node_
#       - _`Value` is a Set of ( neighbour_node, edge_weight )_
# 
graph: Graph = {    # Weighted Adjacency List
    0: { (1, 2) , (2, 4) },
    1: { (2, 1), (3, 7) },
    2: { (4, 3) },
    3: { (5, 1) },
    4: { (5, 5), (3, 2) },
    5: set()
}


# We have Following 3 Important key Concepts in Implementing this Algo
""" 
#### Edge Relaxation

```txt
Sample :

[C]
 * o
 |  \
 |   \
 |    \
 |     \
 o      *
[A]o---*[B]
```

- suppose we have a source selected as A for dijkstra
- let's suppose we are trying to explore the path to reach from [C] to [B]
- then we'll have to consider two things 
    - if there is an existing path of reaching [B] ( i.e from [A] ), then we'll call the cost of this path as -> `Path-1-Cost`
    - and the cost of path that we are currently exploring via [C], we'll call this cost as - `Path-2-Cost`
        - if Path-2-cost is calculated as follows :
            - existing-path-to-c `+` edge-cost-of-C-to-B
- then , if `Path-2-Cost` < `Path-1-Cost` , only then we'll update the existing-shortest-path-storage with this new `Path-1-Cost` value

NOTE : we keep an `existing-shortest-path-storage` , which keeps the track of current shortest path to reach a node

NOTE : we can keep `existing-shortest-path-storage` as a hashmap or a matrix , whichever suits the implementation .

#### Priority Queue
- a priority queue is a special queue data structure that internally maintains an order of data points in a particular fashion based on a value at all times
- internally a priority queue is a heap data structure . heap datastructure can also have 2 flavours i) min heap ii) max heap
- basically at this point the only thing worth caring is that for Dijkstra Algorith we'll use _Min. Heap Priority Queue_

#### BFS
- we know what BFS is , it's about reaching all nodes in a particular pattern
- we use a Queue datastructure to aechive that particular pattern
"""

# ---

# > __So ,  Djiskstra Algorithm is all about performing `BFS` using `Priority Queue` and applying `Edge Relaxation` on every node received .!!!__


def path(graph: Graph, source: Node) -> List[PathCost]:
    """
    Dijkstra Implementation
    -----------------------
    """
    # Steps
    # -----

    # Prepration

    existing_shortest_path: Dict[Node, PathCost] = { v:float('inf') for v in graph}    # Weight here will signify the shortest distance to this node
    # - visiting queue
    #       - it determines which node to visit next
    to_visit: PriorityQueue = PriorityQueue()
    priority_queue_data: Tuple[PathCost, Node] = (0, source)
    to_visit.put(priority_queue_data)
    existing_shortest_path[source] = 0

    # Starting point

    # - idefinate loop until all nodes are visited
    while not to_visit.empty():
        
        # - `1`.visit a node ( using priority queue )
        priority_queue_data: Tuple[Weight, Node] = to_visit.get()                                                                   # 1
        _, source_node = priority_queue_data
        # - `2`.fetch it's neighbours
        neighbour_info: Set[Tuple[Node, EdgeWeight]] = graph[source_node]                                                           # 2
        for neighbour_node_data in neighbour_info:
            neighbour_node, edge_weight = neighbour_node_data
            # - `3`.iteratively apply Edge Relaxation on all Neighbours
            #       - if edge relaxation applies , then add that neighbour node to Priority Queue
            if existing_shortest_path[neighbour_node] > existing_shortest_path[source_node] + edge_weight:                          # 3
                new_shortest_cost_from_source_node_to_neighbour: PathCost = existing_shortest_path[source_node] + edge_weight
                existing_shortest_path[neighbour_node] = new_shortest_cost_from_source_node_to_neighbour
                to_visit.put((new_shortest_cost_from_source_node_to_neighbour, neighbour_node))                                     # 3.1
            
    # Return results
    return existing_shortest_path

# Testing Entrypoint
# ------------------
if __name__ == '__main__':

    print("\nGraph Representation :", GRAPH_REPRESENTATION)
    source: Node = 0
    shortest_path: List[PathCost] = path(graph, source)

    print(f"\n{'Dijkstra\'s Algo Result':^39}")
    print("+","-"*35, "+")
    print(f"| Source | Target | Shortest Distance |")
    print("+","-"*35, "+")
    for target_node, shortest_path_value in shortest_path.items():
        print(f"| {source:^6} | {target_node:^6} | {shortest_path_value:^17} | ")
    print("+", "-"*35, "+")
    expected_shortest_path = [0, 2, 3, 8, 6, 9]
    
    assert list(shortest_path.values()) == expected_shortest_path, f"{expected_shortest_path=} , but got : {list(shortest_path.values())}"
