from PyQt6.QtWidgets import (QWidget, QVBoxLayout,QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame
)

from PyQt6.QtCore import (
    Qt, pyqtSignal
)

from PyQt6.QtGui import (
    QCursor,
)

from .theme import (COLORS, qc)
from .canvascontroller import CanvasController

# ─── Catalogue ────────────────────────────────────────────────────────────────
CATALOGUE = {
    "Entrée": [
        ("📥 Nombre",    [], ["valeur"]),
        ("📝 Texte",     [], ["texte"]),
        ("🎲 Aléatoire", [], ["valeur"]),
    ],
    "Maths": [
        ("➕ Addition",      ["a", "b"],  ["résultat"]),
        ("✖ Multiplication", ["a", "b"],  ["résultat"]),
        ("📐 Sinus",         ["x"],       ["sin(x)"]),
        ("√ Racine",         ["x"],       ["√x"]),
    ],
    "Logique": [
        ("⚖ Comparaison", ["a", "b"],   ["vrai", "faux"]),
        ("🔀 Condition",   ["condition"],["vrai", "faux"]),
        ("∧ ET",           ["a", "b"],   ["résultat"]),
    ],
    "Sortie": [
        ("🖨 Afficher",  ["valeur"], []),
        ("📊 Graphique", ["données"], []),
        ("💾 Sauvegarder",["données"], []),
    ],
}

# ─── Sidebar ──────────────────────────────────────────────────────────────────
SIDE_CSS = f"""
QWidget#sidebar {{
    background: {COLORS["bg_side"]};
    border-right: 1px solid {COLORS["border"]};
}}
QLabel#logo {{
    color: {COLORS["accent"]};
    font-size: 26px;
    padding-top: 16px;
}}
QLabel#app_name {{
    color: {COLORS["text_pri"]};
    font-size: 13px;
    font-weight: bold;
}}
QLabel#app_sub {{
    color: {COLORS["text_mut"]};
    font-size: 9px;
    padding-bottom: 8px;
}}
QLabel#section_title {{
    color: {COLORS["text_mut"]};
    font-size: 9px;
    font-weight: bold;
    padding: 10px 16px 2px 16px;
}}
QFrame#sep {{
    background: {COLORS["border"]};
    max-height: 1px;
    margin: 0 16px;
}}
QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 4px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS["border"]};
    border-radius: 2px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""

class Sidebar(QWidget):
    node_requested = pyqtSignal(str, list, list)

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(230)
        self.setStyleSheet(SIDE_CSS)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Logo
        logo = QLabel("⬡")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(logo)

        name = QLabel("Visual Flow")
        name.setObjectName("app_name")
        name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(name)

        sub = QLabel("PyQt6 node editor")
        sub.setObjectName("app_sub")
        sub.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(sub)

        sep = QFrame(); sep.setObjectName("sep"); sep.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep)

        # Scroll area pour le catalogue
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner  = QWidget()
        inner.setStyleSheet(f"background: {COLORS['bg_side']};")
        self.sideBarBoxLayout = QVBoxLayout(inner)
        self.sideBarBoxLayout.setContentsMargins(0, 4, 0, 8)
        self.sideBarBoxLayout.setSpacing(0)
        scroll.setWidget(inner)
        root.addWidget(scroll, 1)

        self._populate()

        # Boutons du bas
        sep2 = QFrame(); sep2.setObjectName("sep"); sep2.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep2)
        self._add_btn("🗑  Effacer tout", self._emit_clear)
        self._add_btn("▶  Exécuter",     self._emit_run)

    def _add_btn(self, text, slot):
        btn = QPushButton(text)
        btn.clicked.connect(slot)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS["bg_card"]};
                color: {COLORS["text_acc"]};
                border: none;
                padding: 8px 16px;
                text-align: left;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background: {COLORS["bg_card_h"]};
                color: {COLORS["accent_hi"]};
            }}
        """)
        self.layout().addWidget(btn)

    def _populate(self):
        for category, items in CATALOGUE.items():
            sec = QLabel(category.upper())
            sec.setObjectName("section_title")
            self.sideBarBoxLayout.addWidget(sec)
            for label, inputs, outputs in items:
                card = NodeCard(label, inputs, outputs)
                card.spawn.connect(self.node_requested)
                self.sideBarBoxLayout.addWidget(card)
        self.sideBarBoxLayout.addStretch()

    def _emit_clear(self): 
        self.node_requested.emit("__clear__", [], [])
    def _emit_run(self):  
        self.node_requested.emit("__run__",   [], [])
        CanvasController().run()

    
class NodeCard(QFrame):
    spawn = pyqtSignal(str, list, list)

    def __init__(self, label, inputs, outputs):
        super().__init__()
        self._label   = label
        self._inputs  = inputs
        self._outputs = outputs
        self.setFixedHeight(34)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS["bg_card"]};
                border-radius: 6px;
                margin: 2px 12px;
            }}
            QFrame:hover {{
                background: {COLORS["bg_card_h"]};
                border: 1px solid {COLORS["border"]};
            }}
        """)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 0, 10, 0)
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {COLORS['text_pri']}; font-size: 12px; "
                          f"background: transparent; border: none;")
        lay.addWidget(lbl)

    def mouseDoubleClickEvent(self, e):
        self.spawn.emit(self._label, self._inputs, self._outputs)
        super().mouseDoubleClickEvent(e)
