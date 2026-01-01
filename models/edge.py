class Edge:
    def __init__(self, node1_id, node2_id, weight=1.0):
        self.source_id = min(node1_id, node2_id)
        self.target_id = max(node1_id, node2_id)
        self.weight = weight
    
    def get_nodes(self):
        return (self.source_id, self.target_id)
    
    def get_weight(self):
        return self.weight
    
    def set_weight(self, weight):
        self.weight = weight
    
    def contains_node(self, node_id):
        return node_id == self.source_id or node_id == self.target_id
    
    def get_other_node(self, node_id):
        if node_id == self.source_id:
            return self.target_id
        elif node_id == self.target_id:
            return self.source_id
        return None
    
    def __str__(self):
        return f"Edge({self.source_id} -- {self.target_id}, w={self.weight:.2f})"
    
    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.source_id == other.source_id and self.target_id == other.target_id
        return False
    
    def __hash__(self):
        return hash((self.source_id, self.target_id))
