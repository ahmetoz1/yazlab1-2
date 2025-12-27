def find_components(graph):
    visited = set()
    components = []
    
    def dfs(node_id, component):
        visited.add(node_id)
        component.append(node_id)
        for neighbor in graph.get_neighbors(node_id):
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for node_id in graph.nodes:
        if node_id not in visited:
            component = []
            dfs(node_id, component)
            components.append(component)
    
    return {'count': len(components), 'components': components}
