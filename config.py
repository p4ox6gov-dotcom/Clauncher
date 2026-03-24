import json, os
import minecraft_launcher_lib

CONFIG_DIR  = os.path.join(os.path.expanduser("~"), ".craftlauncher")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "username":      "Player",
    "ram_min":       "512M",
    "ram_max":       "2G",
    "java_path":     "",
    "game_dir":      minecraft_launcher_lib.utils.get_minecraft_directory(),
    "show_release":  True,
    "show_snapshot": True,
    "show_beta":     True,
    "show_alpha":    True,
    "language":      "es",
}

def load_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                cfg.setdefault(k, v)
            return cfg
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)

def save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
