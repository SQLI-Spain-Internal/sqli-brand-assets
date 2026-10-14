"""Write README.md and index.html from the files on disk.

Run from anywhere: python3 tools/build_docs.py https://sqli-spain-internal.github.io/sqli-brand-assets
Every SVG in logo/, ascenders/ and promise/ must be listed in the tables below, with the backgrounds
the brand book approves it on.
"""
import sys, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://sqli-spain-internal.github.io/sqli-brand-assets").rstrip("/") + "/"

CREAM, MIDNIGHT, SKY, COBALT = "#FFFAF0", "#0F0E2B", "#6DA5FF", "#1F24E9"
BG = {"Cream": CREAM, "Midnight Blue": MIDNIGHT, "Sky Blue": SKY, "Cobalt Blue": COBALT}

# file stem -> backgrounds it is approved on (brand book p13, p14, p15, p27, p28)
LOGO = {
    "sqli-logo-midnight": ["Cream", "Sky Blue"],
    "sqli-logo-cobalt": ["Cream"],
    "sqli-logo-cream": ["Midnight Blue", "Cobalt Blue"],
    "sqli-logo-sky": ["Midnight Blue"],
    "sqli-logo-midnight-safe-zone": ["Cream", "Sky Blue"],
    "sqli-logo-cream-safe-zone": ["Midnight Blue", "Cobalt Blue"],
    "sqli-logo-sky-safe-zone": ["Midnight Blue"],
}
ASC = {
    "sqli-ascenders-midnight": ["Cream", "Sky Blue"],
    "sqli-ascenders-sky": ["Cream", "Midnight Blue"],
    "sqli-ascenders-cobalt": ["Cream"],
    "sqli-ascenders-cream": ["Midnight Blue", "Sky Blue", "Cobalt Blue"],
}
PROMISE = {
    "elevate-digitally-inline-midnight": ["Cream", "Sky Blue"],
    "elevate-digitally-wrapped-midnight": ["Cream", "Sky Blue"],
    "elevate-digitally-inline-cream": ["Midnight Blue", "Cobalt Blue"],
    "elevate-digitally-wrapped-cream": ["Midnight Blue", "Cobalt Blue"],
    "elevate-digitally-inline-ascenders-midnight-sky": ["Cream"],
    "elevate-digitally-wrapped-ascenders-midnight-sky": ["Cream"],
    "elevate-digitally-inline-ascenders-midnight-cream": ["Sky Blue"],
    "elevate-digitally-inline-ascenders-cream-sky": ["Midnight Blue"],
    "elevate-digitally-wrapped-ascenders-cream-sky": ["Midnight Blue"],
    "elevate-digitally-inline-ascenders-cream": ["Cobalt Blue"],
    "elevate-digitally-wrapped-ascenders-cream": ["Cobalt Blue"],
    "elevate-digitally-inline-ascenders-midnight": ["Cream"],
    "elevate-digitally-wrapped-ascenders-midnight": ["Cream"],
}
GROUPS = [("Logo", "logo", LOGO), ("Ascenders", "ascenders", ASC), ("Promise", "promise", PROMISE)]
# Files not taken unchanged from the official asset set. Brand book pages, for maintainers:
# sqli-logo-cobalt p13 and p27, midnight-cream promise p15, download-fill p9.
BUILT = {
    "logo/sqli-logo-cobalt.svg": "the official Midnight Blue logo recoloured to Cobalt Blue. The brand guidelines approve a Cobalt Blue logo on Cream, but the official asset set does not include the file",
    "promise/elevate-digitally-inline-ascenders-midnight-cream.svg": "the official promise with Cream ascenders, for Sky Blue backgrounds. The brand guidelines approve this combination, but the official asset set does not include the file",
    "icons/cobalt/download-fill.svg": "the filled-circle download icon shown in the brand guidelines, rebuilt from parts of the official icon set",
    "icons/sky/download-fill.svg": "the same icon in Sky Blue",
}
FONTS = [("light", 300, "normal"), ("light-italic", 300, "italic"), ("regular", 400, "normal"),
         ("regular-italic", 400, "italic"), ("medium", 500, "normal")]

for folder, d in (("logo", LOGO), ("ascenders", ASC), ("promise", PROMISE)):
    on_disk = {p.stem for p in (ROOT / folder).glob("*.svg")}
    assert on_disk == set(d), (folder, on_disk ^ set(d))

icons = sorted(p.name for p in (ROOT / "icons/cobalt").glob("*.svg"))
assert icons == sorted(p.name for p in (ROOT / "icons/sky").glob("*.svg"))

# ---------- README ----------
r = []
r.append("# SQLI brand assets\n")
r.append("Basic SQLI brand files with stable public URLs, for email signatures, presentations and web pages. "
         "Every file is served by GitHub Pages at the URLs below. A preview page lists everything: " + BASE + "\n")
