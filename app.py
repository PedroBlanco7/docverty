"""
Docverty — Conversor de documentos a Markdown.
Creado por Pedro Blanco.  Motor: MarkItDown © Microsoft (MIT License).
"""
import os
import sys
import json
import threading
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

APP_NAME    = "Docverty"
APP_VERSION = "1.0"
APP_AUTHOR  = "Pedro Blanco"
APP_ENGINE  = "MarkItDown by Microsoft"
APP_LICENSE = "MIT License"

try:
    import ttkbootstrap as tbs
    from ttkbootstrap.constants import BOTH, X, Y, LEFT, RIGHT, TOP, BOTTOM, YES
except ImportError as e:
    import tkinter.messagebox as mb
    mb.showerror("Dependencia faltante", f"ttkbootstrap no está instalado:\n{e}")
    sys.exit(1)

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError as e:
    import tkinter.messagebox as mb
    mb.showerror("Dependencia faltante", f"tkinterdnd2 no está instalado:\n{e}")
    sys.exit(1)


def _resource_path(name: str) -> str:
    """Ruta a un recurso incluido, tanto en desarrollo como dentro del .exe."""
    base = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, name)


# ── Internacionalización (i18n) ──────────────────────────────────────────────
LANGS      = ["es", "en", "pt", "fr", "de"]
LANG_NAMES = {"es": "Español", "en": "English", "pt": "Português",
              "fr": "Français", "de": "Deutsch"}

# Idioma actual (se carga desde la configuración al iniciar).
_state = {"lang": "es"}

