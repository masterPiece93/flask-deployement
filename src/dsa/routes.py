"""
Routes
"""
from flask import (
    render_template,
    request,
    jsonify,
    Blueprint,
    redirect,
    url_for,
    flash
)
from src.dsa.python.graphs.traversal.bfs import bfs
from src.dsa.python.graphs.traversal.dfs import dfs
from src.dsa.python.graphs.shortest_path.dijkstra import path as dijkstra
from src.dsa.python.graphs.shortest_path.bellman_ford import path as bellman_ford
from src.dsa.python.graphs.minimum_spanning_tree.prims import span as prims
from src.dsa.python.graphs.minimum_spanning_tree.kruskal import span as kruskal
from pprint import pprint
from utilities import is_authenticated

def translate(ui_graph_data):
    graph = {}
    for k, v in ui_graph_data.items():
        vertex_id = int(k.replace('n', ''))
        if vertex_id not in graph:
            graph[vertex_id] = set()
        for edge_info in v:
            target_vertex_id = int(edge_info['target'].replace('n', ''))
            if 'weight' not in edge_info or not edge_info['weight']:
                graph[vertex_id].add(target_vertex_id)
            else:
                graph[vertex_id].add((target_vertex_id, int(edge_info['weight'])))
    return graph

__module__ = 'dsa'

dsa_bp = Blueprint(
    __module__,
    f"{__name__}.{__module__}"
)

@dsa_bp.route('/')
def index():
    # if is_authenticated():
    #     return render_template('dsa/index.html')
    # else:
    #     return redirect(url_for('auth.login'))
    
    return render_template('dsa/index.html')

@dsa_bp.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    # if not is_authenticated():
    #     flash('Please Authenticate', 'error')
    #     return jsonify({'result': None})
    
    data = request.json
    graph_data = data.get('graph')
    print("Graph Structure ( UI )  :")
    pprint(graph_data, indent=4)
    graph = translate(graph_data)
    print("Graph Structure ( Formulated ) :")
    pprint(graph, indent=4)
    algorithm = data.get('algorithm')
    source = data.get('source')
    if source:
        source = int(source.replace('n', ''))
    else:
        raise Exception('source not provided')
    try:
        if algorithm == 'bfs':
            result = bfs(graph, source)
        elif algorithm == 'dfs':
            result = dfs(graph, source)
        elif algorithm == 'dijkstra':
            result = dijkstra(graph, source)
        elif algorithm == 'bellman-ford':
            result = bellman_ford(graph, source)
        elif algorithm == 'prims':
            result, cost = prims(graph, source)
            result = {'tree': result, 'cost': cost}
            return jsonify({'result': result['cost']})
        elif algorithm == 'kruskal':
            result, cost = kruskal(graph)
            result = {'tree': result, 'cost': cost}
            return jsonify({'result': result['cost']})
        else:
            return jsonify({'error': 'Invalid algorithm selected'}), 400

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
