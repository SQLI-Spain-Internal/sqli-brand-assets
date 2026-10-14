# SQLI brand assets

Public repository of SQLI's basic brand files, served by GitHub Pages so each file has a stable URL
for email signatures, websites and Claude Design pages.

- Repository: https://github.com/SQLI-Spain-Internal/sqli-brand-assets (public)
- Pages: https://sqli-spain-internal.github.io/sqli-brand-assets/
- Source of every rule: SQLI Brand Guidelines v1.1 (February 2026). Page numbers like p13 refer to it.

Everything in this repository is public. Never commit credentials, internal links, client names or
anything that is not a brand file or its documentation. Local notes go in `CLAUDE.local.md`, which is
ignored by git.

## Layout

| Folder | Content |
|---|---|
| `logo/` | The logotype in Midnight, Cobalt, Cream and Sky, plus safe-zone versions. SVG and PNG. |
| `ascenders/` | The two ascender bars in the four brand colours. SVG and PNG. |
| `promise/` | "Elevate. Digitally" on one or two lines, with and without ascenders. SVG and PNG. |
| `icons/cobalt/`, `icons/sky/` | The official icon set, same file names in both folders. SVG, and PNG at 120 px for emails. |
| `fonts/` | TWK Everett Light, Light Italic, Regular, Regular Italic, Medium. |
| `tools/` | `build_png.py` renders the PNGs, `build_docs.py` writes README.md and index.html. |

`.nojekyll` makes Pages publish the files as they are. Keep it.

## Rules for any change

- Official files only. Never redraw, recolour, stretch or "improve" an asset. The only exceptions are
  the files listed in `BUILT` in `tools/build_docs.py`: keep that list complete.
- Public text (README, index.html) must not depend on internal material: no brand book page numbers,
  internal folder names or links readers cannot open. Page numbers belong in code comments.
- File names: lowercase, hyphens, no spaces, `<asset>-<colour>[-variant]`. Never rename a published
  file: people link to these URLs. Add a new name instead.
- Every SVG in `logo/`, `ascenders/` and `promise/` has a PNG next to it, and an entry in the tables of
  `tools/build_docs.py` with the backgrounds the brand book approves it on (p13, p14, p15, p27, p28).
- Fonts: only the five weights above. No Bold, no other families.
- Brand colours: Cream #FFFAF0, Midnight Blue #0F0E2B, Sky Blue #6DA5FF, Cobalt Blue #1F24E9, plus
  White and Black. No tints, gradients or transparency.
- Logo colour per background: on Cream, Midnight or Cobalt. On Midnight, Cream or Sky. On Sky,
  Midnight. On Cobalt, Cream.
- The company is written SQLI in text. The logo is always the lower-case mark, never typed.

## Workflow

1. Add or replace SVGs in their folder.
2. `python3 tools/build_png.py` (needs `pip install pymupdf`).
3. Update the tables in `tools/build_docs.py`, then `python3 tools/build_docs.py`.
4. Open `index.html` locally and check every preview sits on an approved background.
5. Commit and push to `main`. Pages rebuilds in about a minute. Check a changed URL with
   `curl -sI <url>`: it should return 200 and the right content type (`image/svg+xml`, `image/png`,
   `font/ttf`).

Documentation style: English, sentence-case headings, plain sentences, no em dashes, no semicolons.
