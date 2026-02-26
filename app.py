import datetime
import logging
from flask import Flask, render_template, request, jsonify
from json import JSONEncoder

app = Flask(__name__)

DEBUG=True
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)
# Assign the custom encoder to the app
app.json_encoder = CustomJSONEncoder

@app.route('/')
def home():
    return """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <h1 style="
        text-align: center;
        background: #000000;
        color: #FFD700;
        border: 0.1em solid gold;
        "
    >
    THE ANKIT </h1>

    <div style="text-align: center;">
    <a href="/ankit-loves-shalu">
    <i class="fa fa-heart" style="font-size:48px;color:red">
    </i>
    </a>
    </div>
    <ul>
        <li>
            <a href="/dsa/"> dsa </a>
        </li>
    </ul>
    """

@app.route('/health')
def health():
    return {"healthy": True}

@app.route('/ankit-loves-shalu')
def message_1():
    return render_template('shalu.html')

@app.route('/callback', methods=['POST'])
def push_notification_webhook():
    print('-'*15)
    print('API Called')
    print(request.headers)
    print('-'*15)
    return {}

# ---------
# DS & Algo
# ---------
from dsa.python.graphs.traversal.bfs import bfs
from dsa.python.graphs.traversal.dfs import dfs
from dsa.python.graphs.shortest_path.dijkstra import path as dijkstra
from dsa.python.graphs.shortest_path.bellman_ford import path as bellman_ford
from dsa.python.graphs.minimum_spanning_tree.prims import span as prims
from dsa.python.graphs.minimum_spanning_tree.kruskal import span as kruskal
from pprint import pprint

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

dsa_route: callable = lambda r: '/dsa' + r

@app.route(dsa_route('/'))
def index():
    return render_template('dsa/index.html')

@app.route(dsa_route('/run-algorithm'), methods=['POST'])
def run_algorithm():
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

if __name__ != '__main__':
    # Get the gunicorn error logger
    gunicorn_logger = logging.getLogger('gunicorn.error')
    # Assign gunicorn's handlers and level to your app's logger
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    
if __name__ == '__main__':
    app.run(debug=True)