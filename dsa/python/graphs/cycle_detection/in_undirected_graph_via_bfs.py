"""
Cycle Detection ( using BFS )
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
    visting_stack: List = []
    
    visited: Set = set()
    source: Node = 0
    parent:dict = {source:source}
    visting_stack.append(source)

    while len(visting_stack) > 0:

        current_node = visting_stack.pop()
        visited.add(current_node)
        neighbour_nodes = graph[current_node]

        for neighbour in neighbour_nodes:
            
            # attach parent
            parent[neighbour] = current_node

            # skip the neighbour that is already visited
            if neighbour in visited:
                continue
            
            # check for back edge
            for back_edge_node in graph[neighbour] :
                #   - _skip the current node_ and _check if back edge node is already visited_
                if back_edge_node != parent[neighbour] and back_edge_node in visited:
                    return True
            
            visting_stack.append(neighbour)
        
    return False

def detect_with_pritable_steps(graph: Graph) -> bool:
    """
    Identical to `def detect(graph: Graph):...` , but also prints
    each step ( in alogrith ) on console .
    """
    visting_stack: List = []
    
    visited: Set = set()
    source: Node = 0
    parent:dict = {source:source}
    visting_stack.append(source)

    while len(visting_stack) > 0:

        current_node = visting_stack.pop()
        visited.add(current_node)
        neighbour_nodes = graph[current_node]
        print(f"{current_node=}")
        for neighbour in neighbour_nodes:
            
            parent[neighbour] = current_node

            # skip the neighbour that is already visited
            if neighbour in visited:
                continue
            
            print(f"\t{neighbour=}")
            # check to back edge
            for back_edge_node in graph[neighbour] :
                #   - __
                # if direct_neighbour != current_node and direct_neighbour in visited:
                print(f"\t\t{back_edge_node=}", f'\t\t\t| parent store : {parent}')
                if back_edge_node != parent[neighbour]:
                    print("\t\t\tchecking for ",f"{back_edge_node=}")
                    if back_edge_node in visited:
                        print('found back edge at : ', neighbour, '-->', back_edge_node)
                        return True
                else:
                    print('\t\t\tpass')
            visting_stack.append(neighbour)
        
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
    
                