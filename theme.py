from tkinter import ttk
import tkinter as tk

# Colores exactos del launcher oficial de Minecraft Java (2024)
C = {
    # Fondos principales
    "bg":          "#1C1B22",   # fondo principal oscuro con tinte morado
    "sidebar":     "#100F17",   # sidebar ultra oscuro
    "card":        "#28262F",   # tarjetas y paneles
    "card_hover":  "#35323F",   # hover sobre tarjetas
    "input_bg":    "#1C1B22",   # fondo de campos de texto
    "divider":     "#3A3845",   # separadores y bordes

    # Acentos
    "green":       "#3DB829",   # boton PLAY verde del launcher
    "green_hover": "#45D431",   # hover del boton play
    "green_dark":  "#2E8C1F",   # pressed del boton play
    "blue":        "#1FA3E8",   # acento azul seleccion
    "blue_dark":   "#1580BA",   # azul oscuro

    # Texto
    "fg":          "#FFFFFF",   # texto principal blanco
    "fg2":         "#9E9B9E",   # texto secundario gris
    "fg3":         "#5C5964",   # texto deshabilitado

    # Estados / badges de version
    "release":     "#3DB829",   # verde release
    "snapshot":    "#FFB300",   # ambar snapshot
    "beta":        "#1FA3E8",   # azul beta
    "alpha":       "#A855F7",   # morado alpha

    # Alertas
    "danger":      "#CF6679",   # error / rojo
    "warning":     "#FFB300",   # warning amarillo
}

def apply_styles(root):
    s = ttk.Style(root)
    s.theme_use("default")

    # Barra de progreso verde estilo launcher
    s.configure("MC.Horizontal.TProgressbar",
                troughcolor=C["card"],
                background=C["green"],
                bordercolor=C["card"],
                lightcolor=C["green"],
                darkcolor=C["green_dark"],
                thickness=6)

    # Scrollbar minimalista
    s.configure("MC.Vertical.TScrollbar",
                background=C["card"],
                troughcolor=C["bg"],
                bordercolor=C["bg"],
                arrowcolor=C["fg3"],
                width=8)
    s.map("MC.Vertical.TScrollbar",
          background=[("active", C["card_hover"])])


def make_pill(parent, text, color, font=("Segoe UI", 8, "bold")):
    """Badge/pill coloreado para el tipo de version."""
    lbl = tk.Label(parent, text=f" {text} ",
                   bg=color, fg=C["bg"],
                   font=font,
                   padx=4, pady=1)
    return lbl


def hover(widget, normal_bg, hover_bg, normal_fg=None, hover_fg=None):
    """Efecto hover en cualquier widget."""
    nfg = normal_fg or widget.cget("fg")
    hfg = hover_fg  or nfg
    widget.bind("<Enter>", lambda e: widget.configure(bg=hover_bg, fg=hfg))
    widget.bind("<Leave>", lambda e: widget.configure(bg=normal_bg, fg=nfg))


def rounded_button(parent, text, command, bg=None, fg=None,
                   font=("Segoe UI", 11, "bold"), pady=10, width=0):
    """Boton con estilos modernos (sin bordes)."""
    bg  = bg  or C["green"]
    fg  = fg  or C["fg"]
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, font=font,
        bd=0, pady=pady, cursor="hand2",
        activebackground=C["green_hover"],
        activeforeground=C["fg"],
        relief="flat",
        width=width
    )
    hover(btn, bg, C["green_hover"] if bg == C["green"] else C["card_hover"])
    return btn


def entry_field(parent, textvariable, width=None):
    """Campo de texto con estilo del launcher."""
    kw = dict(
        textvariable=textvariable,
        bg=C["input_bg"], fg=C["fg"],
        insertbackground=C["fg"],
        font=("Segoe UI", 10),
        bd=0, relief="flat",
        highlightthickness=1,
        highlightbackground=C["divider"],
        highlightcolor=C["blue"],
    )
    if width:
        kw["width"] = width
    return tk.Entry(parent, **kw)


def section_label(parent, text):
    """Etiqueta de seccion con estilo."""
    return tk.Label(parent, text=text.upper(),
                    bg=C["bg"], fg=C["fg3"],
                    font=("Segoe UI", 8, "bold"),
                    padx=0, pady=0)


def divider(parent):
    """Linea divisora."""
    return tk.Frame(parent, bg=C["divider"], height=1)
