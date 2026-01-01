class Node:
    def __init__(self, node_id, aktiflik=0.5, etkilesim=0, baglanti_sayisi=0, label=None):
        self.node_id = node_id
        self.aktiflik = aktiflik
        self.etkilesim = etkilesim
        self.baglanti_sayisi = baglanti_sayisi
        self.label = label if label else f"Kullanici {node_id}"
    
    def get_id(self):
        return self.node_id
    
    def __str__(self):
        return f"Node({self.node_id}, {self.label})"
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False
    
    def __hash__(self):
        return hash(self.node_id)
