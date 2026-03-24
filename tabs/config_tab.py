import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from theme import C, hover
from config import save_config


def build(parent, app):
    outer = tk.Frame(parent, bg=C["bg"])

    tk.Label(outer, text=app._("cfg_title"),
             bg=C["bg"], fg=C["fg"],
             font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=28, pady=(24, 4))
    tk.Label(outer, text=app._("cfg_subtitle"),
             bg=C["bg"], fg=C["fg2"],
             font=("Segoe UI", 10)).pack(anchor="w", padx=28, pady=(0, 16))
    tk.Frame(outer, bg=C["divider"], height=1).pack(fill="x", padx=28)

    canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
    sb     = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner  = tk.Frame(canvas, bg=C["bg"])
    inner.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True, padx=(28, 0))
    sb.pack(side="right", fill="y", padx=(0, 8))
    canvas.bind_all("<MouseWheel>",
                    lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    app._cfg_vars = {}

    def section(title, subtitle=""):
        tk.Frame(inner, bg=C["bg"], height=20).pack()
        row = tk.Frame(inner, bg=C["bg"])
        row.pack(fill="x", pady=(0, 4))
        tk.Label(row, text=title, bg=C["bg"], fg=C["fg"],
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        if subtitle:
            tk.Label(row, text=f"  {subtitle}", bg=C["bg"], fg=C["fg3"],
                     font=("Segoe UI", 9)).pack(side="left")
        tk.Frame(inner, bg=C["divider"], height=1).pack(fill="x", pady=(0, 10))

    def field(label, key, hint="", browse_dir=False, browse_file=False):
        row = tk.Frame(inner, bg=C["bg"])
        row.pack(fill="x", pady=8)
        left = tk.Frame(row, bg=C["bg"], width=200)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        tk.Label(left, text=label, bg=C["bg"], fg=C["fg"],
                 font=("Segoe UI", 10), anchor="w").pack(anchor="w")
        if hint:
            tk.Label(left, text=hint, bg=C["bg"], fg=C["fg3"],
                     font=("Segoe UI", 8), anchor="w").pack(anchor="w")
        right = tk.Frame(row, bg=C["bg"])
        right.pack(side="left", fill="x", expand=True, padx=(12, 0))
        var = tk.StringVar(value=str(app._cfg.get(key, "")))
        app._cfg_vars[key] = var
        ent = tk.Entry(right, textvariable=var,
                       bg=C["input_bg"], fg=C["fg"],
                       insertbackground=C["fg"],
                       font=("Segoe UI", 10), bd=0, relief="flat",
                       highlightthickness=1,
                       highlightbackground=C["divider"],
                       highlightcolor=C["blue"])
        ent.pack(side="left", fill="x", expand=True, ipady=8)
        if browse_dir or browse_file:
            def do_browse(v=var, d=browse_dir):
                if d:
                    path = filedialog.askdirectory(initialdir=v.get() or os.path.expanduser("~"))
                else:
                    path = filedialog.askopenfilename(filetypes=[("Ejecutable","*.exe *")])
                if path:
                    v.set(path)
            b = tk.Button(right, text=app._("cfg_browse"),
                          bg=C["card"], fg=C["fg2"],
                          font=("Segoe UI", 9), bd=0,
                          padx=8, pady=8, cursor="hand2", relief="flat",
                          activebackground=C["card_hover"], command=do_browse)
            b.pack(side="left", padx=(8, 0))
            hover(b, C["card"], C["card_hover"])

    # Secciones
    section(app._("cfg_sec_account"), app._("cfg_sec_account_s"))
    field(app._("cfg_username"), "username", app._("cfg_username_h"))
    tk.Label(inner, text=app._("cfg_offline_warn"),
             bg=C["bg"], fg=C["fg3"],
             font=("Segoe UI", 8)).pack(anchor="w")

    section(app._("cfg_sec_java"))
    field(app._("cfg_rammin"), "ram_min", app._("cfg_rammin_h"))
    field(app._("cfg_rammax"), "ram_max", app._("cfg_rammax_h"))
    field(app._("cfg_java"),   "java_path", app._("cfg_java_h"), browse_file=True)

    section(app._("cfg_sec_paths"))
    field(app._("cfg_gamedir"), "game_dir", app._("cfg_gamedir_h"), browse_dir=True)

    section(app._("cfg_sec_versions"))
    app._cfg_rel  = tk.BooleanVar(value=app._cfg["show_release"])
    app._cfg_snap = tk.BooleanVar(value=app._cfg["show_snapshot"])
    app._cfg_bet  = tk.BooleanVar(value=app._cfg["show_beta"])
    app._cfg_alp  = tk.BooleanVar(value=app._cfg["show_alpha"])

    for var, lbl_key, sub_key, color in [
        (app._cfg_rel,  "cfg_show_rel",  "cfg_show_rel_s",  C["release"]),
        (app._cfg_snap, "cfg_show_snap", "cfg_show_snap_s", C["snapshot"]),
        (app._cfg_bet,  "cfg_show_beta", "cfg_show_beta_s", C["beta"]),
        (app._cfg_alp,  "cfg_show_alph", "cfg_show_alph_s", C["alpha"]),
    ]:
        _toggle_row(inner, app, var, app._(lbl_key), app._(sub_key), color)

    # Selector de idioma
    section(app._("cfg_sec_lang"))
    lang_row = tk.Frame(inner, bg=C["bg"])
    lang_row.pack(fill="x", pady=8)

    app._lang_var = tk.StringVar(value=app._cfg.get("language", "es"))

    for code, label, flag in [("es", "Espanol", "ES"), ("en", "English", "EN")]:
        is_active = app._cfg.get("language", "es") == code
        btn = tk.Button(
            lang_row, text=f"  {flag}  {label}  ",
            bg=C["green"] if is_active else C["card"],
            fg=C["bg"]    if is_active else C["fg2"],
            font=("Segoe UI", 10, "bold"), bd=0,
            padx=10, pady=8, cursor="hand2", relief="flat",
            activebackground=C["green_hover"],
            activeforeground=C["bg"],
        )
        def select_lang(c=code, b=btn, row=lang_row):
            app._lang_var.set(c)
            for child in row.winfo_children():
                child.configure(bg=C["card"], fg=C["fg2"])
            b.configure(bg=C["green"], fg=C["bg"])
        btn.configure(command=select_lang)
        btn.pack(side="left", padx=(0, 8))

    # Boton guardar
    tk.Frame(inner, bg=C["bg"], height=20).pack()
    save_btn = tk.Button(
        inner, text=app._("cfg_save"),
        bg=C["green"], fg=C["fg"],
        font=("Segoe UI", 11, "bold"),
        bd=0, pady=12, padx=24,
        cursor="hand2", relief="flat",
        activebackground=C["green_hover"],
        command=lambda: _save(app)
    )
    save_btn.pack(anchor="w", pady=(0, 30))
    hover(save_btn, C["green"], C["green_hover"])

    return outer


def _toggle_row(parent, app, var, label, subtitle, color):
    row = tk.Frame(parent, bg=C["card"],
                   highlightbackground=C["divider"], highlightthickness=1)
    row.pack(fill="x", pady=4)
    left = tk.Frame(row, bg=C["card"])
    left.pack(side="left", fill="both", expand=True, padx=14, pady=10)
    tk.Label(left, text="  ", bg=color, width=2).pack(side="left", padx=(0, 10))
    texts = tk.Frame(left, bg=C["card"])
    texts.pack(side="left")
    tk.Label(texts, text=label, bg=C["card"], fg=C["fg"],
             font=("Segoe UI", 10, "bold")).pack(anchor="w")
    tk.Label(texts, text=subtitle, bg=C["card"], fg=C["fg3"],
             font=("Segoe UI", 8)).pack(anchor="w")

    toggle_btn = tk.Button(row, font=("Segoe UI", 9), bd=0,
                           padx=12, pady=4, cursor="hand2", relief="flat")
    toggle_btn.pack(side="right", padx=14)

    def refresh():
        if var.get():
            toggle_btn.configure(text=app._("cfg_activated"),
                                 bg=C["green"], fg=C["bg"],
                                 activebackground=C["green_hover"])
        else:
            toggle_btn.configure(text=app._("cfg_deactivated"),
                                 bg=C["card_hover"], fg=C["fg3"],
                                 activebackground=C["card"])

    toggle_btn.configure(command=lambda: (var.set(not var.get()), refresh()))
    refresh()


def _save(app):
    for key, var in app._cfg_vars.items():
        app._cfg[key] = var.get()
    app._cfg["show_release"]  = app._cfg_rel.get()
    app._cfg["show_snapshot"] = app._cfg_snap.get()
    app._cfg["show_beta"]     = app._cfg_bet.get()
    app._cfg["show_alpha"]    = app._cfg_alp.get()
    app._cfg["language"]      = app._lang_var.get()
    app._flt_release.set(app._cfg_rel.get())
    app._flt_snapshot.set(app._cfg_snap.get())
    app._flt_beta.set(app._cfg_bet.get())
    app._flt_alpha.set(app._cfg_alp.get())
    save_config(app._cfg)
    app._apply_filters()
    messagebox.showinfo(app._("cfg_saved_title"), app._("cfg_saved_msg") +
                        ("\n\n" + app._("cfg_warn_restart")
                         if app._lang_var.get() != app._lang else ""))
