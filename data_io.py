import json

def save_json(graph, filepath, positions=None):
    
    data = {
        'nodes': [],
        'edges': []
    }
    
    for node_id, node in graph.nodes.items():
        node_data = {
            'id': node_id,
            'label': node.label,
            'aktiflik': node.aktiflik,
            'etkilesim': node.etkilesim
        }
        if positions and node_id in positions:
            node_data['x'] = positions[node_id][0]
            node_data['y'] = positions[node_id][1]
        data['nodes'].append(node_data)
    
    for edge_key, edge in graph.edges.items():
        data['edges'].append({
            'source': edge.source_id,
            'target': edge.target_id,
            'weight': edge.get_weight()
        })
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(graph, filepath):
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    graph.nodes.clear()
    graph.edges.clear()
    graph.adjacency.clear()
    
    positions = {}
    for node_data in data.get('nodes', []):
        node_id = node_data['id']
        graph.add_node(
            node_id,
            aktiflik=node_data.get('aktiflik', 0.5),
            etkilesim=node_data.get('etkilesim', 0),
            label=node_data.get('label')
        )
        if 'x' in node_data and 'y' in node_data:
            positions[node_id] = (node_data['x'], node_data['y'])
    for edge_data in data.get('edges', []):
        graph.add_edge(edge_data['source'], edge_data['target'])
    
    return positions

