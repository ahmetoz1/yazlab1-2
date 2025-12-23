class Edge:
    def __init__(self, node1_id, node2_id, weight=1.0):
        self.source_id = min(node1_id, node2_id)
        self.target_id = max(node1_id, node2_id)
        self.weight = weight
    
    def get_nodes(self):
        return (self.source_id, self.target_id)
    
    def get_weight(self):
        return self.weight
    
    def __str__(self):
        return f"Edge({self.source_id} -- {self.target_id})"
