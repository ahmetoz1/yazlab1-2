def welsh_powell(graph):
    degrees = []
    for node_id in graph.nodes:
        degree = len(graph.get_neighbors(node_id))
        degrees.append((node_id, degree))
    
    degrees.sort(key=lambda x: x[1], reverse=True)
    
    colors = ['Kirmizi', 'Mavi', 'Yesil', 'Sari', 'Mor', 'Turuncu', 'Pembe', 'Kahverengi']
    coloring = {}
    color_index = 0
    
    for node_id, _ in degrees:
        if node_id in coloring:
            continue
        
        current_color = colors[color_index % len(colors)]
        coloring[node_id] = current_color
        
        for other_id, _ in degrees:
            if other_id in coloring:
                continue
            
            can_color = True
            for neighbor in graph.get_neighbors(other_id):
                if neighbor in coloring and coloring[neighbor] == current_color:
                    can_color = False
                    break
            
            if can_color:
                coloring[other_id] = current_color
        
        color_index += 1
    
    return {'coloring': coloring, 'num_colors': color_index}
