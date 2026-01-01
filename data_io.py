import json
import csv

def save_json(graph, filepath, positions=None):
    data = {
        'nodes': [],
        'edges': []
    }
    
    for node_id, node in graph.nodes.items():
        node_data = {
            'id': node_id,
            'aktiflik': node.aktiflik,
            'etkilesim': node.etkilesim,
            'baglanti_sayisi': node.baglanti_sayisi,
            'label': node.label
        }
        if positions and node_id in positions:
            node_data['x'] = positions[node_id][0]
            node_data['y'] = positions[node_id][1]
        data['nodes'].append(node_data)
    
    for edge_key, edge in graph.edges.items():
        data['edges'].append({
            'source': edge.source_id,
            'target': edge.target_id,
            'weight': edge.weight
        })
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(graph, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    graph.nodes.clear()
    graph.edges.clear()
    graph.adjacency.clear()
    
    positions = {}
    
    for node_data in data['nodes']:
        graph.add_node(
            node_data['id'],
            node_data.get('aktiflik', 0.5),
            node_data.get('etkilesim', 0),
            node_data.get('baglanti_sayisi', 0),
            node_data.get('label')
        )
        if 'x' in node_data and 'y' in node_data:
            positions[node_data['id']] = (node_data['x'], node_data['y'])
    
    for edge_data in data['edges']:
        graph.add_edge(edge_data['source'], edge_data['target'])
    
    return positions

def save_csv(graph, nodes_file, edges_file):
    with open(nodes_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'aktiflik', 'etkilesim', 'baglanti_sayisi', 'label'])
        for node_id, node in graph.nodes.items():
            writer.writerow([node_id, node.aktiflik, node.etkilesim, node.baglanti_sayisi, node.label])
    
    with open(edges_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['source', 'target', 'weight'])
        for edge in graph.edges.values():
            writer.writerow([edge.source_id, edge.target_id, edge.weight])

def load_csv(graph, nodes_file, edges_file):
    graph.nodes.clear()
    graph.edges.clear()
    graph.adjacency.clear()
    
    with open(nodes_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            graph.add_node(
                int(row['id']),
                float(row['aktiflik']),
                int(row['etkilesim']),
                int(row['baglanti_sayisi']),
                row['label']
            )
    
    with open(edges_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            graph.add_edge(int(row['source']), int(row['target']))
