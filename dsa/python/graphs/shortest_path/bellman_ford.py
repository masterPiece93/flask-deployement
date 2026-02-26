"""
Bellman-ford Shortest Path Alogithm
===================================

> _This algorithm gives us the shortest path from a `source` node to all the other nodes_

> Discovered By : `Richard Bellman and Lester Ford Jr. (1955–1958)`

- We should actually call it : `Bellman–Ford–Moore algorithm`

### Problem Statement :

- I want clear a rally rage from `Gate1` till `Gate6`
- There are multiple points on crossing each gate ( either +ve / -ve )
- I want to reach with maximum points
- for e.g :
    
    - `.1.` = _+2_ => `.2.` = _-6_ => `.4.` = _+2_ => `.5.` = _-2_ => `.6.`

    - similarly there cane be multiple permutation and combinations

- so we use Graph Theory ( a branch of mathemetics ) to solve these problems .

### Coverting Problem Statement to Graph :

```txt
               +--------------+               Points           +--------------+ 
               |    Gate2     |o------------------------------*|     Gate4    |
               +--------------+               ( - 6 )          +--------------+
              *       o                                               *        o      Points
   Points    /        |                                               |         \     ( + 1 )
  ( + 2  )  /         |                                               |          \ 
           o          |                                               |           *
+---------+           |                                               |            +----------+
|  Gate1  |           |    Points                           Points    |            |  Gate6   |
+---------+           |   ( - 3  )                         ( + 2  )   |            +----------+
           o          |                                               |          *
            \         |                                               |         /   Points
   Points    \        |                                               |        /   ( - 2  ) 
  (  -1  )    \       *                                               o       o
               +--------------+              Points            +--------------+ 
               |     Gate3    |o------------------------------*|     Gate5    |
               +--------------+             ( + 5  )           +--------------+
```

-2

> __Bellman-Ford-Moore Result__ : `Delhi` -> `Banglore` :  9000 Rs

Route : `Delhi` -> `Bihar` -> `Lucknow` -> `Pune` -> `Orrisa`  -> `Banglore` 

_So this is how we solve Real-Life Problems with Bellman-Ford-Moore Algorithm_

    Bellman-Ford-Moore Alogithm KeyPoints :

    - It follows DP approach
    - It uses following datastructures
        - priority queue

    - Note
        - we are using weighted adjacency list representation ( for this example )
        - this algo only works for positive weighted graphs
            - for negetive weighted graphs we have `Bellman Ford's Algorithm`


---

"""

