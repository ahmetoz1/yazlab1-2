from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QGroupBox, QMessageBox, QGraphicsView, QGraphicsScene, 
                             QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
import math

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y, radius=25):
        super().__init__(-radius, -radius, radius*2, radius*2)
        self.node_id = node_id
        self.setPos(x, y)
        self.setBrush(QBrush(QColor('#4ECDC4')))
        self.setPen(QPen(QColor('#2C3E50'), 2))
        self.setFlag(self.ItemIsMovable)
        
        self.label = QGraphicsTextItem(str(node_id), self)
        self.label.setDefaultTextColor(QColor('white'))
        self.label.setFont(QFont('Arial', 10, QFont.Bold))
        self.label.setPos(-8, -10)
    
    def set_color(self, color):
        self.setBrush(QBrush(QColor(color)))

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
    
    def draw_graph(self):
        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()
        
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        cx, cy = 300, 250
        radius = 150
        
        for i, node_id in enumerate(nodes):
            angle = 2 * math.pi * i / max(n, 1)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            node_item = NodeItem(node_id, x, y)
            self.scene.addItem(node_item)
            self.node_items[node_id] = node_item
        
        for edge in self.graph.get_all_edges():
            n1, n2 = edge.source_id, edge.target_id
            if n1 in self.node_items and n2 in self.node_items:
                edge_item = EdgeItem(self.node_items[n1], self.node_items[n2])
                self.scene.addItem(edge_item)
                self.edge_items[(n1, n2)] = edge_item

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
        
        node_group.setLayout(node_layout)
        layout.addWidget(node_group)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(150)
        layout.addWidget(QLabel("Sonuclar:"))
        layout.addWidget(self.result_text)
        
        layout.addStretch()
        self.setLayout(layout)
        self.setFixedWidth(200)
    
    def add_node(self):
        try:
            node_id = int(self.node_id_input.text())
            if self.parent_window.graph.add_node(node_id):
                self.parent_window.canvas.draw_graph()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Gecersiz ID!")

class MainWindow(QMainWindow):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.setWindowTitle("Sosyal Ag Analizi")
        self.setGeometry(100, 100, 800, 600)
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
