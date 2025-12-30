from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QGroupBox, QMessageBox, QInputDialog,
                             QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
                             QGraphicsLineItem, QGraphicsTextItem, QStatusBar)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
import math
import time

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y, radius=25, canvas=None):
        super().__init__(-radius, -radius, radius*2, radius*2)
        self.node_id = node_id
        self.radius = radius
        self.canvas = canvas
        self.setPos(x, y)
        self.setBrush(QBrush(QColor('#4ECDC4')))
        self.setPen(QPen(Qt.white, 2))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        
        self.label = QGraphicsTextItem(str(node_id), self)
        self.label.setDefaultTextColor(Qt.white)
        self.label.setFont(QFont('Arial', 10, QFont.Bold))
        self.label.setPos(-8, -10)
        
        self.selected_for_edge = False
    
    def set_color(self, color):
        self.setBrush(QBrush(QColor(color)))
    
    def set_selected_for_edge(self, selected):
        self.selected_for_edge = selected
        if selected:
            self.setPen(QPen(QColor('#FFD93D'), 4))
        else:
            self.setPen(QPen(Qt.white, 2))

class EdgeItem(QGraphicsLineItem):
    def __init__(self, node1_item, node2_item):
        super().__init__()
        self.node1 = node1_item
        self.node2 = node2_item
        self.setPen(QPen(QColor('#6c757d'), 2))
        self.update_position()
    
    def update_position(self):
        p1 = self.node1.scenePos()
        p2 = self.node2.scenePos()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

