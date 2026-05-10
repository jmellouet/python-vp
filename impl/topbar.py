import sys
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QFrame)
from .theme import (COLORS)

class Topbar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(42)
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS["bg_side"]};
                border-bottom: 1px solid {COLORS["border"]};
            }}
            QLabel {{ background: transparent; }}
        """)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 0, 16, 0)

        title = QLabel("Canvas")
        title.setStyleSheet(f"color: {COLORS['text_pri']}; font-size: 11px; "
                            f"font-weight: bold;")
        lay.addWidget(title)

        hint = QLabel(
            "Double-clic sur catalogue pour ajouter  ·  "
            "Tire d'un port pour connecter  ·  "
            "Double-clic sur nœud pour supprimer  ·  "
            "Molette = zoom  ·  Clic-milieu = pan")
        hint.setStyleSheet(f"color: {COLORS['text_mut']}; font-size: 9px;")
        lay.addWidget(hint, 1)