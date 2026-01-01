import math

def calculate_weight(node1, node2):
    aktiflik_diff = (node1.aktiflik - node2.aktiflik) ** 2
    etkilesim_diff = (node1.etkilesim - node2.etkilesim) ** 2
    baglanti_diff = (node1.baglanti_sayisi - node2.baglanti_sayisi) ** 2
    
    distance = math.sqrt(aktiflik_diff + etkilesim_diff + baglanti_diff)
    weight = 1 / (1 + distance)
    
    return weight
