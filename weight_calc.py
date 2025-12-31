def calculate_weight(node1, node2):
    aktiflik_diff = abs(node1.aktiflik - node2.aktiflik)
    etkilesim_diff = abs(node1.etkilesim - node2.etkilesim) / 10
    
    denominator = 1 + aktiflik_diff + etkilesim_diff
    if denominator == 0:
        denominator = 0.001
    
    return 1 / denominator
