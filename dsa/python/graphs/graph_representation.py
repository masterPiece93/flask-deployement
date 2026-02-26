"""

"""
from typing import NewType, List, Tuple, Optional, Dict, Union, Any


class Types:
    """Custom Types"""
    Node = NewType('Node', int)


class RepresentationOption:
    """
    Graphs Representation Options
    =============================
    - we can represent graphs in 3 standard ways
        - ADJACENCY_LIST
        - ADJACENCY_MATRIX
        - EDGE_LIST

    1. ADJACENCY_LIST
        - a list contains the neighbouring nodes
            - a node con be represented as a number ( like in our case ), alphabet or class object .
        - we keep a dict to store key:-{node} and value:-{list of neighbouring nodes}
    2. ADJACENCY_MATRIX
        - a list of list , representing a 2D matrix
        - where , matrix[i][j] refer to a value that help us decide if an edge exists
            - useually this value is boolean ( true/false )
            - in more advanced implementations we keep it as a positive integer that represents a weight/cost/priority
    3. EDGE_LIST
        - a list contains the edges
            - an edge con be represented as a tuple ( u, v ) of vertices . Each pair (u,v) signifies an edge connecting node u to node v .
            - in more advanced implementations we keep (u, v, w) , where `w` signifies weight/cost/priority of that edge

    - There is a reason why we have 3 representations of graph
        - each representation is best suited in a certain type of algorithm .
        - It's not that , the other representations will not solve some algorithm , but might act slow .
    """
    ADJACENCY_LIST = "ADJACENCY_LIST"
    ADJACENCY_MATRIX = "ADJACENCY_MATRIX"
    EDGE_LIST = "EDGE_LIST"


class Graph:
    """
    Graph Handling Class
    ====================
    - For keeping things simple , we have assumed that you name your nodes
        with positive integer value identifier only .

    NOTE:
        - !WARNING : please add nodes in incremental order only .
        - !WARNING : please start node counter from `0` .
    """
    def __init__(self):
        self._adjacency_list:   Dict[Types.Node, List[Types.Node]] = {}
        self._adjacency_matrix: List[List[bool]] = []
        self._edge_list:        List[Tuple[Types.Node, Types.Node, Optional[int]]] = []
        self._meta:             Dict[str, Any] = {}
    
    @property
    def meta(self) -> Dict[str, Any]:
        return self._meta
    
    @meta.setter
    def meta(self, value: Dict[str, Any]) -> Dict[str, Any]:
        self._meta = value
        return self._meta
    
    @property
    def adjacency_list(self) -> List[Types.Node]:
        return self._adjacency_list
    
    @property
    def adjacency_matrix(self) -> List[Types.Node]:
        return self._adjacency_matrix
    
    @property
    def edge_list(self) -> List[Types.Node]:
        return self._edge_list
    
    def add_node(self, value: Types.Node, to_representation: Optional[RepresentationOption] = None) -> None:
        """
        
        """
        match to_representation:

            case RepresentationOption.ADJACENCY_LIST:
                self._adjacency_list[value] = []
            
            case RepresentationOption.ADJACENCY_MATRIX:
                elem = len(self._adjacency_matrix[0]) if self._adjacency_matrix else 0
                self._adjacency_matrix.append([False]*elem)
                for row in self._adjacency_matrix:
                    row.append(False)
            
            case RepresentationOption.EDGE_LIST:
                ...
            
            case _:
                self.add_node(value, to_representation=RepresentationOption.ADJACENCY_LIST)
                self.add_node(value, to_representation=RepresentationOption.ADJACENCY_MATRIX)
                self.add_node(value, to_representation=RepresentationOption.EDGE_LIST)

    def add_edge(self, value: Tuple[Types.Node, Types.Node], to_representation: Optional[RepresentationOption]=None) -> None:
        """
        
        """
        _from: Types.Node = value[0]
        _to: Types.Node = value[1]

        match to_representation:
        
            case RepresentationOption.ADJACENCY_LIST:
                self._adjacency_list[_from].append(_to)
            
            case RepresentationOption.ADJACENCY_MATRIX:
                self._adjacency_matrix[_from][_to] = True
            
            case RepresentationOption.EDGE_LIST:
                self._edge_list.append((_from, _to))
            
            case _:
                self.add_edge(value, to_representation=RepresentationOption.ADJACENCY_LIST)
                self.add_edge(value, to_representation=RepresentationOption.ADJACENCY_MATRIX)
                self.add_edge(value, to_representation=RepresentationOption.EDGE_LIST)

    def __str__(self):
        return f"""

        Adjacency List
            {self._adjacency_list}
        Adjacency Matrix
            {self._adjacency_matrix}
        Edge List
            {self._edge_list}

        """


class Utilities:

    @staticmethod
    def print_adjacency_list(graph: Graph):
        print("\nAdjacency List :\n")
        for key, value in graph.adjacency_list.items():
            print(f"{key} : {value}")

    @staticmethod
    def print_adjacency_matrix(graph: Graph):
        print("\nAdjacency Matrix :\n")
        print(' ', ' '.join([str(v) for v in range(len(graph.adjacency_matrix))]))
        for idx, row in enumerate(graph.adjacency_matrix):
            print(idx, *[{True: 'T', False: 'F'}[v] for v in row])

    @staticmethod
    def print_edge_list(graph: Graph):
        print("\nEdge List :\n")
        for value in graph.edge_list:
            print(f"- {value}")

if __name__ == '__main__':
    graph: Graph = Graph()
    meta: dict = graph.meta
    meta['diagram'] = """
    Symbols :
        o : source
        * : desination
        
        Directed edges from nodeA to nodeB can be represented as :

            [A]o------*[B]
            
            ___

            [A]o
                \
                 \
                  *
                  [B]
            ___

            [A]
             o
             |
             |
             *
            [B]

            ___

                 [B]
                 *           
                /
               / 
              o
            [A]
            ___
        
        Un-Directed edges from nodeA to nodeB can be represented as :

            [A]--------[B]
            
            ___

            [A]
                \
                 \
                  [B]
            ___

            [A]
             |
             |
             |
             |
            [B]

            ___

                 [B]
                 /     
                /
               / 
              /
            [A]
            ___
        
    Graph Representation:

            [2]o-------*[6]o-------------:
           *             *               |
          /              |               *
         /               |              [0]
        /                |               *
       o                 o               |
    [1] o---[3]--------*[5]o-------------:
       o             -*    
        \          -/       
         \       -/         
          \    -/
           *  o
           [4]

        - it's a directed graph
        - it's connected
        - it's acyclic

        we can call it as a DAG ( directed acyclic graph )
    """
    
    # add nodes
    graph.add_node(0)
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)
    graph.add_node(4)
    graph.add_node(5)
    graph.add_node(6)

    #add edges
    graph.add_edge((1,2))
    graph.add_edge((1,3))
    graph.add_edge((1,4))
    graph.add_edge((3,5))
    graph.add_edge((4,5))
    graph.add_edge((2,6))
    graph.add_edge((5,6))
    graph.add_edge((6,0))
    graph.add_edge((5,0))
    
    print("\nRepresentation :\n")
    print(graph.meta['diagram'])

    Utilities.print_adjacency_list(graph)
    Utilities.print_adjacency_matrix(graph)
    Utilities.print_edge_list(graph)
