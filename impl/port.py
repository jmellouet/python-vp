from PyQt6.QtWidgets import (
   QGraphicsEllipseItem
)

from PyQt6.QtCore import (
    Qt, QPointF
)
from PyQt6.QtGui import (
    QPen, QBrush, QCursor,
)

from .theme import qc

PORT_R = 5

class Port(QGraphicsEllipseItem):
    def __init__(self, node, index, is_input, label, parent=None):
        super().__init__(-PORT_R, -PORT_R, PORT_R*2, PORT_R*2, parent)
        self.node     = node
        self.index    = index
        self.is_input = is_input
        self.label    = label
        self._hovered = False

        col = qc("port_in") if is_input else qc("port_out")
        self._col     = col
        self._col_h   = col.lighter(140)
        self.setBrush(QBrush(col))
        self.setPen(QPen(qc("bg_canvas"), 1.5))
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))

    def hoverEnterEvent(self, e):
        self._hovered = True
        self.setBrush(QBrush(self._col_h))
        self.setRect(-PORT_R - 0.5, -PORT_R - 0.5, (PORT_R + 0.5) * 2, (PORT_R + 0.5) * 2)
        super().hoverEnterEvent(e)

    def hoverLeaveEvent(self, e):
        self._hovered = False
        self.setBrush(QBrush(self._col))
        self.setRect(-PORT_R, -PORT_R, PORT_R*2, PORT_R*2)
        super().hoverLeaveEvent(e)

    def center_scene(self):
        return self.mapToScene(QPointF(0, 0))

    # Intercept press pour démarrer un fil — délégué à la vue
    def mousePressEvent(self, e):
        scene = self.scene()
        if scene and hasattr(scene, "start_wire"):
            scene.start_wire(self)
        e.accept()