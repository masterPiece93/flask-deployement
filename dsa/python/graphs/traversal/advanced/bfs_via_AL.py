"""
BFS via AL ( Adjacency List )

- we'll do graph traversal via Adjacency List 
"""
from graphs.graph_representation import Graph, Types
from typing import *

def bfs(source: Types.Node):
    """
    """
    # track the linear order of arrival of nodes in traversal
    traversal_order_track: str = ''
    
    # visited flag check
    visited: set[Types.Node] = set()
    # visiting queue
    to_visit: List[Types.Node] = [source]
    # 
    while to_visit:
        node = to_visit.pop(0)
        visited.add(node)
        traversal_order_track += f"-> {node} "
        neighbour_nodes = node.get_links()
        for node in neighbour_nodes:
            if node not in visited and node not in to_visit:
                to_visit.append(node)
    return traversal_order_track.strip('->').strip(' ')
