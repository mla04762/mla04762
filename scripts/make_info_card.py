#!/usr/bin/env python3
"""
Hand-author a neofetch-style info card SVG for the profile README: a terminal
title bar, then colored key/value rows that fade + slide in on a short stagger,
finishing with a classic neofetch color-palette strip.

Static content -- regenerate only when the details change:
    python scripts/make_info_card.py            # writes info-card.svg
    STATIC=1 python scripts/make_info_card.py   # frozen frame (no animation)
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = os.environ.get("STATIC") == "1"

# ---- palette (matches wordmark + heatmap) -----------------------------------
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
MUTED = "#7d8590"
KEY = "#22d3ee"      # cyan keys, like neofetch labels
AT = "#39d353"       # green for user@host
DIM = "#8b949e"

# ---- content ----------------------------------------------------------------
USERHOST = ("kieun", "@", "kissusa")
ROWS = [
    ("Name",  "Kieun Kim"),
    ("Role",  "IT Systems Administrator"),
    ("Org",   "KISS Beauty Group · IT Support Center"),
    ("Focus", "endpoint management · automation · internal tooling"),
    ("MDM",   "Microsoft Intune — company device fleet"),
    ("Now",   "ITSC Bot — Webex helpdesk assistant"),
    ("Also",  "AI invoice automation (SAP Concur) · Workday HR chatbot"),
    ("Stack", "Python · React · Microsoft 365 · GitHub Actions"),
    ("Daily", "new-hire setups · asset tracking · internal docs"),
]
PALETTE_STRIP = ["#ff5f56", "#ffbd2e", "#27c93f", "#22d3ee",
                 "#1f6feb", "#a371f7", "#f778ba", "#c9d1d9"]

# ---- geometry ---------------------------------------------------------------
CANVAS_W = 1026            # matches the wordmark panel so the pair lines up
PAD = 26
TITLEBAR_H = 28
LINE_H = 30
FS = 16                    # monospace font size
KEY_W = 96                 # px column where values start (after the key)
TOP_GAP = 18

STAGGER = 0.16             # seconds between rows
ROW_DUR = 0.5


def esc(s):
    return html.escape(s, quote=True)


def main():
    n_lines = 1 + 1 + len(ROWS) + 1 + 1   # user@host, rule, rows, gap, palette
    art_h = TOP_GAP + n_lines * LINE_H + PAD * 0.4
    canvas_h = int(TITLEBAR_H + art_h + PAD * 0.5)

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{canvas_h}" '
        f'viewBox="0 0 {CANVAS_W} {canvas_h}" font-family="ui-monospace, SFMono-Regular, '
        f'Menlo, Consolas, monospace">',
        '<defs><linearGradient id="cbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        '</linearGradient></defs>',
    ]
    if not STATIC:
        p.append(
            '<style>@keyframes row{0%{opacity:0;transform:translateX(-10px)}'
            '100%{opacity:1;transform:translateX(0)}}'
            f'.r{{opacity:0;animation:row {ROW_DUR}s cubic-bezier(.2,.8,.2,1) both}}</style>'
        )
    p += [
        f'<rect width="{CANVAS_W}" height="{canvas_h}" rx="12" fill="url(#cbg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{canvas_h-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        p.append(f'<circle cx="{PAD + i*15}" cy="{TITLEBAR_H/2}" r="4.5" fill="{dot}"/>')
    p.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" '
             f'font-size="11.5" text-anchor="middle">kieun@github: ~$ neofetch</text>')

    cls = '' if STATIC else ' class="r"'
    y = TITLEBAR_H + TOP_GAP + LINE_H * 0.7
    li = 0

    def delay():
        return '' if STATIC else f' style="animation-delay:{0.15 + li * STAGGER:.2f}s"'

    # user@host header
    u, at, h = USERHOST
    p.append(f'<text{cls}{delay()} x="{PAD}" y="{y:.0f}" font-size="{FS}" font-weight="700">'
             f'<tspan fill="{AT}">{u}</tspan><tspan fill="{INK}">{at}</tspan>'
             f'<tspan fill="{AT}">{h}</tspan></text>')
    li += 1
    y += LINE_H
    # separator rule, sized to user@host
    p.append(f'<text{cls}{delay()} x="{PAD}" y="{y:.0f}" font-size="{FS}" '
             f'fill="{DIM}">{"-" * (len(u) + len(at) + len(h))}</text>')
    li += 1
    y += LINE_H

    for key, val in ROWS:
        p.append(f'<text{cls}{delay()} x="{PAD}" y="{y:.0f}" font-size="{FS}">'
                 f'<tspan fill="{KEY}" font-weight="700">{esc(key)}</tspan>'
                 f'<tspan fill="{DIM}">: </tspan>'
                 f'<tspan fill="{INK}" x="{PAD + KEY_W}">{esc(val)}</tspan></text>')
        li += 1
        y += LINE_H

    # palette strip
    y += LINE_H * 0.4
    sw, gap = 34, 6
    g = f'<g{cls}{delay()}>' if not STATIC else "<g>"
    blocks = "".join(
        f'<rect x="{PAD + i*(sw+gap)}" y="{y - 14:.0f}" width="{sw}" height="18" rx="3" fill="{c}"/>'
        for i, c in enumerate(PALETTE_STRIP)
    )
    p.append(g + blocks + "</g>")

    p.append("</svg>")
    svg = "".join(p)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}  {len(svg)/1024:.1f} KB  {CANVAS_W}x{canvas_h}")


if __name__ == "__main__":
    main()
