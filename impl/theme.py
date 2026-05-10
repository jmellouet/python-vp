from PyQt6.QtGui import QColor

COLORS = {
    "bg_main":    "#0a0a0a",
    "bg_side":    "#0f0f0f",
    "bg_canvas":  "#080808",
    "bg_card":    "#141414",
    "bg_card_h":  "#1e1e1e",
    "accent":     "#491515",
    "accent_dim": "#9b2c2c",
    "accent_hi":  "#ffffff",
    "text_pri":   "#e2e8f0",
    "text_mut":   "#838282",
    "text_acc":   "#beb8b8",
    "border":     "#2a2a2a",
    "node_bg":    "#111111",
    "node_hdr":   "#6bbdd1",
    "node_bdr":   "#6bbdd1",
    "port_in":    "#4C7C56",
    "port_out":   "#c56565",
    "wire":       "#a29ea8",
    "wire_hi":    "#d9d8db",
    "grid_dot":   "#5E5E5E",
    "shadow":     "#000000",
}

# ─── Palette ─────────────────────────────────────────────────────────────────
# COLORS = {
#     "bg_main":    "#0d1117",
#     "bg_side":    "#0f1923",
#     "bg_canvas":  "#0a0b0cff",
#     "bg_card":    "#131e2e",
#     "bg_card_h":  "#1a2a3e",
#     "accent":     "#3b82f6",
#     "accent_dim": "#1d4ed8",
#     "accent_hi":  "#60a5fa",
#     "text_pri":   "#e2e8f0",
#     "text_mut":   "#4a6080",
#     "text_acc":   "#93c5fd",
#     "border":     "#1e3a5f",
#     "node_bg":    "#111827",
#     "node_hdr":   "#0f1f38",
#     "node_bdr":   "#1e3a5f",
#     "port_in":    "#22c55e",
#     "port_out":   "#f59e0b",
#     "wire":       "#3b82f6",
#     "wire_hi":    "#60a5fa",
#     "grid_dot":   "#0f1e30",
#     "shadow":     "#050a12",
# }

def qc(key): return QColor(COLORS[key])