# ## Reresentation of graph that we'll use for demonstration
"""

- Lets Trace the paths manually as dijikstra would
    - we need to specify our `source` first
    - bellman-ford would find all shortest paths from this `source` to all nodes

> Let's select source node as `0`

Since there are 6 Nodes , there will be 6-1=5 Iterations

##### Iteration 1
* 0 ➤ 1 __:__ [0, 2, ∞, ∞, ∞, ∞ ]
* 0 ➤ 2 __:__ [0, 2, -1, ∞, ∞, ∞ ]
* 1 ➤ 3 __:__ [0, 2, -1, ∞, ∞, ∞ ]
* 1 ➤ 2 __:__ [0, 2, -1, -4, ∞, ∞ ]
* 2 ➤ 4 __:__ [0, 2, -1, -4, 4, ∞ ]
* 3 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]


##### Iteration 2
* 0 ➤ 1 __:__ [0, 2, -1, -4, 4, -3 ]
* 0 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 2 ➤ 4 __:__ [0, 2, -1, -4, 4, -3 ]
* 3 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]

##### Iteration 3
* 0 ➤ 1 __:__ [0, 2, -1, -4, 4, -3 ]
* 0 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 2 ➤ 4 __:__ [0, 2, -1, -4, 4, -3 ]
* 3 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]

##### Iteration 4
* 0 ➤ 1 __:__ [0, 2, -1, -4, 4, -3 ]
* 0 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 2 ➤ 4 __:__ [0, 2, -1, -4, 4, -3 ]
* 3 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]

#####  Iteration 5
* 0 ➤ 1 __:__ [0, 2, -1, -4, 4, -3 ]
* 0 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 1 ➤ 2 __:__ [0, 2, -1, -4, 4, -3 ]
* 2 ➤ 4 __:__ [0, 2, -1, -4, 4, -3 ]
* 3 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 3 __:__ [0, 2, -1, -4, 4, -3 ]
* 4 ➤ 5 __:__ [0, 2, -1, -4, 4, -3 ]

- You must be noticing that after Interation-1 , all the other iterations from Iteration-2 to Iteration-5
are generating same results every time .

- This does not happen always , when the graph have more complications and more edges , the changes seem to appear till last Iteration .

"""
GRAPH_REPRESENTATION = """

                           +---+             -6            +---+            
                          *| 1 |o-------------------------*| 3 |o           
                         / +---+                           +---+ \          
                        /    o                               *    \         
                     2 /     |                               |     \  +1      
                      /      |                               |      \       
                     /       |                               |       \      
                    o        |                               |        *     
               +---+         |                               |         +---+
 -             | 0 |         | -3                            | 2       | 5 |
               +---+         |                               |         +---+
                    o        |                               |        *     
                     \       |                               |       /      
                      \      |                               |      /       
                    -1 \     |                               |     /  +2      
                        \    *                               o    /         
                         \ +---+                           +---+ /          
                          *| 2 |o-------------------------*| 4 |o           
                           +---+             +5            +---+             
            
            Edge Explaination

                0 --> 1 , weight/cost : +2
                0 --> 2 , weight/cost : -1
                1 --> 2 , weight/cost : -3
                1 --> 3 , weight/cost : -6
                2 --> 4 , weight/cost : +5
                3 --> 5 , weight/cost : +1
                4 --> 5 , weight/cost : +2
                4 --> 3 , weight/cost : +2

""" 

# ---

# Imports

from typing import *

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
    0: { (1, 2) , (2, -1) },
    1: { (2, -3), (3, -6) },
    2: { (4, 5) },
    3: { (5, 1) },
    4: { (5, 5), (3, 2) },
    5: set()
}

# We have Following Important key Concepts in Implementing this Algo 
# #### Edge Relaxation
"""
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
"""

# ---

# > __So ,  Bellman-Form-Moore Algorithm is all about applying `Edge Relaxation` on every edge repeatedly for N-1 times .!!!__

# ---

def path(graph: Graph, source: Node) -> List[PathCost]:
    """
    Bellman-Ford-Moore Implementation
    ---------------------------------
    """
    # Steps
    # -----

    # Prepration

    total_vertices: int = 6
    distance: Dict[Node, PathCost] = { v:float('inf') for v in graph}    # Weight here will signify the shortest distance to this node
    distance[source] = 0

    # Starting point

    # - idefinate loop until all nodes are visited

    counter = 1
    while counter <= total_vertices - 1:
        print(f'Iteration {counter}:')
        for node in graph:
            u: Node = node
            neighbour_info: Set[Tuple[Node, EdgeWeight]] = graph[u]
            for info in neighbour_info:
                v: Node = info[0]
                edge_weight: EdgeWeight = info[1]
                
                if distance[v] > distance[u] + edge_weight:
                    new_cost: PathCost = distance[u] + edge_weight
                    distance[v] = new_cost
                print(f"\t{[v for _, v in distance.items()]}")
        counter += 1
    # return results
    return distance

# Testing Entrypoint
# ------------------
if __name__ == '__main__':

    print("\nGraph Representation :", GRAPH_REPRESENTATION)
    source: Node = 0
    shortest_path: List[PathCost] = path(graph, source)

    print(f"\n{'Bellman Ford Algo Result':^39}")
    print("+","-"*35, "+")
    print(f"| Source | Target | Shortest Distance |")
    print("+","-"*35, "+")
    for target_node, shortest_path_value in shortest_path.items():
        print(f"| {source:^6} | {target_node:^6} | {shortest_path_value:^17} | ")
    print("+", "-"*35, "+")
    expected_shortest_path = [0, 2, -1, -4, 4, -3]
    
    assert list(shortest_path.values()) == expected_shortest_path, f"{expected_shortest_path=} , but got : {list(shortest_path.values())}"
