"""
Cycle Detection ( using DFS )
=============================

"""
from typing import *

# Custom Types

# - a node ( vertex ) type
Node = NewType('Node', int)
# - a graph type
Graph = NewType('Graph', Dict[Node, Set]) # Adjacency List

# ---

# Reresentation of graph ( with cycle ) that we'll use for demonstration
"""
> Tracing the graph with Algorithm

```txt
current_node=0
        neighbour=2
                back_edge_node=0                        | parent store : {0: 0, 2: 0}
                        pass
                back_edge_node=3                        | parent store : {0: 0, 2: 0}
                        checking for  back_edge_node=3  | visited store : {0}
                back_edge_node=4                        | parent store : {0: 0, 2: 0}
                        checking for  back_edge_node=4  | visited store : {0}
        neighbour=1
                back_edge_node=0                        | parent store : {0: 0, 2: 0, 1: 0}
                        pass
                back_edge_node=3                        | parent store : {0: 0, 2: 0, 1: 0}
                        checking for  back_edge_node=3  | visited store : {0}
current_node=2
        neighbour=4
                back_edge_node=2                        | parent store : {0: 0, 2: 0, 1: 0, 4: 2}
                        pass
        neighbour=3
                back_edge_node=1                        | parent store : {0: 0, 2: 0, 1: 0, 4: 2, 3: 2}
                        checking for  back_edge_node=1  | visited store : {0, 2}
                back_edge_node=2                        | parent store : {0: 0, 2: 0, 1: 0, 4: 2, 3: 2}
                        pass
current_node=1
        neighbour=3
                back_edge_node=1                        | parent store : {0: 2, 2: 0, 1: 0, 4: 2, 3: 1}
                        pass
                back_edge_node=2                        | parent store : {0: 2, 2: 0, 1: 0, 4: 2, 3: 1}
                        checking for  back_edge_node=2  | visited store : {0, 1, 2}
found back edge at :  3 --> 2
```
> Cycle Found

"""
GRAPH_WITH_CYCLE_REPRESENTATION = """


                                                            +---+             
                                                          / | 1 |\             
                                                         /  +---+ \            
                                                        /          \           
                                                       /            \          
                                                      /              \         
                                                     /                \        
                                                    /                  \       
                                              +---+                     \      
                                              | 0 |                     +---+
                                              +---+                  /--| 3 |
                                                    \               /   +---+
                                                     \             /       
                                                      \           /         
                                                       \         /           
                                                        \  +---+/            
                                                         \ | 2 |           
                                                           +---+ \          
                                                                  \         
                                                                   \        
                                                                    \       
                                                                     \      
                                                                      \-+---+ 
                                                                        | 4 | 
                                                                        +---+ 

                                                                Edge Explaination

                                                                        0 <--> 1
                                                                        0 <--> 2
                                                                        1 <--> 3
                                                                        2 <--> 3
                                                                        2 <--> 4                          
"""

# Graph ( in adjacency list repr )
graph_with_cycle: Graph = {
    0: { 1, 2 },
    1: { 0, 3 },
    2: { 0, 3, 4 },
    3: { 1, 2 },
    4: { 2 }
}

# ---