class GraphCanvas(QGraphicsView):
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.node_items = {}
        self.edge_items = {}
        self.setBackgroundBrush(QBrush(QColor('#1a1a2e')))
        self.parent_window = parent
        self.selected_nodes = []
    
    def draw_graph(self):
        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()
        self.selected_nodes.clear()
        
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        if n == 0:
            return
        
        cx, cy = 300, 250
        radius = 150
        
        for i, node_id in enumerate(nodes):
            angle = 2 * math.pi * i / n
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            node_item = NodeItem(node_id, x, y, canvas=self)
            self.scene.addItem(node_item)
            self.node_items[node_id] = node_item
        
        for edge_key in self.graph.edges:
            n1, n2 = edge_key
            if n1 in self.node_items and n2 in self.node_items:
                edge_item = EdgeItem(self.node_items[n1], self.node_items[n2])
                self.scene.addItem(edge_item)
                self.edge_items[edge_key] = edge_item
                edge_item.setZValue(-1)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        item = self.itemAt(event.pos())
        if isinstance(item, NodeItem):
            self.toggle_node_selection(item.node_id)
    
    def toggle_node_selection(self, node_id):
        if node_id in self.selected_nodes:
            self.selected_nodes.remove(node_id)
            self.node_items[node_id].set_selected_for_edge(False)
        else:
            if len(self.selected_nodes) >= 2:
                old_id = self.selected_nodes.pop(0)
                self.node_items[old_id].set_selected_for_edge(False)
            self.selected_nodes.append(node_id)
            self.node_items[node_id].set_selected_for_edge(True)
        
        if self.parent_window:
            self.parent_window.control_panel.update_edge_inputs()
    
    def highlight_path(self, path):
        for node_id in path:
            if node_id in self.node_items:
                self.node_items[node_id].set_color('#FF6B6B')
        
        for i in range(len(path) - 1):
            key = (min(path[i], path[i+1]), max(path[i], path[i+1]))
            if key in self.edge_items:
                self.edge_items[key].setPen(QPen(QColor('#FF6B6B'), 4))
    
    def apply_coloring(self, coloring):
        for node_id, color in coloring.items():
            if node_id in self.node_items:
                self.node_items[node_id].set_color(color)
    
    def reset_colors(self):
        for node_item in self.node_items.values():
            node_item.set_color('#4ECDC4')
        for edge_item in self.edge_items.values():
            edge_item.setPen(QPen(QColor('#6c757d'), 2))

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        node_group = QGroupBox("Dugum Islemleri")
        node_layout = QVBoxLayout()
        
        self.node_id_input = QLineEdit()
        self.node_id_input.setPlaceholderText("Dugum ID")
        node_layout.addWidget(self.node_id_input)
        
        btn_add_node = QPushButton("Dugum Ekle")
        btn_add_node.clicked.connect(self.add_node)
        node_layout.addWidget(btn_add_node)
        
        btn_remove_node = QPushButton("Dugum Sil")
        btn_remove_node.clicked.connect(self.remove_node)
        node_layout.addWidget(btn_remove_node)
        
        node_group.setLayout(node_layout)
        layout.addWidget(node_group)
        
        edge_group = QGroupBox("Kenar Islemleri")
        edge_layout = QVBoxLayout()
        
        self.edge_n1_input = QLineEdit()
        self.edge_n1_input.setPlaceholderText("Dugum 1 ID")
        edge_layout.addWidget(self.edge_n1_input)
        
        self.edge_n2_input = QLineEdit()
        self.edge_n2_input.setPlaceholderText("Dugum 2 ID")
        edge_layout.addWidget(self.edge_n2_input)
        
        btn_add_edge = QPushButton("Kenar Ekle")
        btn_add_edge.clicked.connect(self.add_edge)
        edge_layout.addWidget(btn_add_edge)
        
        btn_remove_edge = QPushButton("Kenar Sil")
        btn_remove_edge.clicked.connect(self.remove_edge)
        edge_layout.addWidget(btn_remove_edge)
        
        edge_group.setLayout(edge_layout)
        layout.addWidget(edge_group)
        
        algo_group = QGroupBox("Algoritmalar")
        algo_layout = QVBoxLayout()
        
        btn_bfs = QPushButton("BFS")
        btn_bfs.clicked.connect(self.run_bfs)
        algo_layout.addWidget(btn_bfs)
        
        btn_dfs = QPushButton("DFS")
        btn_dfs.clicked.connect(self.run_dfs)
        algo_layout.addWidget(btn_dfs)
        
        btn_dijkstra = QPushButton("Dijkstra")
        btn_dijkstra.clicked.connect(self.run_dijkstra)
        algo_layout.addWidget(btn_dijkstra)
        
        btn_astar = QPushButton("A*")
        btn_astar.clicked.connect(self.run_astar)
        algo_layout.addWidget(btn_astar)
        
        btn_components = QPushButton("Bagli Bilesenler")
        btn_components.clicked.connect(self.run_components)
        algo_layout.addWidget(btn_components)
        
        btn_centrality = QPushButton("Merkezilik")
        btn_centrality.clicked.connect(self.run_centrality)
        algo_layout.addWidget(btn_centrality)
        
        btn_coloring = QPushButton("Renklendirme")
        btn_coloring.clicked.connect(self.run_coloring)
        algo_layout.addWidget(btn_coloring)
        
        btn_reset = QPushButton("Sifirla")
        btn_reset.clicked.connect(self.reset_colors)
        algo_layout.addWidget(btn_reset)
        
        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)
        
        result_group = QGroupBox("Sonuclar")
        result_layout = QVBoxLayout()
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(150)
        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        layout.addStretch()
        self.setLayout(layout)
        self.setFixedWidth(200)
    
    def update_edge_inputs(self):
        selected = self.parent_window.canvas.selected_nodes
        if len(selected) >= 1:
            self.edge_n1_input.setText(str(selected[0]))
        if len(selected) >= 2:
            self.edge_n2_input.setText(str(selected[1]))
    
    def add_node(self):
        try:
            node_id = int(self.node_id_input.text())
            if self.parent_window.graph.add_node(node_id):
                self.parent_window.canvas.draw_graph()
                self.parent_window.statusBar().showMessage(f"Dugum {node_id} eklendi")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Gecersiz ID!")
    
    def remove_node(self):
        try:
            node_id = int(self.node_id_input.text())
            if self.parent_window.graph.remove_node(node_id):
                self.parent_window.canvas.draw_graph()
                self.parent_window.statusBar().showMessage(f"Dugum {node_id} silindi")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Gecersiz ID!")
    
    def add_edge(self):
        try:
            n1 = int(self.edge_n1_input.text())
            n2 = int(self.edge_n2_input.text())
            if self.parent_window.graph.add_edge(n1, n2):
                self.parent_window.canvas.draw_graph()
                self.parent_window.statusBar().showMessage(f"Kenar {n1}-{n2} eklendi")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Gecersiz ID!")
    
    def remove_edge(self):
        try:
            n1 = int(self.edge_n1_input.text())
            n2 = int(self.edge_n2_input.text())
            if self.parent_window.graph.remove_edge(n1, n2):
                self.parent_window.canvas.draw_graph()
                self.parent_window.statusBar().showMessage(f"Kenar {n1}-{n2} silindi")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Gecersiz ID!")
    
    def run_bfs(self):
        start, ok = QInputDialog.getInt(self, "BFS", "Baslangic dugum ID:")
        if ok:
            from algorithms.bfs import bfs
            start_time = time.time()
            result = bfs(self.parent_window.graph, start)
            elapsed = (time.time() - start_time) * 1000
            self.result_text.setText(f"BFS Sonucu:\n{result['visited']}\n\nSure: {elapsed:.2f} ms")
            self.parent_window.canvas.reset_colors()
            for node_id in result['visited']:
                if node_id in self.parent_window.canvas.node_items:
                    level = result['levels'].get(node_id, 0)
                    colors = ['#FF6B6B', '#FF8E72', '#FFB07A', '#FFD185', '#FFF192']
                    self.parent_window.canvas.node_items[node_id].set_color(colors[min(level, 4)])
    
    def run_dfs(self):
        start, ok = QInputDialog.getInt(self, "DFS", "Baslangic dugum ID:")
        if ok:
            from algorithms.dfs import dfs
            start_time = time.time()
            result = dfs(self.parent_window.graph, start)
            elapsed = (time.time() - start_time) * 1000
            self.result_text.setText(f"DFS Sonucu:\n{result['visited']}\n\nSure: {elapsed:.2f} ms")
    
    def run_dijkstra(self):
        start, ok1 = QInputDialog.getInt(self, "Dijkstra", "Baslangic dugum ID:")
        if ok1:
            end, ok2 = QInputDialog.getInt(self, "Dijkstra", "Bitis dugum ID:")
            if ok2:
                from algorithms.dijkstra import dijkstra
                start_time = time.time()
                result = dijkstra(self.parent_window.graph, start, end)
                elapsed = (time.time() - start_time) * 1000
                self.result_text.setText(f"Dijkstra:\nYol: {result['path']}\nMaliyet: {result['cost']:.4f}\n\nSure: {elapsed:.2f} ms")
                self.parent_window.canvas.reset_colors()
                self.parent_window.canvas.highlight_path(result['path'])
    
    def run_astar(self):
        start, ok1 = QInputDialog.getInt(self, "A*", "Baslangic dugum ID:")
        if ok1:
            end, ok2 = QInputDialog.getInt(self, "A*", "Bitis dugum ID:")
            if ok2:
                from algorithms.astar import astar
                start_time = time.time()
                result = astar(self.parent_window.graph, start, end)
                elapsed = (time.time() - start_time) * 1000
                self.result_text.setText(f"A*:\nYol: {result['path']}\nMaliyet: {result['cost']:.4f}\n\nSure: {elapsed:.2f} ms")
                self.parent_window.canvas.reset_colors()
                self.parent_window.canvas.highlight_path(result['path'])
    
    def run_components(self):
        from algorithms.components import find_components
        start_time = time.time()
        result = find_components(self.parent_window.graph)
        elapsed = (time.time() - start_time) * 1000
        text = f"Bilesen Sayisi: {result['count']}\n\n"
        for i, comp in enumerate(result['components']):
            text += f"Bilesen {i+1}: {comp}\n"
        text += f"\nSure: {elapsed:.2f} ms"
        self.result_text.setText(text)
    
    def run_centrality(self):
        from algorithms.centrality import degree_centrality
        start_time = time.time()
        result = degree_centrality(self.parent_window.graph)
        elapsed = (time.time() - start_time) * 1000
        text = "En Merkezi 5 Dugum:\n"
        for node_id, val in result['top_5']:
            text += f"  {node_id}: {val:.4f}\n"
        text += f"\nSure: {elapsed:.2f} ms"
        self.result_text.setText(text)
    
    def run_coloring(self):
        from algorithms.welsh_powell import welsh_powell
        start_time = time.time()
        result = welsh_powell(self.parent_window.graph)
        elapsed = (time.time() - start_time) * 1000
        self.result_text.setText(f"Kullanilan Renk: {result['num_colors']}\n\nSure: {elapsed:.2f} ms")
        self.parent_window.canvas.apply_coloring(result['coloring'])
    
    def reset_colors(self):
        self.parent_window.canvas.reset_colors()
        self.result_text.clear()

class MainWindow(QMainWindow):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.setWindowTitle("Sosyal Ag Analizi")
        self.setGeometry(100, 100, 900, 650)
        self.init_ui()
    
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QHBoxLayout()
        
        self.control_panel = ControlPanel(self)
        layout.addWidget(self.control_panel)
        
        self.canvas = GraphCanvas(self.graph, self)
        layout.addWidget(self.canvas)
        
        central.setLayout(layout)
        
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Hazir")
