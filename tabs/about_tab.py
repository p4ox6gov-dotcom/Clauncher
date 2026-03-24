import tkinter as tk
from theme import C

def build(parent, app):
    frame = tk.Frame(parent, bg=C["bg"])
    hero = tk.Frame(frame, bg=C["card"],
                    highlightbackground=C["divider"], highlightthickness=1)
    hero.pack(fill="x", padx=28, pady=(28, 0))
    icon = tk.Canvas(hero, width=64, height=64, bg=C["card"], highlightthickness=0)
    icon.pack(pady=(24, 10))
    icon.create_rectangle(0,  0, 64, 64, fill=C["green"],      outline="")
    icon.create_rectangle(6,  6, 28, 28, fill=C["green_dark"], outline="")
    icon.create_rectangle(36, 6, 58, 28, fill=C["green_dark"], outline="")
    icon.create_rectangle(6, 36, 58, 58, fill=C["green_dark"], outline="")
    tk.Label(hero, text="Minecraft Launcher",
             bg=C["card"], fg=C["fg"],
             font=("Segoe UI", 18, "bold")).pack()
    tk.Label(hero, text=app._("about_subtitle"),
             bg=C["card"], fg=C["fg2"],
             font=("Segoe UI", 10)).pack()
    tk.Label(hero, text=app._("about_version"),
             bg=C["card"], fg=C["fg3"],
             font=("Segoe UI", 9)).pack(pady=(2, 20))

    cards_frame = tk.Frame(frame, bg=C["bg"])
    cards_frame.pack(fill="x", padx=28, pady=20)

    for t_key, d_key in [
        ("about_f1_t","about_f1_d"),
        ("about_f2_t","about_f2_d"),
        ("about_f3_t","about_f3_d"),
        ("about_f4_t","about_f4_d"),
    ]:
        card = tk.Frame(cards_frame, bg=C["card"],
                        highlightbackground=C["divider"], highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=6)
        tk.Frame(card, bg=C["green"], height=3).pack(fill="x")
        tk.Label(card, text=app._(t_key), bg=C["card"], fg=C["fg"],
                 font=("Segoe UI", 10, "bold")).pack(pady=(10, 2))
        tk.Label(card, text=app._(d_key), bg=C["card"], fg=C["fg2"],
                 font=("Segoe UI", 8), justify="center").pack(pady=(0, 10))

    tk.Label(frame, text=app._("about_disclaimer"),
             bg=C["bg"], fg=C["fg3"],
             font=("Segoe UI", 8)).pack(side="bottom", pady=16)
    return frame
