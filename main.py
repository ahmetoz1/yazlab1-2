import sys
from PyQt5.QtWidgets import QApplication
from models.graph import Graph
from gui import MainWindow

def create_sample_graph():
    graph = Graph()
    
    graph.add_node(1, aktiflik=0.8, etkilesim=12, label="Kullanici 1")
    graph.add_node(2, aktiflik=0.6, etkilesim=8, label="Kullanici 2")
    graph.add_node(3, aktiflik=0.9, etkilesim=15, label="Kullanici 3")
    graph.add_node(4, aktiflik=0.4, etkilesim=5, label="Kullanici 4")
    graph.add_node(5, aktiflik=0.7, etkilesim=10, label="Kullanici 5")
    
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    
    return graph

def main():
    app = QApplication(sys.argv)
    
    graph = create_sample_graph()
    
    window = MainWindow(graph)
    window.show()
    window.canvas.draw_graph()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
