"""
Visual Flow IDE — PyQt6
Antialiasing natif, dark blue theme, panneau latéral style Claude.ai
"""
import sys
from PyQt6.QtWidgets import (
    QApplication
)
from PyQt6.QtGui import (
    QColor, QPalette
)

from impl.theme import (COLORS, qc)
from impl.mainwindow import MainWindow

# ─── Lancement ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Palette sombre globale
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window,      QColor(COLORS["bg_main"]))
    pal.setColor(QPalette.ColorRole.WindowText,  QColor(COLORS["text_pri"]))
    pal.setColor(QPalette.ColorRole.Base,        QColor(COLORS["bg_card"]))
    pal.setColor(QPalette.ColorRole.Text,        QColor(COLORS["text_pri"]))
    pal.setColor(QPalette.ColorRole.Button,      QColor(COLORS["bg_card"]))
    pal.setColor(QPalette.ColorRole.ButtonText,  QColor(COLORS["text_pri"]))
    pal.setColor(QPalette.ColorRole.Highlight,   QColor(COLORS["accent"]))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())