# Reresentation of graph ( without cycle ) that we'll use for demonstration
"""
> Tracing the graph with Algorithm

```txt
current_node=0
        neighbour=2
                back_edge_node=0                        | parent store : {0: 0, 2: 0}
                        pass
                back_edge_node=4                        | parent store : {0: 0, 2: 0}
                        checking for  back_edge_node=4  | visited store : {0}
        neighbour=1
                back_edge_node=0                        | parent store : {0: 0, 2: 0, 1: 0}
                        pass
current_node=2
        neighbour=4
                back_edge_node=2                        | parent store : {0: 0, 2: 0, 1: 0, 4: 2}
                        pass
                back_edge_node=3                        | parent store : {0: 0, 2: 0, 1: 0, 4: 2}
                        checking for  back_edge_node=3  | visited store : {0, 2}
current_node=1
current_node=4
        neighbour=3
                back_edge_node=4                        | parent store : {0: 1, 2: 0, 1: 0, 4: 2, 3: 4}
                        pass
current_node=3


```
> Cycle Not Exists
"""
GRAPH_WITHOUT_CYCLE_REPRESENTATION  = """
                                                                +---+             
                                                              / | 1 |             
                                                             /  +---+            
                                                            /                     
                                                           /                     
                                                          /                      
                                                         /                       
                                                        /                        
                                                  +---+                          
                                                  | 0 |                     +---+
                                                  +---+\                    | 3 |
                                                        \                   +---+
                                                         \                    |  
                                                          \                   |  
                                                           \                  |  
                                                            \  +---+          |  
                                                             - | 2 |          |  
                                                               +---+ \        |  
                                                                      \       |  
                                                                       \      |  
                                                                        \     |  
                                                                         \    |  
                                                                          \ +---+ 
                                                                            | 4 | 
                                                                            +---+ 

                                                                    Edge Explaination

                                                                            0 <--> 1
                                                                            0 <--> 2
                                                                            2 <--> 4
                                                                            3 <--> 4                           
"""

# Graph ( in adjacency list repr )
graph_without_cycle: Graph = {
    0: { 1, 2 },
    1: { 0 },
    2: { 0, 4 },
    3: { 4 },
    4: { 2, 3 }
}

# ---

def detect(graph: Graph) -> bool:
    """
    Detect Cycle
    """

    visited: Set = set()
    source: Node = 0
    visiting_queue: List = [source]
    parent: dict = {source: source}

    while len(visiting_queue) > 0:

        current_node: Node = visiting_queue.pop(0)
        visited.add(current_node)
        neighbour_nodes: List[Node] = graph[current_node]
        for neighbour in reversed(list(neighbour_nodes)):

            parent[neighbour] = current_node

            # skip the neighbour that is already visited
            if neighbour in visited:
                continue
            
            # check to back edge
            for back_edge_node in graph[neighbour]:
                
                #   - _skip the current node_ and _check if back edge node is already visited_
                if back_edge_node != parent[neighbour] and back_edge_node in visited:
                    print('found back edge at : ', neighbour, '-->', back_edge_node)
                    return True
                
            visiting_queue.append(neighbour)

    return False

def detect_with_pritable_steps(graph: Graph) -> bool:
    """
    Identical to `def detect(graph: Graph):...` , but also prints
    each step ( in alogrith ) on console .
    """

    visited: Set = set()
    source: Node = 0
    visiting_queue: List = [source]
    parent: dict = {source: source}

    while len(visiting_queue) > 0:

        current_node: Node = visiting_queue.pop(0)
        visited.add(current_node)
        print(f"{current_node=}")
        neighbour_nodes: List[Node] = graph[current_node]
        for neighbour in reversed(list(neighbour_nodes)):

            parent[neighbour] = current_node

            # skip the neighbour that is already visited
            if neighbour in visited:
                continue
            
            print(f"\t{neighbour=}")
            # check to back edge
            for back_edge_node in graph[neighbour]:
                
                print(f"\t\t{back_edge_node=}", f'\t\t\t| parent store : {parent}')
                if back_edge_node != parent[neighbour]:
                    print("\t\t\tchecking for ",f"{back_edge_node=}", f'\t| visited store : {visited}')
                    if back_edge_node in visited:
                        print('found back edge at : ', neighbour, '-->', back_edge_node)
                        return True
                else:
                    print('\t\t\tpass')
            visiting_queue.append(neighbour)

    return False

# Testing Entrypoint
# ------------------
if __name__ == "__main__":

    message = lambda result: '--- [ Cycle Detected ] ---' if result == True else '--- [ NO Cycle Detected ] ---'

    result = detect(graph_with_cycle)
    print("\tCheckin for ", GRAPH_WITH_CYCLE_REPRESENTATION, '\n\t', message(result))
    assert result == True

    print('\n', '-'*20, '\n')

    result = detect(graph_without_cycle)
    print("\tCheckin for ", GRAPH_WITHOUT_CYCLE_REPRESENTATION, '\n\t', message(result))
    assert result == False