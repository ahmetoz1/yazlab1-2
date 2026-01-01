def find_components(graph):
    if not graph.nodes:
        return {'count': 0, 'components': []}
    
    visited = set()
    components = []
    
    for node_id in graph.nodes:
        if node_id in visited:
            continue
        
        component = []
        stack = [node_id]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            component.append(current)
            
            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        components.append(component)
    
    return {'count': len(components), 'components': components}
