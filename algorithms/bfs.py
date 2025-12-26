from collections import deque

def bfs(graph, start_id):
    if start_id not in graph.nodes:
        return {'visited': [], 'levels': {}}
    
    visited = []
    levels = {start_id: 0}
    queue = deque([start_id])
    seen = {start_id}
    
    while queue:
        current = queue.popleft()
        visited.append(current)
        
        for neighbor in graph.get_neighbors(current):
            if neighbor not in seen:
                seen.add(neighbor)
                levels[neighbor] = levels[current] + 1
                queue.append(neighbor)
    
    return {'visited': visited, 'levels': levels}
