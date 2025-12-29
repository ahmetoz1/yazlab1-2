def degree_centrality(graph):
    centrality = {}
    n = len(graph.nodes)
    
    if n <= 1:
        for node_id in graph.nodes:
            centrality[node_id] = 0
        return {'centrality': centrality, 'top_5': []}
    
    for node_id in graph.nodes:
        degree = len(graph.get_neighbors(node_id))
        centrality[node_id] = degree / (n - 1)
    
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_nodes[:5]
    
    return {'centrality': centrality, 'top_5': top_5}
