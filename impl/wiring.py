
from PyQt6.QtWidgets import (
   QGraphicsPathItem
)
from PyQt6.QtCore import (
    Qt, QPointF
)
from PyQt6.QtGui import (
    QPen, QPainterPath,
)

from .port import Port
from .theme import qc

# ─── Fil de connexion ─────────────────────────────────────────────────────────
class WireItem(QGraphicsPathItem):
    def __init__(self, src_port: Port, dst_port: Port):
        super().__init__()
        self.src_port = src_port
        self.dst_port = dst_port
        self.lineWidth = 1.5
        self.hoveredLineWidth = 2.0
        self._hovered = False
        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        pen = QPen(qc("wire"), self.lineWidth, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        self.setPen(pen)
        self.update_path()

    def update_path(self):
        p1 = self.src_port.center_scene()
        p2 = self.dst_port.center_scene()
        path = QPainterPath(p1)
        dx   = abs(p2.x() - p1.x()) * 0.5
        path.cubicTo(p1.x() + dx, p1.y(),
                     p2.x() - dx, p2.y(),
                     p2.x(),      p2.y())
        self.setPath(path)

    def hoverEnterEvent(self, e):
        self._hovered = True
        p = self.pen()
        p.setColor(qc("wire_hi"))
        p.setWidthF(self.hoveredLineWidth)
        self.setPen(p)
        super().hoverEnterEvent(e)

    def hoverLeaveEvent(self, e):
        self._hovered = False
        p = self.pen()
        p.setColor(qc("wire"))
        p.setWidthF(self.lineWidth)
        self.setPen(p)
        super().hoverLeaveEvent(e)

# ─── Fil temporaire (preview) ─────────────────────────────────────────────────
class PreviewWire(QGraphicsPathItem):
    def __init__(self):
        super().__init__()
        self.setZValue(20)
        pen = QPen(qc("wire_hi"), 2.0, Qt.PenStyle.DashLine,
                   Qt.PenCapStyle.RoundCap)
        pen.setDashPattern([6, 4])
        self.setPen(pen)

    def update_path(self, p1: QPointF, p2: QPointF):
        path = QPainterPath(p1)
        dx   = abs(p2.x() - p1.x()) * 0.5
        path.cubicTo(p1.x() + dx, p1.y(),
                     p2.x() - dx, p2.y(),
                     p2.x(),      p2.y())
        self.setPath(path)