r.append("Use the GitHub Pages URLs, not raw.githubusercontent.com. The raw host serves SVG as plain text, so SVG files do not display in an `<img>` tag from there.\n")
r.append("## Use of these files\n")
r.append("The SQLI logo, the promise and the ascenders are trademarks of SQLI. This repository has no open source licence. "
         "The files are published for SQLI communications and for partners SQLI has authorised to use its brand. "
         "Use them as they are, without changing colour, shape or proportions. For anything not covered here, contact SQLI marketing.\n")
r.append("## Brand colours\n")
r.append("| Colour | Hex |\n|---|---|")
for n, h in (("Cream", CREAM), ("Midnight Blue", MIDNIGHT), ("Sky Blue", SKY), ("Cobalt Blue", COBALT)):
    r.append(f"| {n} | `{h}` |")
r.append("")
r.append("## Logo colour per background\n")
r.append("| Background | Logo colour |\n|---|---|")
r.append("| Cream | Midnight Blue or Cobalt Blue |\n| Midnight Blue | Cream or Sky Blue |\n| Sky Blue | Midnight Blue |\n| Cobalt Blue | Cream |\n")
r.append("The safe-zone versions include the clear space the brand book requires around the logo. "
         "Promise file names give the type colour first, then the ascender colour.\n")
r.append("## Files\n")
r.append("PNG files have a transparent background. Logo and promise PNGs are 1000 px wide, ascender PNGs are 500 px wide. "
         "Email clients often block SVG, so use the PNG there.\n")
for title, folder, d in GROUPS:
    r.append(f"### {title}\n")
    r.append("| File | Use on | SVG | PNG |\n|---|---|---|---|")
    for stem in d:
        r.append(f"| `{stem}` | {', '.join(d[stem])} | {BASE}{folder}/{stem}.svg | {BASE}{folder}/{stem}.png |")
    r.append("")
r.append("### Icons\n")
r.append(f"The official iconography in two colours, SVG only: Cobalt Blue in `icons/cobalt/` (for Cream backgrounds) and Sky Blue in `icons/sky/` (for Midnight Blue backgrounds). "
         f"Each icon has the same name in both folders, for example {BASE}icons/cobalt/arrow-right.svg\n")
r.append("Available icons: " + ", ".join(f"`{i[:-4]}`" for i in icons) + ".\n")
r.append("### Fonts\n")
r.append("TWK Everett Light and Regular, each with its italic, and Medium. There is no bold weight in the brand.\n")
r.append("| File | Weight | Style |\n|---|---|---|")
for n, w, s in FONTS:
    r.append(f"| {BASE}fonts/twk-everett-{n}.ttf | {w} | {s} |")
r.append("")
r.append("```css")
for n, w, s in FONTS:
    r.append("@font-face {\n  font-family: \"TWK Everett\";\n"
             f"  src: url(\"{BASE}fonts/twk-everett-{n}.ttf\") format(\"truetype\");\n"
             f"  font-weight: {w};\n  font-style: {s};\n  font-display: swap;\n}}")
r.append("\nbody {\n  font-family: \"TWK Everett\", Arial, sans-serif;\n}\n```\n")
r.append("## Files built from the official ones\n")
r.append("Most files are copied unchanged from the official SQLI asset set and only renamed. These were built from official material:\n")
for k, v in BUILT.items():
    r.append(f"- `{k}` is {v}.")
r.append("- Every PNG is rendered from the SVG with the same name.\n")
r.append("The usage rules come from the SQLI Brand Guidelines v1.1, an internal document. SQLI staff can get it from marketing.\n")
(ROOT / "README.md").write_text("\n".join(r), encoding="utf-8")

# ---------- index.html ----------
def card(folder, stem, bgs):
    bg = BG[bgs[0]]
    svg, png = f"{folder}/{stem}.svg", f"{folder}/{stem}.png"
    return (f'<figure class="card"><div class="preview {folder}" style="background:{bg}">'
            f'<img src="{svg}" alt="{html.escape(stem)}" loading="lazy"></div>'
            f'<figcaption><strong>{stem}</strong><span class="use">Use on {", ".join(bgs)}</span>'
            f'<a href="{BASE}{svg}">{BASE}{svg}</a><a href="{BASE}{png}">{BASE}{png}</a></figcaption></figure>')

