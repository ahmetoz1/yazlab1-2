import json
import random

def generate_test_graph(num_nodes, edge_probability=0.3, filepath=None):
    data = {
        'nodes': [],
        'edges': []
    }
    
    for i in range(1, num_nodes + 1):
        data['nodes'].append({
            'id': i,
            'label': f'Kullanici {i}',
            'aktiflik': round(random.uniform(0.1, 1.0), 2),
            'etkilesim': random.randint(1, 20)
        })
    
    for i in range(1, num_nodes + 1):
        for j in range(i + 1, num_nodes + 1):
            if random.random() < edge_probability:
                data['edges'].append({
                    'source': i,
                    'target': j
                })
    
    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    return data


def generate_disconnected_graph(group1_size, group2_size, filepath=None):
    data = {
        'nodes': [],
        'edges': []
    }
    for i in range(1, group1_size + 1):
        data['nodes'].append({
            'id': i,
            'label': f'Grup1_{i}',
            'aktiflik': round(random.uniform(0.1, 1.0), 2),
            'etkilesim': random.randint(1, 20)
        })
    for i in range(group1_size + 1, group1_size + group2_size + 1):
        data['nodes'].append({
            'id': i,
            'label': f'Grup2_{i}',
            'aktiflik': round(random.uniform(0.1, 1.0), 2),
            'etkilesim': random.randint(1, 20)
        })
    for i in range(1, group1_size + 1):
        for j in range(i + 1, group1_size + 1):
            if random.random() < 0.2:
                data['edges'].append({'source': i, 'target': j})
    for i in range(group1_size + 1, group1_size + group2_size + 1):
        for j in range(i + 1, group1_size + group2_size + 1):
            if random.random() < 0.2:
                data['edges'].append({'source': i, 'target': j})
    
    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    return data


if __name__ == "__main__":
    generate_test_graph(20, 0.3, 'data/test_20.json')
    generate_test_graph(100, 0.1, 'data/test_100.json')
    generate_disconnected_graph(70, 30, 'data/test_null.json')
    print("Test verileri oluşturuldu!")

