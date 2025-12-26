def dfs(graph, start_id):
    if start_id not in graph.nodes:
        return {'visited': [], 'discovery': {}}
    
    visited = []
    discovery = {}
    time = [0]
    
    def dfs_visit(node_id):
        time[0] += 1
        discovery[node_id] = time[0]
        visited.append(node_id)
        
        for neighbor in graph.get_neighbors(node_id):
            if neighbor not in discovery:
                dfs_visit(neighbor)
    
    dfs_visit(start_id)
    return {'visited': visited, 'discovery': discovery}
