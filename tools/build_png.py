"""Render a transparent PNG next to every SVG in logo/, ascenders/, promise/ and icons/.

Run: python3 tools/build_png.py   (needs PyMuPDF: pip install pymupdf)
Logo and promise PNGs are 1000 px wide, ascender PNGs 500 px, icon PNGs 120 px (for emails,
where SVG does not show).
"""
import fitz, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
for folder, width in (("logo", 1000), ("ascenders", 500), ("promise", 1000), ("icons/cobalt", 120), ("icons/sky", 120)):
    for svg in sorted((root / folder).glob("*.svg")):
        doc = fitz.open(str(svg)); page = doc[0]
        z = width / page.rect.width
        pix = page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
        pix.save(str(svg.with_suffix(".png")))
        print(svg.with_suffix(".png").name, pix.width, pix.height)

# Social icons for emails: the glyph cropped and centred on a square canvas, so icons of different
# shapes line up on their centres in every client (icons/social/<colour>/<name>.png, 120 px).
from PIL import Image
for colour in ("sky", "cobalt"):
    out = root / "icons" / "social" / colour
    out.mkdir(parents=True, exist_ok=True)
    for name in ("linked-in", "youtube", "instagram", "x", "facebook", "tiktok"):
        page = fitz.open(str(root / "icons" / colour / f"{name}.svg"))[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(480 / page.rect.width, 480 / page.rect.width), alpha=True)
        im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
        im = im.crop(im.split()[-1].getbbox())
        side = max(im.size)
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
        canvas.resize((120, 120), Image.LANCZOS).save(out / f"{name}.png")
        print(f"icons/social/{colour}/{name}.png")
