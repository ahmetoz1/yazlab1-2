COLORS = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'cyan']

def welsh_powell(graph):
    if not graph.nodes:
        return {'coloring': {}, 'num_colors': 0}
    
    node_degrees = []
    for node_id in graph.nodes:
        degree = len(graph.get_neighbors(node_id))
        node_degrees.append((node_id, degree))
    
    node_degrees.sort(key=lambda x: x[1], reverse=True)
    
    coloring = {}
    
    for node_id, _ in node_degrees:
        neighbor_colors = set()
        for neighbor in graph.get_neighbors(node_id):
            if neighbor in coloring:
                neighbor_colors.add(coloring[neighbor])
        
        for color in COLORS:
            if color not in neighbor_colors:
                coloring[node_id] = color
                break
    
    used_colors = set(coloring.values())
    
    return {'coloring': coloring, 'num_colors': len(used_colors)}
