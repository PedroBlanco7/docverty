# Docverty

> Convierte documentos a Markdown con un clic — aplicación de escritorio nativa para Windows.

**Docverty** es una aplicación de escritorio para Windows que convierte documentos
(PDF, Word, Excel, PowerPoint, EPUB, HTML, imágenes y más) a formato **Markdown**.
Tiene una interfaz moderna, soporta arrastrar y soltar, está disponible en 5 idiomas
y no requiere instalar Python — el instalador es autocontenido.

Creado por **Pedro Blanco**. Motor de conversión:
[MarkItDown](https://github.com/microsoft/markitdown) © Microsoft (licencia MIT).

---

## Características

- **19 formatos** de entrada (PDF, Word, Excel, PowerPoint, EPUB, ZIP, CSV, HTML, imágenes…)
- **Arrastrar y soltar** archivos directamente desde el Explorador de Windows
- **Conversión por lotes** — múltiples archivos a la vez, con estado individual
- **5 idiomas** — español, inglés, portugués, francés y alemán (cambio instantáneo)
- **Optimización opcional para IA** — limpia el Markdown para usarlo con LLMs
- **Interfaz nativa** — sin terminal, sin navegador, sin consola
- **Instalador de Windows** — acceso directo en el menú inicio, desinstalable
- **Autocontenido** — funciona en cualquier PC con Windows 10/11 sin instalar nada

## Instalación (usuarios)

1. Ve a la pestaña **[Releases](../../releases)** de este repositorio
2. Descarga `Docverty-Setup.exe`
3. Ejecútalo y sigue el asistente

> Windows puede mostrar un aviso de SmartScreen la primera vez (normal en
> instaladores sin firma digital de pago): clic en **Más información →
> Ejecutar de todas formas**.

## Formatos soportados

| Categoría        | Extensiones |
|------------------|-------------|
| Documentos       | `.pdf` `.docx` `.pptx` |
| Hojas de cálculo | `.xlsx` `.xls` `.csv` |
| Datos / texto    | `.txt` `.json` `.jsonl` `.xml` |
| Web              | `.html` `.htm` |
| Libros           | `.epub` |
| Comprimidos      | `.zip` |
| Notebooks        | `.ipynb` |
| Correos          | `.msg` |
| Imágenes         | `.jpg` `.jpeg` `.png` (extrae metadatos) |

> **Audio:** no se incluye. MarkItDown puede transcribir audio, pero usa una
> API gratuita no oficial de Google poco fiable, por lo que se omitió.

## Optimización para IA (opcional)

Hay una casilla **"Optimizar para IA"** sobre los botones de conversión,
**desactivada por defecto**. Al activarla, el Markdown resultante se limpia:

- Elimina filas de tabla vacías (típicas en PDF con formularios)
- Colapsa el espaciado sobrante

Es conservadora: no borra contenido real y respeta los bloques de código.
La conversión normal de Docverty no cambia si la casilla está desmarcada.

## Idiomas

La interfaz está disponible en **español, inglés, portugués, francés y alemán**.
Se cambia al instante desde el selector 🌐 en la esquina superior derecha.
Al abrir por primera vez, Docverty detecta el idioma de Windows; la elección
del usuario se guarda en `%APPDATA%\Docverty\config.json`.

---

## Desarrollo

### Requisitos

- Python 3.14
- Windows 10/11

### Preparar el entorno

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Descargar exiftool (metadatos de imágenes)

La carpeta `exiftool/` no se versiona por su tamaño (~33 MB). Para obtenerla:

1. Descarga el paquete Windows de [exiftool.org](https://exiftool.org) (`exiftool-XX.XX_64.zip`)
2. Extráelo
3. Crea la carpeta `exiftool/` en la raíz del proyecto y copia dentro:
   - `exiftool(-k).exe` renombrado a `exiftool.exe`
   - la carpeta `exiftool_files/`

La app funciona sin exiftool, pero las imágenes no extraerán metadatos.

### Ejecutar en modo desarrollo

```powershell
python app.py
```

### Compilar el ejecutable

```powershell
.venv\Scripts\pyinstaller.exe Docverty.spec --clean
# Salida: dist\Docverty.exe
```

> Si regeneras el ícono, ejecuta `python create_icon.py` antes de compilar.

### Crear el instalador

1. Instala [Inno Setup 6](https://jrsoftware.org/isdl.php) (gratuito)
2. Asegúrate de que `dist\Docverty.exe` esté actualizado
3. Abre `setup.iss` con Inno Setup → **Build → Compile** (`Ctrl+F9`)
4. Salida: `installer\Docverty-Setup.exe`

## Pila tecnológica

- **MarkItDown 0.1.5** (Microsoft, MIT) — motor de conversión
- **ttkbootstrap** — interfaz gráfica moderna sobre tkinter
- **tkinterdnd2** — arrastrar y soltar desde el Explorador
- **Pillow** — procesamiento de imágenes y gradiente
- **exiftool** — metadatos de imágenes (binario externo)
- **PyInstaller** — empaquetado a `.exe` autocontenido
- **Inno Setup** — instalador de Windows

## Créditos y licencias

- Docverty fue creado por **Pedro Blanco**
- El motor de conversión es [MarkItDown](https://github.com/microsoft/markitdown),
  publicado por Microsoft bajo licencia MIT
- Ver [`AVISOS-DE-TERCEROS.txt`](AVISOS-DE-TERCEROS.txt) para las licencias
  completas de todos los componentes de terceros
