"""
Genera icon.ico (multi-resolución) a partir de logo.png.

Uso:
    python create_icon.py

Incluye todos los tamaños que Windows solicita en la barra de tareas, el
menú inicio y el explorador, con realce de nitidez en los tamaños pequeños
para que el ícono no se vea borroso.
"""
from PIL import Image, ImageFilter
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH   = os.path.join(PROJECT_DIR, "logo.png")
ICON_PATH   = os.path.join(PROJECT_DIR, "icon.ico")

# Tamaños que Windows realmente usa (incluye los de pantallas con escalado DPI)
ICON_SIZES = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]


def _sharpen(img: Image.Image) -> Image.Image:
    """Realza la nitidez de la imagen sin tocar el canal alfa (bordes)."""
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b)).filter(
        ImageFilter.UnsharpMask(radius=1.0, percent=120, threshold=1)
    )
    r2, g2, b2 = rgb.split()
    return Image.merge("RGBA", (r2, g2, b2, a))


def create_icon(logo_path: str = LOGO_PATH, output_path: str = ICON_PATH):
    if not os.path.exists(logo_path):
        print(f"ERROR: no se encontró el logo en {logo_path}")
        print("Coloca tu logo como 'logo.png' en la raíz del proyecto.")
        sys.exit(1)

    logo = Image.open(logo_path).convert("RGBA")

    images = []
    for s in ICON_SIZES:
        resized = logo.resize((s, s), Image.LANCZOS)
        # El escalado suaviza la imagen; en tamaños chicos se realza para
        # que en la barra de tareas no se vea borroso.
        if s <= 64:
            resized = _sharpen(resized)
        images.append(resized)

    # La imagen mayor es la principal; las demás van como adicionales.
    images[-1].save(output_path, format="ICO", append_images=images[:-1])

    kb = os.path.getsize(output_path) / 1024
    print(f"Icono generado: {output_path}")
    print(f"Resoluciones: {', '.join(f'{s}x{s}' for s in ICON_SIZES)}")
    print(f"Tamaño: {kb:.1f} KB")


if __name__ == "__main__":
    create_icon()
