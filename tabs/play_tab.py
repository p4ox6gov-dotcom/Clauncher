import tkinter as tk
from tkinter import ttk, messagebox
import threading
import minecraft_launcher_lib
from theme import C, hover
from launcher import launch_version


def build(parent, app):
    frame = tk.Frame(parent, bg=C["bg"])

    header = tk.Frame(frame, bg=C["bg"])
    header.pack(fill="x", padx=28, pady=(24, 0))
    tk.Label(header, text=app._("play_title"),
             bg=C["bg"], fg=C["fg"],
             font=("Segoe UI", 15, "bold")).pack(side="left")

    reload_btn = tk.Button(header, text=app._("play_reload"),
                           bg=C["card"], fg=C["fg2"],
                           font=("Segoe UI", 9), bd=0, padx=10, pady=6,
                           cursor="hand2", relief="flat",
                           activebackground=C["card_hover"],
                           activeforeground=C["fg"],
                           command=lambda: load_versions(app))
    reload_btn.pack(side="right")
    hover(reload_btn, C["card"], C["card_hover"])

    filter_bar = tk.Frame(frame, bg=C["bg"])
    filter_bar.pack(fill="x", padx=28, pady=(14, 0))
    tk.Label(filter_bar, text=app._("play_show"),
             bg=C["bg"], fg=C["fg3"],
             font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 12))

    app._flt_release  = tk.BooleanVar(value=app._cfg["show_release"])
    app._flt_snapshot = tk.BooleanVar(value=app._cfg["show_snapshot"])
    app._flt_beta     = tk.BooleanVar(value=app._cfg["show_beta"])
    app._flt_alpha    = tk.BooleanVar(value=app._cfg["show_alpha"])

    for var, str_key, color in [
        (app._flt_release,  "play_release",  C["release"]),
        (app._flt_snapshot, "play_snapshot", C["snapshot"]),
        (app._flt_beta,     "play_beta",     C["beta"]),
        (app._flt_alpha,    "play_alpha",    C["alpha"]),
    ]:
        _pill_checkbox(filter_bar, app._(str_key), var, color, app._apply_filters)

    list_wrap = tk.Frame(frame, bg=C["card"],
                         highlightbackground=C["divider"], highlightthickness=1)
    list_wrap.pack(fill="both", expand=True, padx=28, pady=12)

    try:
        sb = ttk.Scrollbar(list_wrap, style="MC.Vertical.TScrollbar")
    except Exception:
        sb = ttk.Scrollbar(list_wrap)
    sb.pack(side="right", fill="y")

    app._version_lb = tk.Listbox(
        list_wrap,
        bg=C["card"], fg=C["fg"],
        selectbackground=C["blue_dark"],
        selectforeground=C["fg"],
        font=("Consolas", 10),
        bd=0, highlightthickness=0,
        activestyle="none",
        yscrollcommand=sb.set,
        selectmode="single",
    )
    app._version_lb.pack(fill="both", expand=True, padx=2, pady=2)
    sb.config(command=app._version_lb.yview)
    app._version_lb.bind("<Double-Button-1>", lambda e: _do_launch(app))

    footer = tk.Frame(frame, bg=C["bg"])
    footer.pack(fill="x", padx=28, pady=(0, 20))

    info_col = tk.Frame(footer, bg=C["bg"])
    info_col.pack(side="left", fill="x", expand=True)

    app._prog_label = tk.StringVar(value="")
    tk.Label(info_col, textvariable=app._prog_label,
             bg=C["bg"], fg=C["fg2"],
             font=("Segoe UI", 9)).pack(anchor="w")

    app._prog_var = tk.DoubleVar(value=0)
    try:
        app._progress = ttk.Progressbar(info_col, variable=app._prog_var,
                                         maximum=100,
                                         style="MC.Horizontal.TProgressbar",
                                         length=300)
    except Exception:
        app._progress = ttk.Progressbar(info_col, variable=app._prog_var,
                                         maximum=100, length=300)
    app._progress.pack(anchor="w", pady=(4, 0))

    app._launch_btn = tk.Button(
        footer, text=app._("play_btn"),
        bg=C["green"], fg=C["fg"],
        font=("Segoe UI", 13, "bold"),
        bd=0, padx=32, pady=12,
        cursor="hand2", relief="flat",
        activebackground=C["green_hover"],
        activeforeground=C["fg"],
        command=lambda: _do_launch(app)
    )
    app._launch_btn.pack(side="right", padx=(16, 0))
    hover(app._launch_btn, C["green"], C["green_hover"])

    return frame


def _pill_checkbox(parent, text, var, color, command):
    container = tk.Frame(parent, bg=C["bg"])
    container.pack(side="left", padx=4)
    lbl = tk.Label(container, text=f"  {text}  ",
                   font=("Segoe UI", 9, "bold"),
                   padx=2, pady=4, cursor="hand2",
                   bd=1, relief="solid")
    lbl.pack()
    container._label = lbl
    container._var   = var
    container._color = color
    _refresh(container, var, color)
    def toggle():
        var.set(not var.get())
        _refresh(container, var, color)
        command()
    lbl.bind("<Button-1>", lambda e: toggle())


def _refresh(container, var, color):
    lbl = container._label
    if var.get():
        lbl.configure(bg=color, fg=C["bg"], highlightbackground=color)
    else:
        lbl.configure(bg=C["card"], fg=C["fg3"], highlightbackground=C["divider"])


def _do_launch(app):
    sel = app._version_lb.curselection()
    if not sel:
        messagebox.showwarning(app._("play_warn_title"), app._("play_warn_msg"))
        return
    line  = app._version_lb.get(sel[0]).strip()
    parts = line.split()
    if len(parts) >= 2:
        launch_version(app, parts[-1])


def load_versions(app):
    app._status_var.set(app._("play_connecting"))
    app._version_lb.delete(0, "end")
    app._version_lb.insert("end", app._("play_loading"))

    def worker():
        try:
            app._versions = minecraft_launcher_lib.utils.get_version_list()
            app.after(0, app._apply_filters)
            app.after(0, lambda: app._status_var.set(
                app._("play_loaded", n=len(app._versions))))
        except Exception as exc:
            from tkinter import messagebox
            app.after(0, lambda: messagebox.showerror(
                app._("err_net_title"), str(exc)))
            app.after(0, lambda: app._status_var.set("Error"))

    threading.Thread(target=worker, daemon=True).start()
