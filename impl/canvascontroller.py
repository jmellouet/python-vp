class CanvasControllerMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel, QPushButton, QDialog
)

from PyQt6.QtCore import (
    Qt
)

from .node_item import NodeItem
from .theme import (COLORS, qc)

class CanvasController(metaclass=CanvasControllerMeta):
    
    def setMainWindow(self, mainWindow, scene):
        self.mainWindow = mainWindow
        self.scene = scene
    
    def run(self):
        nodes = [i for i in self.scene.items() if isinstance(i, NodeItem)]
        wires = self.scene._wires
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
