"""
BFS ( Breadth First Search )
============================

> Slogan : " _jo milta jaye , usko use kro aur ussi ke aage find kro_ "

"""
from typing import *

# Custom Types

# - a node ( vertex ) type
Node = NewType('Node', int)
# - a graph type
Graph = NewType('Graph', Dict[Node, Set]) # Adjacency List

# Reresentation of graph that we'll use for demonstration
GRAPH_REPRESENTATION = """

                            +---+             
                          -*| 1 |             
                         /  +---+o            
                        /     o    \           
                       /      |     \          
                      /       |      \         
                     /        |       \        
                    o         |        \       
              +---+           /         *      
   -          | 0 |          |         -+---+
              +---+o         |          | 3 |
                    \        |       /* +---+
                     \       |     /-     o  
                      \      |   /-       |  
                       \     *  o         |  
                        \  +---+          |  
                         -*| 2 |o         |  
                           +---+ \        |  
                                  \       |  
                                   \      |  
                                    \     |  
                                     \    *  
                                      \ +---+ 
                                      -*| 4 | 
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


def bfs(graph: Graph, source: Node):
    """
    BFS Traversing Alogo

    - Note
        - using adjacency list representation
        - bfs traversal order differ for different source
    """
    # Steps
    # -----

    # Prepration

    # - variable to track the linear order of arrival of nodes in traversal
    traversal_order_track: str = ''
    # - storage for already visited nodes
    #       - visited flag check
    visited: set[Node] = set()
    # - visiting queue
    #       - it determines which node to visit next
    to_visit: List[Node] = [source]
    
    # Starting point

    # - idefinate loop until all nodes are visited
    while to_visit:
        # 1. visit a node
        # 2. mark it as visited
        # 3. add it to your traversal tracking
        # 4. fetch all neighbour nodes
        # 5. add the neighbours to the queue for visiting
        #       - only if a node is neither visited & not to be visited in queue
        node: Node = to_visit.pop(0)                            # 1.
        visited.add(node)                                       # 2.
        traversal_order_track += f"-> {node} "                  # 3.
        neighbour_nodes: List[Node] = graph[node]               # 4.
        for node in neighbour_nodes:                            # 5.
            if node not in visited and node not in to_visit:    # 5.1
                to_visit.append(node)
    # return results
    return traversal_order_track.strip('->').strip(' ')

# Testing Entrypoint
# ------------------
if __name__ == '__main__':

    bfs_traversal_order: str = bfs(graph, Node(0))
    print(bfs_traversal_order)
    expected_order = "0 -> 1 -> 2 -> 3 -> 4"
    assert bfs_traversal_order == expected_order
