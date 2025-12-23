class Node:
    def __init__(self, node_id, aktiflik=0.5, etkilesim=0, baglanti_sayisi=0):
        self.node_id = node_id
        self.aktiflik = aktiflik
        self.etkilesim = etkilesim
        self.baglanti_sayisi = baglanti_sayisi
    
    def get_id(self):
        return self.node_id
    
    def __str__(self):
        return f"Node({self.node_id})"
