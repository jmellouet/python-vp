
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel, QPushButton, QDialog
)
from PyQt6.QtCore import (
    Qt
)

from .node_item import NodeItem
from .theme import (COLORS, qc)

# ─── Fenêtre principale ───────────────────────────────────────────────────────
class Controller():
    
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def _show_run_dialog(self, scene):
        nodes = [i for i in scene.items() if isinstance(i, NodeItem)]
        wires = scene._wires
        dlg = QDialog(self.mainWindow)
        dlg.setWindowTitle("Exécution")
        dlg.setFixedSize(320, 160)
        dlg.setStyleSheet(f"""
            QDialog {{ background: {COLORS['bg_main']}; }}
            QLabel  {{ color: {COLORS['text_pri']}; }}
            QPushButton {{
                background: {COLORS['accent']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background: {COLORS['accent_hi']}; }}
        """)
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)
        title = QLabel("▶  Exécution simulée")
        title.setStyleSheet(f"color: {COLORS['accent_hi']}; font-size: 13px; "
                            f"font-weight: bold;")
        lay.addWidget(title)
        info = QLabel(f"{len(nodes)} nœud(s)  ·  {len(wires)} connexion(s)")
        info.setStyleSheet(f"color: {COLORS['text_mut']}; font-size: 10px;")
        lay.addWidget(info)
        btn = QPushButton("Fermer")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        dlg.exec()
