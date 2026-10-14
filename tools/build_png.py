"""Render a transparent PNG next to every SVG in logo/, ascenders/ and promise/.

Run: python3 tools/build_png.py   (needs PyMuPDF: pip install pymupdf)
Logo and promise PNGs are 1000 px wide, ascender PNGs 500 px.
"""
import fitz, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
for folder, width in (("logo", 1000), ("ascenders", 500), ("promise", 1000)):
    for svg in sorted((root / folder).glob("*.svg")):
        doc = fitz.open(str(svg)); page = doc[0]
        z = width / page.rect.width
        pix = page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
        pix.save(str(svg.with_suffix(".png")))
        print(svg.with_suffix(".png").name, pix.width, pix.height)
