from PyQt6.QtWidgets import (
    QFrame, QGraphicsView, QGraphicsScene
)

from PyQt6.QtCore import (
    Qt, QPointF
)

from PyQt6.QtGui import (
    QPainter, QPen, QBrush, QCursor,
)

from .node_item import NodeItem
from .wiring import (WireItem, PreviewWire)
from .port import Port
from .theme import qc

# ─── Scène ────────────────────────────────────────────────────────────────────
class FlowScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-5000, -5000, 10000, 10000)
        self._wires: list[WireItem]   = []
        self._wire_src: Port | None   = None
        self._preview: PreviewWire | None = None

    # ── API publique ─────────────────────────────────────────────────────────
    def add_node(self, label, inputs, outputs, x=0, y=0) -> NodeItem:
        node = NodeItem(label, inputs, outputs)
        node.setPos(x, y)
        self.addItem(node)
        return node

    def update_wires_for(self, node: NodeItem):
        for w in self._wires:
            if w.src_port.node is node or w.dst_port.node is node:
                w.update_path()

    def remove_node(self, node: NodeItem):
        dead = [w for w in self._wires
                if w.src_port.node is node or w.dst_port.node is node]
        for w in dead:
            self.removeItem(w)
            self._wires.remove(w)
        self.removeItem(node)

    # ── Gestion des fils ─────────────────────────────────────────────────────
    def start_wire(self, port: Port):
        self._wire_src = port
        self._preview  = PreviewWire()
        self.addItem(self._preview)
        p = port.center_scene()
        self._preview.update_path(p, p)

    def mouseMoveEvent(self, e):
        if self._preview and self._wire_src:
            p1 = self._wire_src.center_scene()
            self._preview.update_path(p1, e.scenePos())
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if self._preview:
            self.removeItem(self._preview)
            self._preview = None
            # Cherche un port cible sous le curseur
            for item in self.items(e.scenePos()):
                if isinstance(item, Port) and item is not self._wire_src:
                    self._try_connect(self._wire_src, item)
                    break
            self._wire_src = None
        super().mouseReleaseEvent(e)

    def _try_connect(self, a: Port, b: Port):
        # Règle : output → input
        if a.is_input and not b.is_input:
            src, dst = b, a
        elif not a.is_input and b.is_input:
            src, dst = a, b
        else:
            return
        # Evite les doublons
        for w in self._wires:
            if w.src_port is src and w.dst_port is dst:
                return
        wire = WireItem(src, dst)
        self.addItem(wire)
        self._wires.append(wire)

    # ── Double-clic → supprime nœud ──────────────────────────────────────────
    def mouseDoubleClickEvent(self, e):
        for item in self.items(e.scenePos()):
            if isinstance(item, NodeItem):
                self.remove_node(item)
                return
        super().mouseDoubleClickEvent(e)

# ─── Vue ──────────────────────────────────────────────────────────────────────
class FlowView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setBackgroundBrush(QBrush(qc("bg_canvas")))
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self._pan_start = None
        self._zoom = 1.0

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        step = 28
        pen  = QPen(qc("grid_dot"), 0)
        pen.setCosmetic(True)
        painter.setPen(pen)
        l = int(rect.left())  - int(rect.left())  % step
        t = int(rect.top())   - int(rect.top())   % step
        x = l
        while x < rect.right():
            y = t
            while y < rect.bottom():
                painter.drawPoint(QPointF(x, y))
                y += step
            x += step

    def wheelEvent(self, e):
        factor = 1.12 if e.angleDelta().y() > 0 else 1 / 1.12
        self._zoom *= factor
        self._zoom  = max(0.2, min(self._zoom, 4.0))
        self.scale(factor, factor)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.MiddleButton:
            self._pan_start = e.position().toPoint()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
        else:
            super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self._pan_start:
            delta = e.position().toPoint() - self._pan_start
            self._pan_start = e.position().toPoint()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.MiddleButton:
            self._pan_start = None
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            super().mouseReleaseEvent(e)