STRINGS = {
    "app_subtitle": {
        "es": "Convierte documentos a Markdown al instante",
        "en": "Convert documents to Markdown instantly",
        "pt": "Converte documentos para Markdown na hora",
        "fr": "Convertit vos documents en Markdown en un instant",
        "de": "Dokumente sofort in Markdown umwandeln",
    },
    "dz_drag": {
        "es": "Arrastra tus archivos aquí",
        "en": "Drag your files here",
        "pt": "Arraste seus arquivos aqui",
        "fr": "Glissez vos fichiers ici",
        "de": "Dateien hierher ziehen",
    },
    "dz_click_only": {
        "es": "Haz clic para seleccionar archivos",
        "en": "Click to select files",
        "pt": "Clique para selecionar arquivos",
        "fr": "Cliquez pour sélectionner des fichiers",
        "de": "Zum Auswählen von Dateien klicken",
    },
    "dz_hint": {
        "es": "o haz clic para seleccionarlos",
        "en": "or click to select them",
        "pt": "ou clique para selecioná-los",
        "fr": "ou cliquez pour les sélectionner",
        "de": "oder zum Auswählen klicken",
    },
    "dz_formats": {
        "es": "PDF · Word · Excel · PowerPoint · EPUB · ZIP · CSV · HTML · imágenes",
        "en": "PDF · Word · Excel · PowerPoint · EPUB · ZIP · CSV · HTML · images",
        "pt": "PDF · Word · Excel · PowerPoint · EPUB · ZIP · CSV · HTML · imagens",
        "fr": "PDF · Word · Excel · PowerPoint · EPUB · ZIP · CSV · HTML · images",
        "de": "PDF · Word · Excel · PowerPoint · EPUB · ZIP · CSV · HTML · Bilder",
    },
    "files_added": {
        "es": "Archivos agregados",
        "en": "Added files",
        "pt": "Arquivos adicionados",
        "fr": "Fichiers ajoutés",
        "de": "Hinzugefügte Dateien",
    },
    "clear_all": {
        "es": "Limpiar todo",
        "en": "Clear all",
        "pt": "Limpar tudo",
        "fr": "Tout effacer",
        "de": "Alle entfernen",
    },
    "status_start": {
        "es": "Agrega archivos para comenzar",
        "en": "Add files to get started",
        "pt": "Adicione arquivos para começar",
        "fr": "Ajoutez des fichiers pour commencer",
        "de": "Dateien hinzufügen, um zu starten",
    },
    "status_files": {
        "es": "Archivos: {n}   ·   Por convertir: {p}",
        "en": "Files: {n}   ·   To convert: {p}",
        "pt": "Arquivos: {n}   ·   A converter: {p}",
        "fr": "Fichiers : {n}   ·   À convertir : {p}",
        "de": "Dateien: {n}   ·   Zu konvertieren: {p}",
    },
    "status_converting": {
        "es": "Convirtiendo: {name}…",
        "en": "Converting: {name}…",
        "pt": "Convertendo: {name}…",
        "fr": "Conversion : {name}…",
        "de": "Konvertiere: {name}…",
    },
    "btn_convert": {
        "es": "Convertir todo",
        "en": "Convert all",
        "pt": "Converter tudo",
        "fr": "Tout convertir",
        "de": "Alle konvertieren",
    },
    "btn_converting": {
        "es": "Convirtiendo…",
        "en": "Converting…",
        "pt": "Convertendo…",
        "fr": "Conversion…",
        "de": "Konvertiere…",
    },
    "btn_add_more": {
        "es": "+ Agregar más",
        "en": "+ Add more",
        "pt": "+ Adicionar mais",
        "fr": "+ Ajouter d'autres",
        "de": "+ Mehr hinzufügen",
    },
    "credit": {
        "es": "Creado por {author}",
        "en": "Created by {author}",
        "pt": "Criado por {author}",
        "fr": "Créé par {author}",
        "de": "Erstellt von {author}",
    },
    "unsupported": {
        "es": "Formato no soportado — usa PDF, Word, Excel, etc.",
        "en": "Unsupported format — use PDF, Word, Excel, etc.",
        "pt": "Formato não suportado — use PDF, Word, Excel, etc.",
        "fr": "Format non pris en charge — utilisez PDF, Word, Excel, etc.",
        "de": "Format nicht unterstützt — PDF, Word, Excel usw. verwenden",
    },
    "about_title": {
        "es": "Acerca de {app}",
        "en": "About {app}",
        "pt": "Sobre o {app}",
        "fr": "À propos de {app}",
        "de": "Über {app}",
    },
    "about_version": {
        "es": "Versión {v}",
        "en": "Version {v}",
        "pt": "Versão {v}",
        "fr": "Version {v}",
        "de": "Version {v}",
    },
    "about_desc": {
        "es": "Convierte PDF, Word, PowerPoint, Excel,\nHTML e imágenes a Markdown con un clic.",
        "en": "Convert PDF, Word, PowerPoint, Excel,\nHTML and images to Markdown with one click.",
        "pt": "Converte PDF, Word, PowerPoint, Excel,\nHTML e imagens para Markdown com um clique.",
        "fr": "Convertit PDF, Word, PowerPoint, Excel,\nHTML et images en Markdown en un clic.",
        "de": "Wandelt PDF, Word, PowerPoint, Excel,\nHTML und Bilder mit einem Klick in Markdown um.",
    },
    "about_engine_label": {
        "es": "Motor de conversión",
        "en": "Conversion engine",
        "pt": "Motor de conversão",
        "fr": "Moteur de conversion",
        "de": "Konvertierungs-Engine",
    },
    "btn_close": {
        "es": "Cerrar", "en": "Close", "pt": "Fechar",
        "fr": "Fermer", "de": "Schließen",
    },
    "save_title": {
        "es": "¿Cómo guardar los archivos?",
        "en": "How to save the files?",
        "pt": "Como salvar os arquivos?",
        "fr": "Comment enregistrer les fichiers ?",
        "de": "Wie sollen die Dateien gespeichert werden?",
    },
    "save_count": {
        "es": "Archivos a convertir: {n}",
        "en": "Files to convert: {n}",
        "pt": "Arquivos a converter: {n}",
        "fr": "Fichiers à convertir : {n}",
        "de": "Zu konvertierende Dateien: {n}",
    },
    "save_question": {
        "es": "¿Cómo quieres guardar los resultados?",
        "en": "How do you want to save the results?",
        "pt": "Como você quer salvar os resultados?",
        "fr": "Comment voulez-vous enregistrer les résultats ?",
        "de": "Wie möchten Sie die Ergebnisse speichern?",
    },
    "save_folder": {
        "es": "Guardar todos en una carpeta",
        "en": "Save all in one folder",
        "pt": "Salvar todos em uma pasta",
        "fr": "Tout enregistrer dans un dossier",
        "de": "Alle in einem Ordner speichern",
    },
    "save_each": {
        "es": "Preguntar dónde guardar cada uno",
        "en": "Ask where to save each one",
        "pt": "Perguntar onde salvar cada um",
        "fr": "Demander où enregistrer chacun",
        "de": "Für jede Datei nachfragen",
    },
    "btn_cancel": {
        "es": "Cancelar", "en": "Cancel", "pt": "Cancelar",
        "fr": "Annuler", "de": "Abbrechen",
    },
    "pick_title": {
        "es": "Seleccionar archivos para convertir",
        "en": "Select files to convert",
        "pt": "Selecionar arquivos para converter",
        "fr": "Sélectionner les fichiers à convertir",
        "de": "Dateien zum Konvertieren auswählen",
    },
    "ft_supported": {
        "es": "Documentos soportados",
        "en": "Supported documents",
        "pt": "Documentos suportados",
        "fr": "Documents pris en charge",
        "de": "Unterstützte Dokumente",
    },
    "ft_images": {
        "es": "Imágenes", "en": "Images", "pt": "Imagens",
        "fr": "Images", "de": "Bilder",
    },
    "ft_all": {
        "es": "Todos los archivos",
        "en": "All files",
        "pt": "Todos os arquivos",
        "fr": "Tous les fichiers",
        "de": "Alle Dateien",
    },
    "dest_folder": {
        "es": "Carpeta de destino",
        "en": "Destination folder",
        "pt": "Pasta de destino",
        "fr": "Dossier de destination",
        "de": "Zielordner",
    },
    "save_as": {
        "es": "Guardar '{name}' como…",
        "en": "Save '{name}' as…",
        "pt": "Salvar '{name}' como…",
        "fr": "Enregistrer '{name}' sous…",
        "de": "'{name}' speichern unter…",
    },
    "dep_error_title": {
        "es": "Error de dependencia",
        "en": "Dependency error",
        "pt": "Erro de dependência",
        "fr": "Erreur de dépendance",
        "de": "Abhängigkeitsfehler",
    },
    "dep_error_msg": {
        "es": "MarkItDown no está disponible:\n{e}",
        "en": "MarkItDown is not available:\n{e}",
        "pt": "O MarkItDown não está disponível:\n{e}",
        "fr": "MarkItDown n'est pas disponible :\n{e}",
        "de": "MarkItDown ist nicht verfügbar:\n{e}",
    },
    "done_errors_title": {
        "es": "Completado con errores",
        "en": "Completed with errors",
        "pt": "Concluído com erros",
        "fr": "Terminé avec des erreurs",
        "de": "Mit Fehlern abgeschlossen",
    },
    "done_errors_msg": {
        "es": "Convertidos correctamente: {done}\n\nErrores:\n{details}",
        "en": "Successfully converted: {done}\n\nErrors:\n{details}",
        "pt": "Convertidos com sucesso: {done}\n\nErros:\n{details}",
        "fr": "Convertis avec succès : {done}\n\nErreurs :\n{details}",
        "de": "Erfolgreich konvertiert: {done}\n\nFehler:\n{details}",
    },
    "done_ok_title": {
        "es": "¡Conversión completada!",
        "en": "Conversion complete!",
        "pt": "Conversão concluída!",
        "fr": "Conversion terminée !",
        "de": "Konvertierung abgeschlossen!",
    },
    "done_ok_msg": {
        "es": "Archivos convertidos a Markdown: {done}",
        "en": "Files converted to Markdown: {done}",
        "pt": "Arquivos convertidos para Markdown: {done}",
        "fr": "Fichiers convertis en Markdown : {done}",
        "de": "In Markdown konvertierte Dateien: {done}",
    },
    "err_save_cancelled": {
        "es": "Guardado cancelado",
        "en": "Save cancelled",
        "pt": "Salvamento cancelado",
        "fr": "Enregistrement annulé",
        "de": "Speichern abgebrochen",
    },
    "opt_label": {
        "es": "Optimizar para IA — quita tablas vacías y espacios sobrantes",
        "en": "Optimize for AI — remove empty rows and extra blank space",
        "pt": "Otimizar para IA — remove linhas vazias e espaços extras",
        "fr": "Optimiser pour l'IA — supprime lignes vides et espaces inutiles",
        "de": "Für KI optimieren — leere Zeilen und Leerraum entfernen",
    },
}


