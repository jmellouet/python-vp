from PyQt6.QtWidgets import (
    QGraphicsItem
)
from PyQt6.QtCore import (
    Qt, QRectF
)
from PyQt6.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont, QPainterPath,
    QLinearGradient
)

from .port import Port
from .theme import qc

NODE_WIDTH  = 170
HEADER_HEIGHT   = 34
ROW_HEIGHT   = 26
PAD_V   = 10
RADIUS  = 10

_node_id = 0

class NodeItem(QGraphicsItem):

    def __init__(self, label, inputs, outputs):
        super().__init__()
        global _node_id
        _node_id += 1
        self.nid     = _node_id
        self.label   = label
        self.inputs  = inputs
        self.outputs = outputs
        self._w      = NODE_WIDTH
        self._h      = HEADER_HEIGHT + max(len(inputs), len(outputs), 1) * ROW_HEIGHT + PAD_V
        self._selected = False

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setZValue(2)

        # Polices
        self._fnt_title = QFont("Segoe UI", 9, QFont.Weight.Bold)
        self._fnt_port  = QFont("Segoe UI", 8)

        # Créer les ports
        self.in_ports  = []
        self.out_ports = []
        for i, lbl in enumerate(inputs):
            p = Port(self, i, True, lbl, self)
            p.setPos(0, HEADER_HEIGHT + PAD_V//2 + i * ROW_HEIGHT + ROW_HEIGHT//2)
            self.in_ports.append(p)
        for i, lbl in enumerate(outputs):
            p = Port(self, i, False, lbl, self)
            p.setPos(self._w, HEADER_HEIGHT + PAD_V//2 + i * ROW_HEIGHT + ROW_HEIGHT//2)
            self.out_ports.append(p)

    def boundingRect(self):
        return QRectF(-6, -6, self._w + 12, self._h + 12)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            scene = self.scene()
            if scene:
                scene.update_wires_for(self)
        return super().itemChange(change, value)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self._w, self._h
        r = RADIUS

        # ── Ombre ──
        shadow_path = QPainterPath()
        shadow_path.addRoundedRect(QRectF(5, 6, w, h), r, r)
        painter.fillPath(shadow_path, QBrush(qc("shadow")))

        # ── Corps ──
        body_path = QPainterPath()
        body_path.addRoundedRect(QRectF(0, 0, w, h), r, r)

        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, QColor(qc("node_bg")))
        grad.setColorAt(1.0, QColor(qc("node_bg")))
        painter.fillPath(body_path, QBrush(grad))

        # ── En-tête ──
        showHeader = True

        if (showHeader):
            hdr_path = QPainterPath()
            hdr_path.addRoundedRect(QRectF(0, 0, w, HEADER_HEIGHT), r, r)
            painter.fillPath(hdr_path, QBrush(qc("node_hdr")))

            hdr_path2 = QPainterPath()
            # Remplir en carré en bas pour avoir une coupure nette
            hdr_path2.addRect(QRectF(0, r, w, HEADER_HEIGHT - r + 1))
            painter.fillPath(hdr_path2, QBrush(qc("node_bg")))

        # ── Bordure ──
        sel_color = qc("accent_hi") if self.isSelected() else qc("node_bdr")
        painter.setPen(QPen(sel_color, 1 if self.isSelected() else 0.5))
        painter.drawPath(body_path)

        # ── Trait gauche ──
        showLeftLine = False
       
        if (showLeftLine):
            # ── Trait accent gauche ──
            accent_path = QPainterPath()
            accent_path.addRoundedRect(QRectF(0, 4, 2, h - 8), 1.5, 1.5)
            painter.fillPath(accent_path, QBrush(qc("accent")))
            
        # ── Titre ──
        painter.setFont(self._fnt_title)
        painter.setPen(QPen(qc("text_pri")))
        painter.drawText(QRectF(12, 5, w - 16, HEADER_HEIGHT), Qt.AlignmentFlag.AlignVCenter, self.label)

        # ── Labels des ports ──
        painter.setFont(self._fnt_port)
        painter.setPen(QPen(qc("text_mut")))
        for i, lbl in enumerate(self.inputs):
            y = HEADER_HEIGHT + PAD_V//2 + i * ROW_HEIGHT + ROW_HEIGHT//2
            painter.drawText(QRectF(14, y - 10, w//2 - 10, 20),
                             Qt.AlignmentFlag.AlignVCenter, lbl)
        for i, lbl in enumerate(self.outputs):
            y = HEADER_HEIGHT + PAD_V//2 + i * ROW_HEIGHT + ROW_HEIGHT//2
            painter.drawText(QRectF(w//2, y - 10, w//2 - 14, 20),
                             Qt.AlignmentFlag.AlignVCenter |
                             Qt.AlignmentFlag.AlignRight, lbl)