# Docverty — Convert Documents to Markdown

> **Free native Windows desktop app to convert PDF, Word, Excel, PowerPoint, EPUB, HTML and images to Markdown — in one click.**

**Docverty** is a fast, lightweight **document-to-Markdown converter** for Windows.
It turns **PDF, DOCX, XLSX, PPTX, EPUB, HTML, CSV, images and 12 more formats**
into clean Markdown — ideal for **LLMs, RAG pipelines, Obsidian notes, static
sites and technical documentation**.

No terminal, no browser, no Python required. Just install and convert.

Built by **Pedro Blanco**. Conversion engine:
[MarkItDown](https://github.com/microsoft/markitdown) by Microsoft (MIT license).

---

## Features

- **19 input formats** — PDF, Word, Excel, PowerPoint, EPUB, ZIP, CSV, HTML, images and more
- **Drag and drop** files straight from Windows Explorer
- **Batch conversion** — convert many files at once, each with its own status
- **5 interface languages** — English, Spanish, Portuguese, French, German (instant switching)
- **Optional AI optimization** — cleans the Markdown for use with LLMs and RAG
- **Native Windows UI** — no console window, no web view
- **Windows installer** — Start Menu shortcut, clean uninstall
- **Self-contained** — runs on any Windows 10/11 PC, no dependencies to install

## Download & Install

1. Open the **[Releases](../../releases)** tab of this repository
2. Download **`Docverty-Setup.exe`**
3. Run it and follow the installer

> Windows SmartScreen may warn you the first time (normal for installers
> without a paid code-signing certificate): click **More info → Run anyway**.

## Supported formats

| Category        | Extensions |
|-----------------|------------|
| Documents       | `.pdf` `.docx` `.pptx` |
| Spreadsheets    | `.xlsx` `.xls` `.csv` |
| Data / text     | `.txt` `.json` `.jsonl` `.xml` |
| Web             | `.html` `.htm` |
| E-books         | `.epub` |
| Archives        | `.zip` |
| Notebooks       | `.ipynb` |
| Email           | `.msg` |
| Images          | `.jpg` `.jpeg` `.png` (metadata extraction) |

> **Audio** is intentionally not included. MarkItDown can transcribe audio, but
> it relies on an unofficial free Google speech API that is unreliable.

## Why convert documents to Markdown?

Markdown is the lingua franca of modern text workflows. Docverty is useful for:

- **Feeding documents to AI models** (ChatGPT, Claude, Gemini) with clean, token-efficient input
- **Building RAG knowledge bases** and vector embeddings from PDFs and Office files
- **Importing content into Obsidian, Notion or static site generators**
- **Turning reports, contracts and papers into version-controllable plain text**

## AI optimization (optional)

An **"Optimize for AI"** checkbox sits above the convert buttons, **off by
default**. When enabled, the resulting Markdown is cleaned:

- Removes empty table rows (common in form-style PDFs)
- Collapses excessive blank lines

It is conservative — it never deletes real content and leaves code blocks
intact. Docverty's normal conversion is unchanged when the box is unchecked.

## Languages

The interface is available in **English, Spanish, Portuguese, French and
German**, switchable instantly from the 🌐 selector in the top-right corner.
On first launch Docverty detects the Windows language; the user's choice is
saved to `%APPDATA%\Docverty\config.json`.

---

## Development

### Requirements

- Python 3.14
- Windows 10/11

### Set up the environment

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Download exiftool (for image metadata)

The `exiftool/` folder is not versioned due to its size (~33 MB). To get it:

1. Download the Windows package from [exiftool.org](https://exiftool.org) (`exiftool-XX.XX_64.zip`)
2. Extract it
3. Create an `exiftool/` folder in the project root and copy in:
   - `exiftool(-k).exe` renamed to `exiftool.exe`
   - the `exiftool_files/` folder

The app works without exiftool, but images will not extract metadata.

### Run in development mode

```powershell
python app.py
```

### Build the executable

```powershell
.venv\Scripts\pyinstaller.exe Docverty.spec --clean
# Output: dist\Docverty.exe
```

> If you regenerate the icon, run `python create_icon.py` before building.

### Build the installer

1. Install [Inno Setup 6](https://jrsoftware.org/isdl.php) (free)
2. Make sure `dist\Docverty.exe` is up to date
3. Open `setup.iss` with Inno Setup → **Build → Compile** (`Ctrl+F9`)
4. Output: `installer\Docverty-Setup.exe`

## Tech stack

- **MarkItDown 0.1.5** (Microsoft, MIT) — conversion engine
- **ttkbootstrap** — modern themed UI on top of tkinter
- **tkinterdnd2** — drag-and-drop from Windows Explorer
- **Pillow** — image processing and background gradient
- **exiftool** — image metadata (external binary)
- **PyInstaller** — packaging into a self-contained `.exe`
- **Inno Setup** — Windows installer

## FAQ

**Is Docverty free?**
Yes — free and open source.

**Do I need Python installed to use it?**
No. The installer is fully self-contained and runs on any Windows 10/11 PC.

**Does it work offline?**
Yes. All conversion runs locally on your machine.

**How is it different from MarkItDown?**
MarkItDown is a command-line library. Docverty wraps it in a polished native
Windows app with drag-and-drop, batch conversion and a multilingual UI — so you
don't need a terminal.

**Can it convert PDF to Markdown?**
Yes — PDF, Word, Excel, PowerPoint, EPUB, HTML and more, all to Markdown.

## Credits & license

- Docverty was created by **Pedro Blanco**
- The conversion engine is [MarkItDown](https://github.com/microsoft/markitdown),
  released by Microsoft under the MIT license
- See [`AVISOS-DE-TERCEROS.txt`](AVISOS-DE-TERCEROS.txt) for full third-party
  license notices
