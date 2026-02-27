"""
DFS ( Depth First Search )
"""
from typing import *

Node = NewType('Node', int)
Graph = NewType('Graph', Dict[Node, Set]) # Adjacency List

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


def dfs(graph: Graph, source: Node):
    """
    - using adjacency list representation
    - dfs traversal order differ for different source
    """
    # track the linear order of arrival of nodes in traversal
    traversal_order_track: str = ''
    
    # visited flag check
    visited: set[Node] = set()
    # visiting queue
    to_visit: List[Node] = [source]
    # 
    while to_visit:
        node = to_visit.pop()
        visited.add(node)
        traversal_order_track += f"-> {node} "
        neighbour_nodes = graph[node]
        
        for node in reversed(list(neighbour_nodes)): # `reversed` function ensures that we get the latest made neighbour first
            
            if node not in visited and node not in to_visit:
                to_visit.append(node)
    return traversal_order_track.strip('->').strip(' ')

# entrypoint
if __name__ == '__main__':

    bfs_traversal_order: str = dfs(graph, Node(0))
    print(bfs_traversal_order)
    expected_order = "0 -> 1 -> 3 -> 4 -> 2"
    assert bfs_traversal_order == expected_order
