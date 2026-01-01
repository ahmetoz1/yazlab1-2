from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QGroupBox, QMessageBox, QFileDialog, QInputDialog,
                             QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
                             QGraphicsLineItem, QGraphicsTextItem, QStatusBar,
                             QMenuBar, QAction, QSplitter, QDialog, QFormLayout,
                             QDialogButtonBox, QDoubleSpinBox, QSpinBox)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
import math
import random
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
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)
        
        self.label = QGraphicsTextItem(str(node_id), self)
        self.label.setDefaultTextColor(Qt.white)
        self.label.setFont(QFont('Arial', 10, QFont.Bold))
        self.label.setPos(-8, -10)
        
        self.selected_for_edge = False
    
    def set_color(self, color):
        self.setBrush(QBrush(QColor(color)))
    
    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionHasChanged and self.canvas:
            self.canvas.update_edges()
        return super().itemChange(change, value)
    
    def set_selected_for_edge(self, selected):
        self.selected_for_edge = selected
        if selected:
            self.setPen(QPen(QColor('#FFD93D'), 4))
        else:
            self.setPen(QPen(Qt.white, 2))

class EdgeItem(QGraphicsLineItem):
    def __init__(self, node1_item, node2_item, weight=0):
        super().__init__()
        self.node1 = node1_item
        self.node2 = node2_item
        self.weight = weight
        self.setPen(QPen(QColor('#6c757d'), 2))
        
        self.weight_label = QGraphicsTextItem(f"{weight:.2f}")
        self.weight_label.setDefaultTextColor(QColor('#adb5bd'))
        self.weight_label.setFont(QFont('Arial', 8))
        self.update_position()
    
    def update_position(self):
        p1 = self.node1.scenePos()
        p2 = self.node2.scenePos()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
        mid_x = (p1.x() + p2.x()) / 2 - 15
        mid_y = (p1.y() + p2.y()) / 2 - 10
        self.weight_label.setPos(mid_x, mid_y)

