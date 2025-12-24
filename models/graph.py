from models.node import Node
from models.edge import Edge

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.adjacency = {}
    
    def add_node(self, node_id, aktiflik=0.5, etkilesim=0, baglanti_sayisi=0):
        if node_id in self.nodes:
            return False
        node = Node(node_id, aktiflik, etkilesim, baglanti_sayisi)
        self.nodes[node_id] = node
        self.adjacency[node_id] = []
        return True
    
    def remove_node(self, node_id):
        if node_id not in self.nodes:
            return False
        del self.nodes[node_id]
        del self.adjacency[node_id]
        return True
    
    def get_node(self, node_id):
        return self.nodes.get(node_id, None)
    
    def get_all_nodes(self):
        return list(self.nodes.values())
