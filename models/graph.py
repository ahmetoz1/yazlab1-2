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
        
        edges_to_remove = []
        for edge_key in self.edges:
            if node_id in edge_key:
                edges_to_remove.append(edge_key)
        for edge_key in edges_to_remove:
            self.remove_edge(edge_key[0], edge_key[1])
        
        del self.nodes[node_id]
        del self.adjacency[node_id]
        return True
    
    def get_node(self, node_id):
        return self.nodes.get(node_id, None)
    
    def get_all_nodes(self):
        return list(self.nodes.values())
    
    def add_edge(self, node1_id, node2_id, weight=1.0):
        if node1_id not in self.nodes or node2_id not in self.nodes:
            return False
        if node1_id == node2_id:
            return False
        
        edge_key = (min(node1_id, node2_id), max(node1_id, node2_id))
        if edge_key in self.edges:
            return False
        
        edge = Edge(node1_id, node2_id, weight)
        self.edges[edge_key] = edge
        
        self.adjacency[node1_id].append(node2_id)
        self.adjacency[node2_id].append(node1_id)
        
        return True
    
    def remove_edge(self, node1_id, node2_id):
        edge_key = (min(node1_id, node2_id), max(node1_id, node2_id))
        if edge_key not in self.edges:
            return False
        
        del self.edges[edge_key]
        
        if node2_id in self.adjacency.get(node1_id, []):
            self.adjacency[node1_id].remove(node2_id)
        if node1_id in self.adjacency.get(node2_id, []):
            self.adjacency[node2_id].remove(node1_id)
        
        return True
    
    def get_neighbors(self, node_id):
        return self.adjacency.get(node_id, [])
    
    def get_edge(self, node1_id, node2_id):
        edge_key = (min(node1_id, node2_id), max(node1_id, node2_id))
        return self.edges.get(edge_key, None)
    
    def get_all_edges(self):
        return list(self.edges.values())
