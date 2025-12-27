import heapq
import math

def heuristic(graph, node_id, end_id):
    node = graph.get_node(node_id)
    end_node = graph.get_node(end_id)
    
    aktiflik_diff = (node.aktiflik - end_node.aktiflik) ** 2
    etkilesim_diff = (node.etkilesim - end_node.etkilesim) ** 2
    baglanti_diff = (node.baglanti_sayisi - end_node.baglanti_sayisi) ** 2
    
    return math.sqrt(aktiflik_diff + etkilesim_diff + baglanti_diff)

def astar(graph, start_id, end_id):
    if start_id not in graph.nodes or end_id not in graph.nodes:
        return {'path': [], 'cost': float('inf')}
    
    if start_id == end_id:
        return {'path': [start_id], 'cost': 0}
    
    g_score = {node_id: float('inf') for node_id in graph.nodes}
    g_score[start_id] = 0
    
    f_score = {node_id: float('inf') for node_id in graph.nodes}
    f_score[start_id] = heuristic(graph, start_id, end_id)
    
    previous = {}
    pq = [(f_score[start_id], start_id)]
    visited = set()
    
    while pq:
        current_f, current = heapq.heappop(pq)
        
        if current == end_id:
            break
        
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor in graph.get_neighbors(current):
            if neighbor in visited:
                continue
            
            edge = graph.get_edge(current, neighbor)
            weight = edge.get_weight()
            tentative_g = g_score[current] + weight
            
            if tentative_g < g_score[neighbor]:
                previous[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(graph, neighbor, end_id)
                heapq.heappush(pq, (f_score[neighbor], neighbor))
    
    if end_id not in previous and start_id != end_id:
        return {'path': [], 'cost': float('inf')}
    
    path = []
    current = end_id
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    
    return {'path': path, 'cost': g_score[end_id]}
