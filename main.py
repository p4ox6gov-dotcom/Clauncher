import tkinter as tk
from tkinter import ttk
from config import load_config
from theme import C, apply_styles
import lang as L
import tabs.play_tab   as play_tab
import tabs.config_tab as config_tab
import tabs.about_tab  as about_tab


class CraftLauncher(tk.Tk):

    def __init__(self):
        super().__init__()
        self._cfg  = load_config()
        self._lang = self._cfg.get("language", "es")

        self.title("Minecraft Launcher")
        self.geometry("980x640")
        self.minsize(820, 520)
        self.configure(bg=C["bg"])

        self._versions  = []
        self._launching = False

        apply_styles(self)
        self._build_ui()
        self.after(200, lambda: play_tab.load_versions(self))

    def _(self, key, **kw):
        """Shortcut para traduccion."""
        return L.get(key, self._lang, **kw)

    def _build_ui(self):
        sidebar = tk.Frame(self, bg=C["sidebar"], width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(sidebar, bg=C["sidebar"])
        logo_frame.pack(fill="x", pady=(28, 0))
        icon_c = tk.Canvas(logo_frame, width=36, height=36,
                           bg=C["sidebar"], highlightthickness=0)
        icon_c.pack(side="left", padx=(20, 10))
        icon_c.create_rectangle(0,  0, 36, 36, fill=C["green"],      outline="")
        icon_c.create_rectangle(4,  4, 16, 16, fill=C["green_dark"], outline="")
        icon_c.create_rectangle(20, 4, 32, 16, fill=C["green_dark"], outline="")
        icon_c.create_rectangle(4, 20, 32, 32, fill=C["green_dark"], outline="")

        tf = tk.Frame(logo_frame, bg=C["sidebar"])
        tf.pack(side="left")
        tk.Label(tf, text="Minecraft",
                 bg=C["sidebar"], fg=C["fg"],
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(tf, text=self._("app_subtitle"),
                 bg=C["sidebar"], fg=C["fg2"],
                 font=("Segoe UI", 8)).pack(anchor="w")

        tk.Frame(sidebar, bg=C["divider"], height=1).pack(fill="x", padx=16, pady=20)

        self._nav_btns = {}
        for key, str_key in [("play","nav_play"), ("config","nav_config"), ("about","nav_about")]:
            btn = tk.Button(
                sidebar, text=self._(str_key),
                bg=C["sidebar"], fg=C["fg2"],
                font=("Segoe UI", 11), bd=0,
                pady=13, anchor="w", padx=22,
                cursor="hand2",
                activebackground=C["card"],
                activeforeground=C["fg"],
                relief="flat",
                command=lambda k=key: self._show_tab(k)
            )
            btn.pack(fill="x")
            self._nav_btns[key] = btn

        self._status_var = tk.StringVar(value=self._("status_ready"))
        tk.Frame(sidebar, bg=C["divider"], height=1).pack(
            fill="x", padx=16, side="bottom", pady=(0, 50))
        tk.Label(sidebar, textvariable=self._status_var,
                 bg=C["sidebar"], fg=C["fg3"],
                 font=("Segoe UI", 8), wraplength=200,
                 justify="left").pack(side="bottom", padx=16, pady=(0, 8))

        self._bg_canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0)
        self._bg_canvas.pack(side="left", fill="both", expand=True)
        self._bg_canvas.bind("<Configure>", self._draw_bg)

        self._content = tk.Frame(self._bg_canvas, bg=C["bg"])
        self._bg_canvas.create_window(0, 0, window=self._content,
                                      anchor="nw", tags="content")
        self._bg_canvas.bind("<Configure>",
            lambda e: (self._draw_bg(e),
                       self._bg_canvas.coords("content", 0, 0),
                       self._bg_canvas.itemconfig(
                           "content", width=e.width, height=e.height)))

        self._tabs = {
            "play":   play_tab.build(self._content, self),
            "config": config_tab.build(self._content, self),
            "about":  about_tab.build(self._content, self),
        }
        self._show_tab("play")

    def _draw_bg(self, event=None):
        w = self._bg_canvas.winfo_width()
        h = self._bg_canvas.winfo_height()
        self._bg_canvas.delete("bg_grad")
        steps = 40
        for i in range(steps):
            ratio = i / steps
            r = int(0x1C + (0x14 - 0x1C) * ratio)
            g = int(0x1B + (0x12 - 0x1B) * ratio)
            b = int(0x22 + (0x28 - 0x22) * ratio)
            self._bg_canvas.create_rectangle(
                0, int(h*i/steps), w, int(h*(i+1)/steps)+1,
                fill=f"#{r:02x}{g:02x}{b:02x}", outline="", tags="bg_grad")
        self._bg_canvas.tag_lower("bg_grad")

    def _show_tab(self, name):
        for k, f in self._tabs.items():
            f.place_forget()
        self._tabs[name].place(relx=0, rely=0, relwidth=1, relheight=1)
        for k, b in self._nav_btns.items():
            b.configure(
                bg=C["card"] if k == name else C["sidebar"],
                fg=C["fg"]   if k == name else C["fg2"])

    def _apply_filters(self):
        type_show = {
            "release":   self._flt_release.get(),
            "snapshot":  self._flt_snapshot.get(),
            "old_beta":  self._flt_beta.get(),
            "old_alpha": self._flt_alpha.get(),
        }
        type_meta = {
            "release":   ("Release",  C["release"]),
            "snapshot":  ("Snapshot", C["snapshot"]),
            "old_beta":  ("Beta",     C["beta"]),
            "old_alpha": ("Alpha",    C["alpha"]),
        }
        self._version_lb.delete(0, "end")
        count = 0
        for v in self._versions:
            vtype = v.get("type", "release")
            if not type_show.get(vtype, False):
                continue
            tag, color = type_meta.get(vtype, ("?", C["fg2"]))
            self._version_lb.insert("end", f"  [{tag:<8}]  {v['id']}")
            self._version_lb.itemconfig("end", fg=color)
            count += 1
        if count == 0:
            self._version_lb.insert("end", self._("play_no_results"))
        elif self._version_lb.size() > 0:
            self._version_lb.selection_set(0)
            self._version_lb.see(0)


if __name__ == "__main__":
    CraftLauncher().mainloop()