class GraphCanvas(QGraphicsView):
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.node_items = {}
        self.edge_items = {}
        self.setRenderHint(True)
        self.setBackgroundBrush(QBrush(QColor('#1a1a2e')))
        self.parent_window = parent
        self.selected_nodes = []
    
    def draw_graph(self):
        old_positions = {}
        for node_id, item in self.node_items.items():
            old_positions[node_id] = item.scenePos()
        
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
            if node_id in old_positions:
                x = old_positions[node_id].x()
                y = old_positions[node_id].y()
            else:
                angle = 2 * math.pi * i / n
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
            
            node_item = NodeItem(node_id, x, y, canvas=self)
            self.scene.addItem(node_item)
            self.node_items[node_id] = node_item
        
        for edge_key in self.graph.edges:
            n1, n2 = edge_key
            if n1 in self.node_items and n2 in self.node_items:
                edge = self.graph.get_edge(n1, n2)
                weight = edge.get_weight() if edge else 0
                edge_item = EdgeItem(self.node_items[n1], self.node_items[n2], weight)
                self.scene.addItem(edge_item)
                self.scene.addItem(edge_item.weight_label)
                self.edge_items[edge_key] = edge_item
                edge_item.setZValue(-1)
    
    def update_edges(self):
        for edge_item in self.edge_items.values():
            edge_item.update_position()
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        item = self.itemAt(event.pos())
        if isinstance(item, NodeItem):
            self.toggle_node_selection(item.node_id)
        elif isinstance(item, QGraphicsTextItem) and isinstance(item.parentItem(), NodeItem):
            self.toggle_node_selection(item.parentItem().node_id)
    
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        item = self.itemAt(event.pos())
        node_id = None
        if isinstance(item, NodeItem):
            node_id = item.node_id
        elif isinstance(item, QGraphicsTextItem) and isinstance(item.parentItem(), NodeItem):
            node_id = item.parentItem().node_id
        
        if node_id is not None:
            self.show_node_info(node_id)
    
    def show_node_info(self, node_id):
        node = self.graph.get_node(node_id)
        if not node:
            return
        
        neighbors = self.graph.get_neighbors(node_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Dugum {node_id} Bilgisi")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        
        info_label = QLabel()
        info_label.setText(
            f"Dugum ID: {node_id}\n"
            f"Etiket: {node.label}\n"
            f"Aktiflik: {node.aktiflik}\n"
            f"Etkilesim: {node.etkilesim}\n"
            f"Baglanti Sayisi: {len(neighbors)}\n"
            f"Komsular: {neighbors}"
        )
        layout.addWidget(info_label)
        
        btn_edit = QPushButton("Duzenle")
        btn_edit.clicked.connect(lambda: self.open_edit_dialog(node_id, dialog))
        layout.addWidget(btn_edit)
        
        btn_close = QPushButton("Kapat")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def open_edit_dialog(self, node_id, parent_dialog):
        parent_dialog.close()
        self.edit_node(node_id)
    
    def edit_node(self, node_id):
        node = self.graph.get_node(node_id)
        if not node:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Dugum {node_id} Duzenle")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QFormLayout()
        
        etiket_input = QLineEdit(node.label)
        layout.addRow("Etiket:", etiket_input)
        
        aktiflik_input = QDoubleSpinBox()
        aktiflik_input.setRange(0, 1)
        aktiflik_input.setDecimals(2)
        aktiflik_input.setSingleStep(0.1)
        aktiflik_input.setValue(node.aktiflik)
        layout.addRow("Aktiflik:", aktiflik_input)
        
        etkilesim_input = QSpinBox()
        etkilesim_input.setRange(0, 1000)
        etkilesim_input.setValue(node.etkilesim)
        layout.addRow("Etkilesim:", etkilesim_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            node.label = etiket_input.text()
            node.aktiflik = aktiflik_input.value()
            node.etkilesim = etkilesim_input.value()
            self.graph.update_all_weights()
            self.draw_graph()
            if self.parent_window:
                self.parent_window.statusBar().showMessage(f"Dugum {node_id} guncellendi")
    
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
    
    def clear_selection(self):
        for node_id in self.selected_nodes:
            if node_id in self.node_items:
                self.node_items[node_id].set_selected_for_edge(False)
        self.selected_nodes.clear()
    
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
        
        self.aktiflik_input = QLineEdit()
        self.aktiflik_input.setPlaceholderText("Aktiflik (0-1)")
        node_layout.addWidget(self.aktiflik_input)
        
        self.etkilesim_input = QLineEdit()
        self.etkilesim_input.setPlaceholderText("Etkilesim")
        node_layout.addWidget(self.etkilesim_input)
        
        self.etiket_input = QLineEdit()
        self.etiket_input.setPlaceholderText("Etiket (opsiyonel)")
        node_layout.addWidget(self.etiket_input)
        
        btn_add_node = QPushButton("Dugum Ekle")
        btn_add_node.clicked.connect(self.add_node)
        node_layout.addWidget(btn_add_node)
        
        btn_random_node = QPushButton("Rastgele Ekle")
        btn_random_node.clicked.connect(self.add_random_node)
        node_layout.addWidget(btn_random_node)
        
        btn_remove_node = QPushButton("Dugum Sil")
        btn_remove_node.clicked.connect(self.remove_node)
        node_layout.addWidget(btn_remove_node)
        
        btn_list_nodes = QPushButton("Dugum Listesi")
        btn_list_nodes.clicked.connect(self.show_node_list)
        node_layout.addWidget(btn_list_nodes)
        
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
    
    def add_node(self):
        id_text = self.node_id_input.text()
        if not id_text:
            QMessageBox.warning(self, "Hata", "Dugum ID bos olamaz!")
            return
        
        try:
            node_id = int(id_text)
        except ValueError:
            QMessageBox.warning(self, "Hata", "Dugum ID sayi olmali!")
            return
        
        try:
            aktiflik = float(self.aktiflik_input.text() or "0.5")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Aktiflik sayi olmali (ornek: 0.5)!")
            return
        
        if aktiflik < 0 or aktiflik > 1:
            QMessageBox.warning(self, "Hata", "Aktiflik 0-1 arasi olmali!")
            return
        
        try:
            etkilesim = int(self.etkilesim_input.text() or "0")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Etkilesim tam sayi olmali!")
            return
        
        etiket = self.etiket_input.text() or None
        
        if self.parent_window.graph.add_node(node_id, aktiflik, etkilesim, label=etiket):
            self.parent_window.canvas.draw_graph()
            self.parent_window.statusBar().showMessage(f"Dugum {node_id} eklendi")
        else:
            QMessageBox.warning(self, "Hata", f"Dugum {node_id} zaten var!")
    
    def add_random_node(self):
        existing_ids = list(self.parent_window.graph.nodes.keys())
        new_id = max(existing_ids) + 1 if existing_ids else 1
        aktiflik = round(random.uniform(0.1, 1.0), 2)
        etkilesim = random.randint(1, 20)
        
        self.parent_window.graph.add_node(new_id, aktiflik, etkilesim)
        self.parent_window.canvas.draw_graph()
        self.parent_window.statusBar().showMessage(f"Rastgele dugum {new_id} eklendi (a={aktiflik}, e={etkilesim})")
    
    def update_edge_inputs(self):
        selected = self.parent_window.canvas.selected_nodes
        if len(selected) >= 1:
            self.edge_n1_input.setText(str(selected[0]))
        if len(selected) >= 2:
            self.edge_n2_input.setText(str(selected[1]))
    
    def show_node_list(self):
        nodes = self.parent_window.graph.get_all_nodes()
        if not nodes:
            QMessageBox.information(self, "Dugum Listesi", "Hic dugum yok!")
            return
        
        text = f"{'ID':<5}{'Etiket':<15}{'Aktiflik':<10}{'Etkilesim':<10}\n"
        text += "-" * 40 + "\n"
        for node in nodes:
            text += f"{node.node_id:<5}{node.label:<15}{node.aktiflik:<10}{node.etkilesim:<10}\n"
        
        text += "\nDuzenleme icin dugum ID girin:"
        
        reply = QMessageBox.question(self, f"Dugum Listesi ({len(nodes)} dugum)", 
                                     text + "\n\nDuzenlemek ister misiniz?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            node_id, ok = QInputDialog.getInt(self, "Duzenle", "Dugum ID:")
            if ok and node_id in self.parent_window.graph.nodes:
                self.parent_window.canvas.edit_node(node_id)
    
    def remove_node(self):
        try:
            node_id = int(self.node_id_input.text())
            if self.parent_window.graph.remove_node(node_id):
                self.parent_window.canvas.draw_graph()
                self.parent_window.statusBar().showMessage(f"Dugum {node_id} silindi")
            else:
                QMessageBox.warning(self, "Hata", "Dugum bulunamadi!")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Gecersiz ID!")
    
    def add_edge(self):
        try:
            n1 = int(self.edge_n1_input.text())
            n2 = int(self.edge_n2_input.text())
            if self.parent_window.graph.add_edge(n1, n2):
                self.parent_window.canvas.draw_graph()
                self.parent_window.statusBar().showMessage(f"Kenar {n1}-{n2} eklendi")
            else:
                QMessageBox.warning(self, "Hata", "Kenar eklenemedi!")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Gecersiz ID!")
    
    def remove_edge(self):
        try:
            n1 = int(self.edge_n1_input.text())
            n2 = int(self.edge_n2_input.text())
            if self.parent_window.graph.remove_edge(n1, n2):
                self.parent_window.canvas.draw_graph()
                self.parent_window.statusBar().showMessage(f"Kenar {n1}-{n2} silindi")
            else:
                QMessageBox.warning(self, "Hata", "Kenar bulunamadi!")
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
            bfs_colors = ['#FF6B6B', '#FF8E72', '#FFB07A', '#FFD185', '#FFF192']
            for node_id in result['visited']:
                if node_id in self.parent_window.canvas.node_items:
                    level = result['levels'].get(node_id, 0)
                    color_idx = min(level, len(bfs_colors) - 1)
                    self.parent_window.canvas.node_items[node_id].set_color(bfs_colors[color_idx])
    
    def run_dfs(self):
        start, ok = QInputDialog.getInt(self, "DFS", "Baslangic dugum ID:")
        if ok:
            from algorithms.dfs import dfs
            start_time = time.time()
            result = dfs(self.parent_window.graph, start)
            elapsed = (time.time() - start_time) * 1000
            self.result_text.setText(f"DFS Sonucu:\n{result['visited']}\n\nSure: {elapsed:.2f} ms")
            self.parent_window.canvas.reset_colors()
            dfs_colors = ['#2ECC71', '#27AE60', '#1E8449', '#196F3D', '#145A32']
            for node_id in result['visited']:
                if node_id in self.parent_window.canvas.node_items:
                    disc = result['discovery'].get(node_id, 0) - 1
                    color_idx = min(max(disc, 0), len(dfs_colors) - 1)
                    self.parent_window.canvas.node_items[node_id].set_color(dfs_colors[color_idx])
    
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
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()
        self.create_menu()
    
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
    
    def create_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("Dosya")
        
        open_json = QAction("JSON Ac", self)
        open_json.triggered.connect(self.load_json)
        file_menu.addAction(open_json)
        
        save_json = QAction("JSON Kaydet", self)
        save_json.triggered.connect(self.save_json)
        file_menu.addAction(save_json)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Cikis", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def load_json(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "JSON Dosyasi Ac", "", "JSON (*.json)")
        if filepath:
            from data_io import load_json
            positions = load_json(self.graph, filepath)
            self.canvas.draw_graph()
            if positions:
                for node_id, (x, y) in positions.items():
                    if node_id in self.canvas.node_items:
                        self.canvas.node_items[node_id].setPos(x, y)
                self.canvas.update_edges()
            self.statusBar().showMessage(f"Yuklendi: {filepath}")
    
    def save_json(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "JSON Kaydet", "", "JSON (*.json)")
        if filepath:
            from data_io import save_json
            positions = {}
            for node_id, item in self.canvas.node_items.items():
                pos = item.scenePos()
                positions[node_id] = (pos.x(), pos.y())
            save_json(self.graph, filepath, positions)
            self.statusBar().showMessage(f"Kaydedildi: {filepath}")
