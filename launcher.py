import threading, subprocess, os
import minecraft_launcher_lib
from config import save_config

def launch_version(app, version_id):
    if app._launching:
        return
    app._launching = True
    app._launch_btn.configure(state="disabled", text="Preparando...", bg="#21262d")
    app._prog_var.set(0)

    def worker():
        try:
            from config import load_config
            cfg = app._cfg
            game_dir = cfg.get("game_dir") or minecraft_launcher_lib.utils.get_minecraft_directory()
            os.makedirs(game_dir, exist_ok=True)

            def _st(t):
                app.after(0, lambda: app._prog_label.set(t))
                app.after(0, lambda: app._status_var.set(t))

            def _prog(v):
                app.after(0, lambda: app._prog_var.set(v))

            def _max(v):
                app.after(0, lambda: app._progress.configure(maximum=max(int(v), 1)))

            callbacks = {"setStatus": _st, "setProgress": _prog, "setMax": _max}

            _st(f"Instalando {version_id}...")
            minecraft_launcher_lib.install.install_minecraft_version(version_id, game_dir, callbacks)

            username  = (cfg.get("username") or "Player").strip()
            ram_min   = (cfg.get("ram_min")  or "512M").strip()
            ram_max   = (cfg.get("ram_max")  or "2G").strip()
            java_path = (cfg.get("java_path") or "").strip()

            options = {
                "username":     username,
                "uuid":         "",
                "token":        "",
                "jvmArguments": [
                    f"-Xms{ram_min}", f"-Xmx{ram_max}",
                    "-XX:+UnlockExperimentalVMOptions",
                    "-XX:+UseG1GC",
                    "-XX:G1NewSizePercent=20",
                    "-XX:G1ReservePercent=20",
                    "-XX:MaxGCPauseMillis=50",
                    "-XX:G1HeapRegionSize=32M",
                ],
            }
            if java_path:
                options["executablePath"] = java_path

            cmd = minecraft_launcher_lib.command.get_minecraft_command(version_id, game_dir, options)
            _st(f"Minecraft {version_id} en ejecucion")
            app.after(0, lambda: _reset_btn(app))
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        except Exception as exc:
            msg = str(exc)
            from tkinter import messagebox
            app.after(0, lambda: messagebox.showerror("Error al lanzar", f"Error con {version_id}:\n\n{msg}"))
            app.after(0, lambda: app._status_var.set(f"Error: {msg[:60]}"))
            app.after(0, lambda: _reset_btn(app))

    threading.Thread(target=worker, daemon=True).start()

def _reset_btn(app):
    app._launching = False
    app._launch_btn.configure(state="normal", text="LANZAR MINECRAFT", bg="#238636")
