"""
Minimum Spanning Tree 
===================================

- a Minimum Spanning Tree (MST) does not depend on a source node .
- a Shortest Path Tree (SPT) does .
- An MST is a global property of a graph, representing the minimum possible total edge weight to connect all vertices .
- works of negetive weights also , but not for negetive weight cycle .
- While algorithmically you may start building an MST from a specific vertex (e.g., Prim's algorithm), 
the resulting set of edges and the total weight of the MST will be the same regardless of which node is chosen as the starting point .

### Problem Statement
- given a `connected` `un-directed` graph
- with the edges having `weights`
- we need to adjust the graph in such a way that 
    - by keep all the nodes connected in a minimal possible way such that each node is at most reachable from somewhere
    - and the sum of weight of all the edges shall be minimum

> there can be many spanning trees of a graph , but only one MST

### Visualize :
- [visualize at algorithms-visual.com](https://algorithms-visual.com/prim/?nodes=20_62_A~113_20_B~95_151_C~200_119_D~159_243_E~281_189_F~372_195_G~379_22_H~466_113_I&edges=0_1_6~1_3_2~0_2_4~2_3_10~3_5_0~2_4_4~4_5_7~4_6_1~5_6_6~6_7_1~6_8_33~7_8_44~1_7_3&directed=0)

### KeyPoints :
- this algorithm works on the connected graph

"""

# ---

# Reresentation of graph ( with cycle ) that we'll use for demonstration
GRAPH_REPRESENTATION = """
                                                            Graph :
                                                                - Un-Directed
                                                                - Connected
                                                                - Weighted

                                                            +---+              3               +---+
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

                                                                        0 <--> 1 : 6
                                                                        0 <--> 2 : 4
                                                                        1 <--> 3 : 2
                                                                        1 <--> 6 : 3
                                                                        2 <--> 3 : 10
                                                                        2 <--> 4 : 4
                                                                        3 <--> 5 : 0
                                                                        4 <--> 5 : 7
                                                                        4 <--> 7 : 1
                                                                        5 <--> 7 : 6
                                                                        6 <--> 7 : 1
                                                                        6 <--> 8 : 44
                                                                        7 <--> 8 : 33
                                                                        
                                                                        

                                                                Resultant Minimum Spanning Tree


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

                                                                    * Minimum Weight : 48 *
"""

# ---

# Imports
from typing import *
from dataclasses import dataclass
from src.dsa.python.graphs.ds import PriorityQueue
import uuid

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

def span(graph: Graph, source: Node):
    """
    Minimum Spanning Tree Implementation via Prims
    ----------------------------------------------
    """
    # Initialization
    to_visit: PriorityQueue = PriorityQueue() # it'll contain all nodes explored
    min_spanning_tree: Graph = {}
    sum_min_spanning_cost: PathCost = 0

    # Seed
    @dataclass
    class Data:
        vertex: Node
        parent: Optional[Node] = None
    priority_queue_task: Tuple[PathCost, Node] = PriorityQueue.Task(task_id=uuid.uuid4().hex, priority=0, data=Data(vertex=source, parent=None)) # path cost to reach the source is 0
    to_visit.put(priority_queue_task)

    # Start
    while not to_visit.empty():
        # - `1`.visit a node ( using priority queue )
        priority_queue_task: PriorityQueue.Task = to_visit.get()
        current_node = priority_queue_task.data.vertex
        parent_of_current_node = priority_queue_task.data.parent
        cost: PathCost = priority_queue_task.priority 
        sum_min_spanning_cost += cost

        # - `2`.Add to spanning tree
        min_spanning_tree[current_node] = set()
        if parent_of_current_node is not None:
            min_spanning_tree[parent_of_current_node].add((current_node, cost))
            min_spanning_tree[current_node].add((parent_of_current_node, cost))
        
        # - `3`.Fetch it's neighbours
        neighbour_info: Set[Tuple[Node, EdgeWeight]] = graph[current_node]
        
        # - `4`.Find minimum for neighbours
        for neighbour_node_data in neighbour_info:
            neighbour_node, edge_weight = neighbour_node_data
            if neighbour_node == current_node or neighbour_node in min_spanning_tree:
                continue
            task: Optional[PriorityQueue.Task] = to_visit.fetch_task(by=lambda task: task.data.vertex == neighbour_node)
            if task:
                #   - if exists in priority queue & current edge is smaller , then update the queue
                if edge_weight < task.priority:
                    to_visit.task_priority_update(task, edge_weight) # signifies that , a shorter edge exists to reach this neighbour with cost == `edge_weight`  
                    task.data.parent = current_node
            else: # - if not exists in priority queue , then add
                to_visit.put(PriorityQueue.Task(task_id=uuid.uuid4().hex, priority=edge_weight, data=Data(vertex=neighbour_node, parent=current_node))) # signifies that , we have found an `edge_weight` cost to reach this neighbour 

    return min_spanning_tree, sum_min_spanning_cost


