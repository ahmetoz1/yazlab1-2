import heapq

def dijkstra(graph, start_id, end_id):
    if start_id not in graph.nodes or end_id not in graph.nodes:
        return {'path': [], 'cost': float('inf')}
    
    if start_id == end_id:
        return {'path': [start_id], 'cost': 0}
    
    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_id] = 0
    previous = {}
    
    pq = [(0, start_id)]
    visited = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == end_id:
            break
        
        for neighbor in graph.get_neighbors(current):
            if neighbor in visited:
                continue
            
            edge = graph.get_edge(current, neighbor)
            weight = edge.get_weight()
            new_dist = current_dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    if end_id not in previous and start_id != end_id:
        return {'path': [], 'cost': float('inf')}
    
    path = []
    current = end_id
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    
    return {'path': path, 'cost': distances[end_id]}
