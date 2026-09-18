# -*- coding: utf-8 -*-
"""Rebuild the three logo assets from the supplied PAM ADMIN artwork.

Geometry is taken from a pixel census of the source PNG rather than guessed:

  icon      chip outline x 4..25, y 4..25, wall ~3.6px, corners ~r5
  pins      three per side, 2px wide, 4px long, 5px apart, centred on 14.75
  "AI"      inside the chip, bbox x 8..21, y 10..19  (cap height 10)
  wordmark  bbox x 34..150, y 8..21  (cap height 14, baseline 22)
  canvas    152 x 30

Both lettering runs are converted to outlines, so the files carry no font
dependency and render identically inside an <img> tag, where page CSS and
webfonts cannot reach.
"""
import re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

FONT   = "C:/Windows/Fonts/arialbd.ttf"
ORANGE = "#F26522"
DARK   = "#3D3B3B"
DEST   = "C:/Users/PAM-BÜRO/Documents/Claude/Projects/PAM-ADMIN/assets/img/"

CX = 14.75                     # icon centre, both axes
_f  = TTFont(FONT)
_gs = _f.getGlyphSet()
_cm = _f.getBestCmap()
_hm = _f["hmtx"]
_bp = BoundsPen(_gs); _gs[_cm[ord("P")]].draw(_bp)
CAP_UNITS = _bp.bounds[3]


def outline(text, cap_h, start_x, baseline, target_w=None):
    """Draw `text` as SVG path data, optionally tracked to an exact width."""
    scale = cap_h / CAP_UNITS
    names = [_cm[ord(c)] for c in text]
    adv   = [_hm[n][0] * scale for n in names]
    gaps  = max(len(names) - 1, 1)
    track = ((target_w - sum(adv)) / gaps) if target_w else 0.0

    parts, x = [], start_x
    for n, a in zip(names, adv):
        pen = SVGPathPen(_gs)
        _gs[n].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, x, baseline)))
        if pen.getCommands(): parts.append(pen.getCommands())
        x += a + track
    d = " ".join(parts)
    return re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group()):.2f}".rstrip("0").rstrip("."), d)


def chip(cx=CX, cy=CX):
    """The processor mark: rounded-square outline plus three pins per side."""
    body = (f'<rect x="{cx-9.15:.2f}" y="{cy-9.15:.2f}" width="18.3" height="18.3" '
            f'rx="4.6" fill="none" stroke="{ORANGE}" stroke-width="3.6"/>')
    pins = []
    for off in (-5, 0, 5):                       # pin centres, 5px apart
        p = cx + off
        pins.append(f'<rect x="{p-1:.2f}" y="{cy-13.75:.2f}" width="2" height="4.6" rx="0.7" fill="{ORANGE}"/>')
        pins.append(f'<rect x="{p-1:.2f}" y="{cy+9.15:.2f}"  width="2" height="4.6" rx="0.7" fill="{ORANGE}"/>')
        pins.append(f'<rect x="{cx-13.75:.2f}" y="{p-1:.2f}" width="4.6" height="2" rx="0.7" fill="{ORANGE}"/>')
        pins.append(f'<rect x="{cx+9.15:.2f}"  y="{p-1:.2f}" width="4.6" height="2" rx="0.7" fill="{ORANGE}"/>')
    ai = outline("AI", cap_h=10.0, start_x=cx - 6.5, baseline=cy + 5.0, target_w=13.0)
    return body + "".join(pins) + f'<path d="{ai}" fill="{ORANGE}"/>'


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


if __name__ == "__main__":
    word = outline("PAM ADMIN", cap_h=14.0, start_x=34.0, baseline=22.0, target_w=116.0)
    files = {
        "logo.svg":       svg(152, 30, chip() + f'<path d="{word}" fill="{DARK}"/>',  "PAM ADMIN"),
        "logo-white.svg": svg(152, 30, chip() + f'<path d="{word}" fill="#FFFFFF"/>', "PAM ADMIN"),
        "logo-small.svg": svg(30,  30, chip(),                                        "PAM ADMIN"),
    }
    for name, content in files.items():
        open(DEST + name, "w", encoding="utf-8").write(content)
        print(f"  {name:16s} {len(content):6d} bytes")