def span_with_printable_steps(graph: Graph, source: Node):
    """
    Identical to `def span(graph: Graph, source: Node):...` , but also prints
    each step ( in alogrithm ) on console .
    """
    # Initialization
    to_visit: PriorityQueue = PriorityQueue() # it'll contain all nodes explored
    min_spanning_tree: Graph = {}
    sum_min_spanning_cost: PathCost = 0

    # Seed
    @dataclass
    class Data:
        vertex: Node
        parent: Optional[Node] = None
    priority_queue_task: Tuple[PathCost, Node] = PriorityQueue.Task(task_id=uuid.uuid4().hex, priority=0, data=Data(vertex=source, parent=None)) # path cost to reach the source is 0
    to_visit.put(priority_queue_task)

    # Start
    while not to_visit.empty():
        print(f"- Visiting Queue : {[f"[ {v.data.vertex} ({v.priority})<{v.data.parent}>]" for v in to_visit]}")
        # - `1`.visit a node ( using priority queue )
        priority_queue_task: PriorityQueue.Task = to_visit.get()
        current_node = priority_queue_task.data.vertex
        parent_of_current_node = priority_queue_task.data.parent
        cost: PathCost = priority_queue_task.priority 
        sum_min_spanning_cost += cost
        print(f"\tCurrent Node : {current_node}")
        print(f"\tParent of Current Node : {parent_of_current_node}")
        print(f"\tCost : {cost}")
        # - `2`.Add to spanning tree
        min_spanning_tree[current_node] = set()
        if parent_of_current_node is not None:
            min_spanning_tree[parent_of_current_node].add((current_node, cost))
            min_spanning_tree[current_node].add((parent_of_current_node, cost))
        
        # - `3`.Fetch it's neighbours
        neighbour_info: Set[Tuple[Node, EdgeWeight]] = graph[current_node]
        
        # - `4`.Find minimum for neighbours
        for neighbour_node_data in neighbour_info:
            neighbour_node, edge_weight = neighbour_node_data
            if neighbour_node == current_node or neighbour_node in min_spanning_tree:
                continue

            # - `5`.Check if exists in priority queue 
            task: Optional[PriorityQueue.Task] = to_visit.fetch_task(by=lambda task: task.data.vertex == neighbour_node)
            
            if task:
                print(f"\t\t\t- existing cost : {task.priority} from vertex : {task.data.parent}")
                print(f"\t\t\t- current cost  : {edge_weight} from vertex : {current_node}")
                if edge_weight < task.priority:
                    to_visit.task_priority_update(task, edge_weight) # signifies that , a shorter edge exists to reach this neighbour with cost == `edge_weight`  
                    task.data.parent = current_node
                    print(f"\t\t\t- updated to current cost")
                else:
                    print(f"\t\t\t- left at existing cost")
            else:
                print(f"\t\t\t- added to priority queue : [ {neighbour_node} ({edge_weight})<{current_node}>]")
                to_visit.put(PriorityQueue.Task(task_id=uuid.uuid4().hex, priority=edge_weight, data=Data(vertex=neighbour_node, parent=current_node))) # signifies that , we have found an `edge_weight` cost to reach this neighbour 
        print(f"- Visiting Queue : {[f"[ {v.data.vertex} ({v.priority})<{v.data.parent}>]" for v in to_visit]}")
        print('\n','-'*10,'\n')
    return min_spanning_tree, sum_min_spanning_cost


from pprint import pprint
if __name__ == '__main__':

    min_spanning_tree, sum_min_spanning_cost = span(graph, source=0)
    print()
    pprint(min_spanning_tree, indent=4)
    print(f"{sum_min_spanning_cost=}")