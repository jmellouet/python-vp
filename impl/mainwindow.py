from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
)

from PyQt6.QtCore import (
    Qt, QTimer
)

from .canvas import (FlowScene, FlowView)
from .node_item import NodeItem
from .sidebar import Sidebar
from .topbar import Topbar
from .theme import (COLORS, qc)
from .controller import Controller
from .canvascontroller import CanvasController

# ─── Fenêtre principale ───────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = Controller(self)
        CanvasController().setMainWindow(self)

        self.setWindowTitle("Visual Flow IDE")
        self.resize(1280, 780)

        # Fond global
        self.setStyleSheet(f"QMainWindow {{ background: {COLORS['bg_main']}; }}")

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self._sidebar = Sidebar()
        self._sidebar.node_requested.connect(self._handle_request)
        root.addWidget(self._sidebar)

        # Zone droite
        right = QWidget()
        right.setStyleSheet(f"background: {COLORS['bg_main']};")
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(0)

        self._topbar = Topbar()
        right_lay.addWidget(self._topbar)

        self._scene = FlowScene()
        self._view  = FlowView(self._scene)
        right_lay.addWidget(self._view, 1)

        root.addWidget(right, 1)

        self._spawn_counter = 0
        QTimer.singleShot(100, self._demo_nodes)

    # ── Gestion des demandes de la sidebar ───────────────────────────────────
    def _handle_request(self, label, inputs, outputs):
        if label == "__clear__":
            items = list(self._scene.items())
            for item in items:
                if isinstance(item, NodeItem):
                    self._scene.remove_node(item)
            return
        if label == "__run__":
            # self._show_run_dialog()
            self.controller._show_run_dialog(self._scene)
            return
        # Offset en cascade
        cx = self._view.mapToScene(
            self._view.viewport().rect().center()).x()
        cy = self._view.mapToScene(
            self._view.viewport().rect().center()).y()
        x = cx - 85 + self._spawn_counter * 22
        y = cy - 60 + self._spawn_counter * 14
        self._spawn_counter = (self._spawn_counter + 1) % 8
        self._scene.add_node(label, inputs, outputs, x, y)

    # ── Nœuds de démonstration ───────────────────────────────────────────────
    def _demo_nodes(self):
        n1 = self._scene.add_node("📥 Nombre",    [],       ["valeur"],   -340, -60)
        n2 = self._scene.add_node("📥 Nombre",    [],       ["valeur"],   -340,  80)
        n3 = self._scene.add_node("➕ Addition",   ["a","b"],["résultat"], -100,  10)
        n4 = self._scene.add_node("🖨 Afficher",  ["valeur"],[],            180,  10)
        n5 = self._scene.add_node("⚖ Comparaison",["a","b"],["vrai","faux"],180, 160)

        # Connexions démo
        self._scene._try_connect(n1.out_ports[0], n3.in_ports[0])
        self._scene._try_connect(n2.out_ports[0], n3.in_ports[1])
        self._scene._try_connect(n3.out_ports[0], n4.in_ports[0])
        self._scene._try_connect(n3.out_ports[0], n5.in_ports[0])
        self._scene._try_connect(n2.out_ports[0], n5.in_ports[1])