def T(key: str, **kw) -> str:
    """Devuelve el texto traducido al idioma actual."""
    table = STRINGS.get(key, {})
    text = table.get(_state["lang"]) or table.get("es") or key
    return text.format(**kw) if kw else text


def _detect_os_lang() -> str:
    """Detecta el idioma de Windows; devuelve 'es' si no se reconoce."""
    try:
        import ctypes
        primary = ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF
        return {0x0A: "es", 0x09: "en", 0x16: "pt",
                0x0C: "fr", 0x07: "de"}.get(primary, "es")
    except Exception:
        return "es"


def _config_path() -> str:
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(base, "Docverty", "config.json")


def _load_config() -> dict:
    """Carga la configuración del usuario (idioma, opciones)."""
    try:
        with open(_config_path(), encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg if isinstance(cfg, dict) else {}
    except Exception:
        return {}


def _save_config(cfg: dict):
    try:
        path = _config_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
    except Exception:
        pass


# ── Post-procesado opcional del Markdown ─────────────────────────────────────
def post_process(md_text: str) -> str:
    """Limpieza opcional del Markdown para uso con IA: elimina filas de tabla
    vacías y colapsa el espaciado sobrante. Es conservadora — nunca borra
    contenido real y deja intacto el interior de los bloques de código."""
    cleaned: list[str] = []
    in_fence = False
    blanks = 0
    for raw in md_text.split("\n"):
        line = raw.rstrip()
        # Bloques de código ``` : se dejan exactamente como están.
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            cleaned.append(line)
            blanks = 0
            continue
        if in_fence:
            cleaned.append(raw)
            continue
        # Fila de tabla totalmente vacía (solo "|" y espacios, sin guiones).
        if "|" in line and "-" not in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and all(c == "" for c in cells):
                continue
        # Colapsar líneas en blanco consecutivas (máximo una).
        if line == "":
            blanks += 1
            if blanks <= 1:
                cleaned.append("")
            continue
        blanks = 0
        cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


# ── Motor de conversión ──────────────────────────────────────────────────────
_markitdown = None
_markitdown_error = ""
try:
    from markitdown import MarkItDown
    # exiftool (si está incluido) extrae metadatos de las imágenes.
    _exiftool = _resource_path(os.path.join("exiftool", "exiftool.exe"))
    if os.path.exists(_exiftool):
        _markitdown = MarkItDown(exiftool_path=_exiftool)
    else:
        _markitdown = MarkItDown()
except Exception as e:
    _markitdown_error = str(e)


# ── Tipos de archivo soportados ──────────────────────────────────────────────
# Cada extensión -> (etiqueta del badge [máx 4 letras], color del badge)
SUPPORTED_EXT = {
    ".pdf":   ("PDF",  "#EF4444"),
    ".docx":  ("DOC",  "#2563EB"),
    ".pptx":  ("PPT",  "#F97316"),
    ".xlsx":  ("XLS",  "#10B981"),
    ".xls":   ("XLS",  "#10B981"),
    ".csv":   ("CSV",  "#059669"),
    ".html":  ("HTM",  "#F59E0B"),
    ".htm":   ("HTM",  "#F59E0B"),
    ".xml":   ("XML",  "#D97706"),
    ".json":  ("JSON", "#475569"),
    ".jsonl": ("JSON", "#475569"),
    ".txt":   ("TXT",  "#6B7280"),
    ".epub":  ("EPUB", "#0D9488"),
    ".zip":   ("ZIP",  "#64748B"),
    ".ipynb": ("NB",   "#F97316"),
    ".msg":   ("MSG",  "#2563EB"),
    ".jpg":   ("IMG",  "#8B5CF6"),
    ".jpeg":  ("IMG",  "#8B5CF6"),
    ".png":   ("IMG",  "#8B5CF6"),
}

STATUS_PENDING    = "pending"
STATUS_PROCESSING = "processing"
STATUS_DONE       = "done"
STATUS_ERROR      = "error"

STATUS_ICON = {
    STATUS_PENDING:    "⏳",
    STATUS_PROCESSING: "🔄",
    STATUS_DONE:       "✅",
    STATUS_ERROR:      "❌",
}

# Colores de fondo de fila por estado
STATUS_ROW_COLOR = {
    STATUS_PENDING:    "#FFFFFF",
    STATUS_PROCESSING: "#FFFBEB",
    STATUS_DONE:       "#F0FDF4",
    STATUS_ERROR:      "#FEF2F2",
}

PURPLE = "#6B48FF"
PURPLE_HOVER = "#5539CC"
PURPLE_LIGHT = "#EEE9FF"
BLUE   = "#2563EB"
GRAY   = "#94A3B8"
DARK   = "#1F2937"
LINE   = "#E2E8F0"

# Zona de arrastre
DZ_BG        = "#F8F7FF"
DZ_BG_HOVER  = "#EEE9FF"
DZ_BORDER    = "#C4B8FF"

# Gradiente de fondo (purple -> blue)
GRAD_TOP     = (107, 72, 255)
GRAD_BOTTOM  = (37, 99, 235)


# ── Modelo de datos ──────────────────────────────────────────────────────────
class FileItem:
    def __init__(self, path: str):
        self.path = Path(path)
        self.status = STATUS_PENDING
        self.error: str | None = None
        self.output_path: str | None = None


# ── Aplicación ───────────────────────────────────────────────────────────────
class App(tbs.Window, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__(themename="litera")
        self._config = _load_config()
        cfg_lang = self._config.get("lang")
        _state["lang"] = cfg_lang if cfg_lang in LANGS else _detect_os_lang()

        self.title(APP_NAME)
        self.geometry("900x700")
        self.minsize(720, 560)
        self.resizable(True, True)

        self._set_icon()

        # Habilitar arrastrar y soltar (tkdnd). Si falla, la app sigue
        # funcionando solo con el selector de archivos.
        self._dnd_ok = False
        try:
            self.TkdndVersion = TkinterDnD._require(self)
            self._dnd_ok = True
        except Exception:
            pass

        self.files: list[FileItem] = []
        self._widgets: dict[str, dict] = {}
        self._converting = False
        self._resize_job = None
        self._bg_photo = None
        # Opción de post-procesado (desactivada por defecto).
        self._optimize_var = tk.BooleanVar(
            value=bool(self._config.get("optimize", False)))

        self._build_ui()
        self._setup_dnd()
        self._center_window()

    # ── Icono ──────────────────────────────────────────────────────────────
    def _get_resource(self, name: str) -> str:
        return _resource_path(name)

    def _set_icon(self):
        ico = self._get_resource("icon.ico")
        if os.path.exists(ico):
            self.iconbitmap(ico)

    def _dialog_icon(self, dlg: tk.Toplevel):
        """Aplica el ícono de la app a una ventana de diálogo."""
        ico = self._get_resource("icon.ico")
        if os.path.exists(ico):
            try:
                dlg.iconbitmap(ico)
            except tk.TclError:
                pass

    # ── Layout ────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Fondo con gradiente
        self._bg_canvas = tk.Canvas(self, highlightthickness=0)
        self._bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._on_resize)

        # Tarjeta blanca central
        self._card = tk.Frame(self._bg_canvas, bg="white", bd=0)
        self._card.place(relx=0.5, rely=0.5, anchor="center",
                         relwidth=0.88, relheight=0.90)

        self._build_card()

        # Primer render del gradiente
        self.after(30, self._draw_gradient)

    def _build_card(self):
        """Construye el contenido del card. Se puede reconstruir al cambiar
        de idioma. Orden importante: la barra inferior se ancla al fondo
        ANTES de construir la lista, para que sus botones nunca queden tapados."""
        self._build_header()
        self._build_drop_zone()
        self._build_bottom_bar()
        self._build_file_list()

    def _relocalize(self):
        """Reconstruye la interfaz en el idioma actual, conservando archivos."""
        for w in self._card.winfo_children():
            w.destroy()
        self._widgets.clear()
        self._build_card()
        for item in self.files:
            self._add_row(item)
            if item.status != STATUS_PENDING:
                self._set_row_status(item)
        self._refresh_state()

    def _build_header(self):
        hf = tk.Frame(self._card, bg="white")
        hf.pack(fill=X, padx=30, pady=(22, 0))

        tk.Label(hf, text=APP_NAME,
                 font=("Segoe UI", 22, "bold"),
                 fg=PURPLE, bg="white").pack(side=LEFT)

        tk.Label(hf, text="  ·  " + T("app_subtitle"),
                 font=("Segoe UI", 11), fg=GRAY, bg="white").pack(side=LEFT, pady=(6, 0))

        # Botón "Acerca de" (extremo derecho)
        info_btn = tk.Label(hf, text="ℹ",
                            font=("Segoe UI", 15), fg=GRAY, bg="white",
                            cursor="hand2")
        info_btn.pack(side=RIGHT, padx=(10, 0), pady=(2, 0))
        info_btn.bind("<Button-1>", lambda _e: self._show_about())
        info_btn.bind("<Enter>",    lambda _e: info_btn.configure(fg=PURPLE))
        info_btn.bind("<Leave>",    lambda _e: info_btn.configure(fg=GRAY))

        # Selector de idioma (a la izquierda del botón de info)
        lang_btn = tk.Label(hf, text=f"🌐 {LANG_NAMES[_state['lang']]}  ▾",
                            font=("Segoe UI", 10), fg=GRAY, bg="white",
                            cursor="hand2")
        lang_btn.pack(side=RIGHT, pady=(6, 0))
        lang_btn.bind("<Button-1>", self._show_lang_menu)
        lang_btn.bind("<Enter>", lambda _e: lang_btn.configure(fg=PURPLE))
        lang_btn.bind("<Leave>", lambda _e: lang_btn.configure(fg=GRAY))

        tk.Frame(self._card, height=1, bg=LINE).pack(fill=X, padx=30, pady=(14, 0))

    def _build_drop_zone(self):
        outer = tk.Frame(self._card, bg="white")
        outer.pack(fill=X, padx=30, pady=(18, 0))

        self._dz = tk.Frame(outer, bg=DZ_BG,
                            highlightbackground=DZ_BORDER,
                            highlightcolor=PURPLE,
                            highlightthickness=2,
                            cursor="hand2")
        self._dz.pack(fill=X, ipady=14)

        self._dz_icon = tk.Label(self._dz, text="📂",
                                 font=("Segoe UI Emoji", 26), bg=DZ_BG)
        self._dz_icon.pack(pady=(8, 2))

        main_text = T("dz_drag") if self._dnd_ok else T("dz_click_only")
        self._dz_text = tk.Label(self._dz, text=main_text,
                                 font=("Segoe UI", 13, "bold"),
                                 fg=PURPLE, bg=DZ_BG)
        self._dz_text.pack()

        self._dz_hint = tk.Label(self._dz,
                                 text=T("dz_hint") if self._dnd_ok else "",
                                 font=("Segoe UI", 10), fg=GRAY, bg=DZ_BG)
        self._dz_hint.pack(pady=(1, 0))

        self._dz_sub = tk.Label(self._dz, text=T("dz_formats"),
                                font=("Segoe UI", 9), fg="#B8AEE8", bg=DZ_BG)
        self._dz_sub.pack(pady=(6, 8))

        self._dz_widgets = (self._dz, self._dz_icon, self._dz_text,
                            self._dz_hint, self._dz_sub)
        for w in self._dz_widgets:
            w.bind("<Button-1>", self._pick_files)
            w.bind("<Enter>",    self._dz_enter)
            w.bind("<Leave>",    self._dz_leave)

    def _build_file_list(self):
        header = tk.Frame(self._card, bg="white")
        header.pack(fill=X, padx=30, pady=(18, 6))

        self._count_lbl = tk.Label(header, text=T("files_added"),
                                   font=("Segoe UI", 11, "bold"),
                                   fg=DARK, bg="white")
        self._count_lbl.pack(side=LEFT)

        clr = tk.Label(header, text=T("clear_all"),
                       font=("Segoe UI", 10), fg=PURPLE, bg="white",
                       cursor="hand2")
        clr.pack(side=RIGHT)
        clr.bind("<Button-1>", self._clear_all)

        # Canvas con scrollbar para la lista
        list_outer = tk.Frame(self._card, bg="white")
        list_outer.pack(fill=BOTH, expand=YES, padx=30)

        self._list_canvas = tk.Canvas(list_outer, bg="white",
                                      highlightthickness=0)
        sb = tk.Scrollbar(list_outer, orient="vertical",
                          command=self._list_canvas.yview)
        self._list_canvas.configure(yscrollcommand=sb.set)

        sb.pack(side=RIGHT, fill=Y)
        self._list_canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        self._rows_frame = tk.Frame(self._list_canvas, bg="white")
        self._rows_win = self._list_canvas.create_window(
            (0, 0), window=self._rows_frame, anchor="nw"
        )

        self._rows_frame.bind("<Configure>", self._sync_scrollregion)
        self._list_canvas.bind("<Configure>", self._sync_row_width)
        self._list_canvas.bind("<MouseWheel>", self._on_scroll)

    def _build_bottom_bar(self):
        # Toda la barra se ancla al fondo del card (side=BOTTOM). Se empaqueta
        # de abajo hacia arriba: crédito, botones, separador.
        credit_bar = tk.Frame(self._card, bg="white")
        credit_bar.pack(side=BOTTOM, fill=X, padx=30, pady=(4, 14))
        tk.Label(credit_bar,
                 text=T("credit", author=APP_AUTHOR),
                 font=("Segoe UI", 9, "italic"), fg="#C4B8FF", bg="white",
                 anchor="w").pack(side=LEFT)

        bar = tk.Frame(self._card, bg="white")
        bar.pack(side=BOTTOM, fill=X, padx=30, pady=(10, 0))

        self._status_lbl = tk.Label(bar, text=T("status_start"),
                                    font=("Segoe UI", 10), fg=GRAY, bg="white")
        self._status_lbl.pack(side=LEFT)

        self._convert_btn = tk.Button(
            bar, text=T("btn_convert"),
            font=("Segoe UI", 12, "bold"),
            fg="white", bg=PURPLE,
            activebackground=PURPLE_HOVER, activeforeground="white",
            bd=0, padx=22, pady=9, cursor="hand2", relief="flat",
            command=self._start_conversion,
            state="disabled",
        )
        self._convert_btn.pack(side=RIGHT)

        self._add_btn = tk.Button(
            bar, text=T("btn_add_more"),
            font=("Segoe UI", 11),
            fg=PURPLE, bg="white",
            activebackground=PURPLE_LIGHT, activeforeground=PURPLE,
            bd=1, padx=14, pady=8, cursor="hand2", relief="solid",
            command=self._pick_files,
        )
        self._add_btn.pack(side=RIGHT, padx=(0, 10))

        # Fila de opción de post-procesado (sobre los botones).
        opts = tk.Frame(self._card, bg="white")
        opts.pack(side=BOTTOM, fill=X, padx=30, pady=(10, 0))
        chk = tk.Checkbutton(
            opts, text=T("opt_label"),
            variable=self._optimize_var, command=self._on_optimize_toggle,
            font=("Segoe UI", 9), fg=GRAY, bg="white",
            activebackground="white", activeforeground=PURPLE,
            selectcolor="white", cursor="hand2",
            bd=0, highlightthickness=0, anchor="w",
        )
        chk.pack(side=LEFT)

        tk.Frame(self._card, height=1, bg=LINE).pack(
            side=BOTTOM, fill=X, padx=30, pady=(10, 0))

    # ── Selector de idioma ────────────────────────────────────────────────
    def _show_lang_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        for code in LANGS:
            menu.add_command(label=LANG_NAMES[code],
                             command=lambda c=code: self._change_language(c))
        menu.tk_popup(event.x_root, event.y_root)

    def _change_language(self, code: str):
        if code == _state["lang"] or self._converting:
            return
        _state["lang"] = code
        self._config["lang"] = code
        _save_config(self._config)
        self._relocalize()

    def _on_optimize_toggle(self):
        self._config["optimize"] = bool(self._optimize_var.get())
        _save_config(self._config)

    # ── Gradiente ─────────────────────────────────────────────────────────
    def _on_resize(self, event=None):
        # Solo reaccionar al redimensionado de la ventana principal,
        # no a eventos <Configure> que burbujean desde widgets hijos.
        if event is not None and event.widget is not self:
            return
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(60, self._draw_gradient)

    def _draw_gradient(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1 or h <= 1:
            return

        # Construir una franja vertical de 1px de ancho y escalarla a lo
        # ancho. Pillow hace el escalado en C: mucho más rápido que llenar
        # pixel por pixel (h iteraciones en vez de w*h).
        strip = Image.new("RGB", (1, h))
        r1, g1, b1 = GRAD_TOP
        r2, g2, b2 = GRAD_BOTTOM
        for y in range(h):
            t = y / h
            strip.putpixel((0, y), (
                int(r1 + (r2 - r1) * t),
                int(g1 + (g2 - g1) * t),
                int(b1 + (b2 - b1) * t),
            ))
        gradient = strip.resize((w, h))

        self._bg_photo = ImageTk.PhotoImage(gradient)
        self._bg_canvas.delete("all")
        self._bg_canvas.create_image(0, 0, image=self._bg_photo, anchor="nw")
        self._card.lift()

    # ── Arrastrar y soltar (drag & drop) ──────────────────────────────────
    def _setup_dnd(self):
        if not self._dnd_ok:
            return
        # Toda la ventana acepta archivos soltados desde el Explorador.
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>",      self._on_drop)
        self.dnd_bind("<<DragEnter>>", lambda _e: self._dz_enter())
        self.dnd_bind("<<DragLeave>>", lambda _e: self._dz_leave())

    def _on_drop(self, event):
        self._dz_leave()
        try:
            paths = self.tk.splitlist(event.data)
        except Exception:
            paths = event.data.split()
        self._add_files([str(p) for p in paths])

    # ── Zona de drop ──────────────────────────────────────────────────────
    def _dz_enter(self, _event=None):
        self._dz.configure(highlightbackground=PURPLE)
        for w in self._dz_widgets:
            w.configure(bg=DZ_BG_HOVER)

    def _dz_leave(self, _event=None):
        self._dz.configure(highlightbackground=DZ_BORDER)
        for w in self._dz_widgets:
            w.configure(bg=DZ_BG)

    # ── Agregar archivos ──────────────────────────────────────────────────
    def _pick_files(self, _event=None):
        ext_list = " ".join(f"*{e}" for e in SUPPORTED_EXT)
        paths = filedialog.askopenfilenames(
            title=T("pick_title"),
            filetypes=[
                (T("ft_supported"), ext_list),
                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("Excel", "*.xlsx *.xls"),
                ("PowerPoint", "*.pptx"),
                ("CSV / JSON / XML", "*.csv *.json *.jsonl *.xml"),
                ("HTML", "*.html *.htm"),
                ("EPUB", "*.epub"),
                ("ZIP", "*.zip"),
                (T("ft_images"), "*.jpg *.jpeg *.png"),
                (T("ft_all"), "*.*"),
            ],
        )
        if paths:
            self._add_files(list(paths))

    def _add_files(self, paths: list[str]):
        existing = {f.path for f in self.files}
        added = 0
        rejected = 0
        for path in paths:
            p = Path(path)
            if p in existing:
                continue
            if not p.is_file() or p.suffix.lower() not in SUPPORTED_EXT:
                rejected += 1
                continue
            item = FileItem(path)
            self.files.append(item)
            self._add_row(item)
            existing.add(p)
            added += 1
        self._refresh_state()
        # Si se soltó algo pero nada era válido, avisar discretamente.
        if added == 0 and rejected > 0:
            self._status_lbl.configure(text=T("unsupported"))

    def _add_row(self, item: FileItem):
        ext = item.path.suffix.lower()
        label, color = SUPPORTED_EXT.get(ext, ("FIL", "#6B7280"))

        row = tk.Frame(self._rows_frame, bg="white",
                       highlightbackground=LINE, highlightthickness=1)
        row.pack(fill=X, pady=(0, 3))

        badge = tk.Label(row, text=label,
                         font=("Segoe UI", 8, "bold"),
                         fg="white", bg=color, width=4, pady=2)
        badge.pack(side=LEFT, padx=(8, 8), pady=7)

        name = tk.Label(row, text=item.path.name,
                        font=("Segoe UI", 10), fg=DARK, bg="white",
                        anchor="w")
        name.pack(side=LEFT, fill=X, expand=YES, pady=7)

        icon_lbl = tk.Label(row, text=STATUS_ICON[STATUS_PENDING],
                            font=("Segoe UI Emoji", 14), bg="white", width=3)
        icon_lbl.pack(side=RIGHT, padx=(0, 6))

        rm = tk.Label(row, text="✕", font=("Segoe UI", 11),
                      fg=GRAY, bg="white", cursor="hand2")
        rm.pack(side=RIGHT, padx=(0, 4))
        rm.bind("<Button-1>", lambda _e, i=item, r=row: self._remove_file(i, r))

        self._widgets[str(item.path)] = {
            "row": row, "name": name, "icon": icon_lbl,
        }

    def _remove_file(self, item: FileItem, row: tk.Frame):
        if self._converting:
            return
        self.files = [f for f in self.files if f.path != item.path]
        self._widgets.pop(str(item.path), None)
        row.destroy()
        self._refresh_state()

    def _clear_all(self, _event=None):
        if self._converting:
            return
        self.files.clear()
        self._widgets.clear()
        for w in self._rows_frame.winfo_children():
            w.destroy()
        self._refresh_state()

    def _refresh_state(self):
        n = len(self.files)
        if n == 0:
            self._count_lbl.configure(text=T("files_added"))
            self._status_lbl.configure(text=T("status_start"))
            self._convert_btn.configure(state="disabled")
        else:
            pending = sum(1 for f in self.files if f.status in (STATUS_PENDING, STATUS_ERROR))
            self._count_lbl.configure(text=f"{T('files_added')} ({n})")
            self._status_lbl.configure(text=T("status_files", n=n, p=pending))
            can_convert = pending > 0 and not self._converting
            self._convert_btn.configure(state="normal" if can_convert else "disabled")

    def _set_row_status(self, item: FileItem):
        key = str(item.path)
        if key not in self._widgets:
            return
        w = self._widgets[key]
        w["icon"].configure(text=STATUS_ICON[item.status])
        bg = STATUS_ROW_COLOR[item.status]
        w["row"].configure(bg=bg, highlightbackground=LINE)
        w["name"].configure(bg=bg)
        w["icon"].configure(bg=bg)

        if item.status == STATUS_ERROR and item.error:
            w["name"].configure(fg="#991B1B",
                                text=f"{item.path.name}  ⚠ {item.error[:60]}")
        elif item.status == STATUS_DONE:
            w["name"].configure(fg="#065F46")

    # ── Conversión ────────────────────────────────────────────────────────
    def _start_conversion(self):
        if self._converting:
            return
        if _markitdown is None:
            messagebox.showerror(
                T("dep_error_title"),
                T("dep_error_msg", e=_markitdown_error),
            )
            return

        pending = [f for f in self.files if f.status in (STATUS_PENDING, STATUS_ERROR)]
        if not pending:
            return

        mode = self._ask_save_mode(len(pending))
        if mode is None:
            return

        if mode == "folder":
            folder = filedialog.askdirectory(title=T("dest_folder"))
            if not folder:
                return
        else:
            folder = None

        self._converting = True
        self._convert_btn.configure(state="disabled", text=T("btn_converting"))

        # Se lee la opción aquí (hilo principal) y se pasa al worker.
        optimize = bool(self._optimize_var.get())
        threading.Thread(
            target=self._worker,
            args=(pending, mode == "individual", folder, optimize),
            daemon=True,
        ).start()

    def _ask_save_mode(self, count: int) -> str | None:
        W, H = 440, 350
        dlg = tk.Toplevel(self)
        dlg.title(T("save_title"))
        dlg.resizable(False, False)
        dlg.configure(bg="white")
        dlg.transient(self)
        dlg.update_idletasks()
        dx = self.winfo_x() + (self.winfo_width()  - W) // 2
        dy = self.winfo_y() + (self.winfo_height() - H) // 2
        dlg.geometry(f"{W}x{H}+{dx}+{dy}")
        self._dialog_icon(dlg)
        dlg.grab_set()

        result: list[str | None] = [None]

        def pick(val):
            result[0] = val
            dlg.destroy()

        tk.Label(dlg, text=T("save_count", n=count),
                 font=("Segoe UI", 13, "bold"), fg=DARK,
                 bg="white").pack(side=TOP, pady=(24, 2))
        tk.Label(dlg, text=T("save_question"),
                 font=("Segoe UI", 10), fg=GRAY,
                 bg="white").pack(side=TOP, pady=(0, 18))

        # "Cancelar" se ancla al fondo del diálogo: siempre visible.
        cancel = tk.Label(dlg, text=T("btn_cancel"), font=("Segoe UI", 10),
                          fg=GRAY, bg="white", cursor="hand2")
        cancel.pack(side=BOTTOM, pady=(0, 18))
        cancel.bind("<Button-1>", lambda _e: dlg.destroy())

        btns = tk.Frame(dlg, bg="white")
        btns.pack(side=TOP, fill=X, padx=34)

        # Botones apilados verticalmente: el texto nunca se corta.
        tk.Button(btns, text=T("save_folder"),
                  font=("Segoe UI", 10, "bold"), fg="white", bg=PURPLE,
                  activebackground=PURPLE_HOVER, activeforeground="white",
                  bd=0, pady=11, cursor="hand2", relief="flat",
                  command=lambda: pick("folder")).pack(fill=X, pady=(0, 10))

        tk.Button(btns, text=T("save_each"),
                  font=("Segoe UI", 10), fg=PURPLE, bg="white",
                  activebackground=PURPLE_LIGHT, activeforeground=PURPLE,
                  bd=1, pady=10, cursor="hand2", relief="solid",
                  command=lambda: pick("individual")).pack(fill=X)

        dlg.wait_window()
        return result[0]

    def _worker(self, files: list[FileItem], individual: bool,
                folder: str | None, optimize: bool):
        for item in files:
            item.status = STATUS_PROCESSING
            item.error = None
            self.after(0, self._set_row_status, item)
            self.after(0, self._status_lbl.configure,
                       {"text": T("status_converting", name=item.path.name)})

            try:
                result = _markitdown.convert(str(item.path))
                md_text = result.text_content
                # Post-procesado opcional (limpieza para IA).
                if optimize:
                    md_text = post_process(md_text)

                if individual:
                    out_path = self._ask_save_path(item)
                    if out_path is None:
                        item.status = STATUS_PENDING
                        item.error = T("err_save_cancelled")
                        self.after(0, self._set_row_status, item)
                        continue
                else:
                    out_path = Path(folder) / (item.path.stem + ".md")

                Path(out_path).write_text(md_text, encoding="utf-8")
                item.output_path = str(out_path)
                item.status = STATUS_DONE

            except Exception as exc:
                item.status = STATUS_ERROR
                item.error = str(exc)

            self.after(0, self._set_row_status, item)

        self.after(0, self._conversion_finished)

    def _ask_save_path(self, item: FileItem) -> str | None:
        """Llama al diálogo de guardado desde el hilo principal."""
        holder: list[str | None] = [None]
        event = threading.Event()

        def ask():
            path = filedialog.asksaveasfilename(
                title=T("save_as", name=item.path.name),
                defaultextension=".md",
                initialfile=item.path.stem + ".md",
                initialdir=str(item.path.parent),
                filetypes=[("Markdown", "*.md"), (T("ft_text"), "*.txt"),
                           (T("ft_all"), "*.*")],
            )
            holder[0] = path or None
            event.set()

        self.after(0, ask)
        event.wait(timeout=300)
        return holder[0]

    def _conversion_finished(self):
        self._converting = False
        done   = sum(1 for f in self.files if f.status == STATUS_DONE)
        errors = sum(1 for f in self.files if f.status == STATUS_ERROR)

        self._convert_btn.configure(text=T("btn_convert"))
        self._refresh_state()

        if errors:
            details = "\n".join(
                f"• {f.path.name}: {f.error}"
                for f in self.files if f.status == STATUS_ERROR
            )
            messagebox.showwarning(
                T("done_errors_title"),
                T("done_errors_msg", done=done, details=details),
            )
        elif done:
            messagebox.showinfo(
                T("done_ok_title"),
                T("done_ok_msg", done=done),
            )

    # ── Scroll y redimensionado de lista ─────────────────────────────────
    def _sync_scrollregion(self, _event=None):
        self._list_canvas.configure(scrollregion=self._list_canvas.bbox("all"))

    def _sync_row_width(self, event):
        self._list_canvas.itemconfig(self._rows_win, width=event.width)

    def _on_scroll(self, event):
        self._list_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    # ── Acerca de ─────────────────────────────────────────────────────────
    def _show_about(self):
        W, H, HEAD = 480, 420, 88
        dlg = tk.Toplevel(self)
        dlg.title(T("about_title", app=APP_NAME))
        dlg.resizable(False, False)
        dlg.configure(bg="white")
        dlg.transient(self)
        dlg.update_idletasks()
        dx = self.winfo_x() + (self.winfo_width()  - W) // 2
        dy = self.winfo_y() + (self.winfo_height() - H) // 2
        dlg.geometry(f"{W}x{H}+{dx}+{dy}")
        self._dialog_icon(dlg)
        dlg.grab_set()

        # Cabecera con gradiente
        header = tk.Canvas(dlg, width=W, height=HEAD, highlightthickness=0)
        header.pack(fill=X)
        r1, g1, b1 = GRAD_TOP
        r2, g2, b2 = GRAD_BOTTOM
        for y in range(HEAD):
            t = y / HEAD
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            header.create_line(0, y, W, y, fill=f"#{r:02x}{g:02x}{b:02x}")
        header.create_text(W // 2, HEAD // 2, text=APP_NAME,
                           font=("Segoe UI", 24, "bold"), fill="white")

        body = tk.Frame(dlg, bg="white")
        body.pack(fill=BOTH, expand=YES, padx=24, pady=(18, 0))

        tk.Label(body, text=T("about_version", v=APP_VERSION),
                 font=("Segoe UI", 11), fg=GRAY, bg="white").pack()

        tk.Label(body, text=T("about_desc"),
                 font=("Segoe UI", 10), fg=DARK, bg="white",
                 justify="center").pack(pady=(10, 0))

        tk.Frame(body, height=1, bg=LINE).pack(fill=X, pady=(16, 14))

        tk.Label(body, text=T("credit", author=APP_AUTHOR),
                 font=("Segoe UI", 12, "bold"), fg=PURPLE, bg="white").pack()

        tk.Frame(body, height=1, bg=LINE).pack(fill=X, pady=(14, 14))

        tk.Label(body, text=T("about_engine_label"),
                 font=("Segoe UI", 9, "bold"), fg=GRAY, bg="white").pack()
        tk.Label(body, text=APP_ENGINE,
                 font=("Segoe UI", 9), fg=GRAY, bg="white").pack()
        tk.Label(body, text=APP_LICENSE,
                 font=("Segoe UI", 9), fg=GRAY, bg="white").pack()

        tk.Button(body, text=T("btn_close"),
                  font=("Segoe UI", 10, "bold"), fg="white", bg=PURPLE,
                  activebackground=PURPLE_HOVER, activeforeground="white",
                  bd=0, padx=30, pady=8, cursor="hand2", relief="flat",
                  command=dlg.destroy).pack(pady=(20, 0))

    # ── Centrar ventana ───────────────────────────────────────────────────
    def _center_window(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = max(0, (sw - 900) // 2)
        y = max(0, (sh - 700) // 2)
        self.geometry(f"900x700+{x}+{y}")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
