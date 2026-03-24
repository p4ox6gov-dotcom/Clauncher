# CraftLauncher

Launcher no oficial de **Minecraft Java Edition** hecho en Python con Tkinter.

## Requisitos

- Python 3.10+
- `pip install minecraft-launcher-lib`

## Uso

```bash
python main.py
```

## Estructura

```
CraftLauncher/
├── main.py             # Ventana principal y navegacion
├── config.py           # Carga y guardado de ajustes (~/.craftlauncher/config.json)
├── theme.py            # Colores, estilos y helpers de widgets
├── lang.py             # Traducciones ES / EN
├── launcher.py         # Logica de descarga y lanzamiento de Minecraft
└── tabs/
    ├── play_tab.py     # Pestaña Jugar
    ├── config_tab.py   # Pestaña Configuracion
    └── about_tab.py    # Pestaña Acerca de
```

## Caracteristicas

- Todas las versiones: Release, Snapshot, Beta, Alpha
- Descarga automatica de assets y librerias desde Mojang
- Configuracion de RAM, Java y rutas
- Modo offline (sin cuenta Microsoft)
- Idioma: Espanol / English
- Tema oscuro replica del launcher oficial

## Licencia

MIT — No afiliado con Mojang Studios ni Microsoft Corporation.