h = []
h.append("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQLI brand assets</title>
<link rel="icon" href="ascenders/sqli-ascenders-cobalt.svg" type="image/svg+xml">
<style>""")
for n, w, s in FONTS:
    h.append(f'@font-face{{font-family:"TWK Everett";src:url("fonts/twk-everett-{n}.ttf") format("truetype");font-weight:{w};font-style:{s};font-display:swap}}')
h.append(f""":root{{--cream:{CREAM};--midnight:{MIDNIGHT};--sky:{SKY};--cobalt:{COBALT}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cream);color:var(--midnight);font-family:"TWK Everett",Arial,sans-serif;font-weight:400;line-height:1.5}}
main{{max-width:1200px;margin:0 auto;padding:48px 16px 80px}}
header img{{height:72px;display:block}}
h1{{font-weight:400;font-size:40px;margin:32px 0 8px}}
h2{{font-weight:500;font-size:24px;margin:56px 0 16px}}
p{{max-width:72ch;font-weight:300}}
a{{color:var(--cobalt);word-break:break-all}}
code{{font-size:.9em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px}}
.card{{margin:0;border:1px solid rgba(15,14,43,.15);background:#fff;overflow:hidden}}
.preview{{height:180px;display:flex;align-items:center;justify-content:center;padding:24px}}
.preview img{{max-width:100%;max-height:100%}}
.preview.ascenders img{{height:110px}}
figcaption{{padding:12px 16px 16px;font-size:13px;display:flex;flex-direction:column;gap:4px}}
figcaption strong{{font-weight:500;font-size:14px}}
.use{{font-weight:300}}
.swatches{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}}
.swatch{{height:120px;padding:16px;display:flex;flex-direction:column;justify-content:flex-end;font-size:14px}}
.icons{{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;padding:16px}}
.icons a{{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:11px;text-decoration:none;text-align:center;word-break:break-word}}
.icons img{{width:36px;height:36px}}
.on-cream{{background:var(--cream);border:1px solid rgba(15,14,43,.15)}}
.on-midnight{{background:var(--midnight)}}
.on-midnight a{{color:var(--cream)}}
.fonts div{{font-size:28px;margin:8px 0}}
pre{{background:var(--midnight);color:var(--cream);padding:16px;overflow-x:auto;font-size:13px}}
</style>
</head>
<body>
<main>
<header><img src="logo/sqli-logo-midnight.svg" alt="sqli"></header>
<h1>Brand assets</h1>
<p>Logos, ascenders, the promise, icons and fonts with stable public URLs, for email signatures, presentations and web pages. Each file is available as SVG and as a transparent PNG (icons as SVG only). Use the PNG in email signatures. The usage rules come from the SQLI Brand Guidelines v1.1.</p>
<p>The SQLI logo, the promise and the ascenders are trademarks of SQLI. These files are published for SQLI communications and for authorised partners. Use them as they are, without changing colour, shape or proportions.</p>
<p>Repository: <a href="https://github.com/SQLI-Spain-Internal/sqli-brand-assets">github.com/SQLI-Spain-Internal/sqli-brand-assets</a></p>
<h2>Colours</h2>
<div class="swatches">
<div class="swatch on-cream">Cream<br><code>{CREAM}</code></div>
<div class="swatch" style="background:var(--midnight);color:var(--cream)">Midnight Blue<br><code>{MIDNIGHT}</code></div>
<div class="swatch" style="background:var(--sky);color:var(--midnight)">Sky Blue<br><code>{SKY}</code></div>
<div class="swatch" style="background:var(--cobalt);color:var(--cream)">Cobalt Blue<br><code>{COBALT}</code></div>
</div>
<p>Logo colour per background. On Cream, Midnight Blue or Cobalt Blue. On Midnight Blue, Cream or Sky Blue. On Sky Blue, Midnight Blue. On Cobalt Blue, Cream.</p>""")
for title, folder, d in GROUPS:
    h.append(f"<h2>{title}</h2>")
    if folder == "promise":
        h.append("<p>File names give the type colour first, then the ascender colour. Inline is one line, wrapped is two lines.</p>")
    if folder == "logo":
        h.append("<p>The safe-zone versions include the clear space around the logo.</p>")
    h.append('<div class="grid">' + "".join(card(folder, s, b) for s, b in d.items()) + "</div>")
h.append("<h2>Icons</h2>")
h.append(f"<p>Cobalt Blue icons for Cream backgrounds, Sky Blue icons for Midnight Blue backgrounds. URL pattern: <code>{BASE}icons/cobalt/&lt;name&gt;.svg</code> and <code>{BASE}icons/sky/&lt;name&gt;.svg</code>.</p>")
for colour, cls in (("cobalt", "on-cream"), ("sky", "on-midnight")):
    h.append(f'<div class="icons {cls}">' + "".join(
        f'<a href="{BASE}icons/{colour}/{i}"><img src="icons/{colour}/{i}" alt="" loading="lazy">{i[:-4]}</a>' for i in icons) + "</div>")
    h.append('<div style="height:16px"></div>')
h.append("<h2>Fonts</h2><div class=\"fonts\">")
for n, w, s in FONTS:
    h.append(f'<div style="font-weight:{w};font-style:{s}">TWK Everett {n.replace("-", " ").capitalize()}</div><a href="{BASE}fonts/twk-everett-{n}.ttf">{BASE}fonts/twk-everett-{n}.ttf</a>')
h.append("</div><pre>")
for n, w, s in FONTS:
    h.append(html.escape(f'@font-face {{ font-family: "TWK Everett"; src: url("{BASE}fonts/twk-everett-{n}.ttf") format("truetype"); font-weight: {w}; font-style: {s}; }}'))
h.append("</pre>\n</main>\n</body>\n</html>\n")
(ROOT / "index.html").write_text("\n".join(h), encoding="utf-8")
print("ok", BASE)
