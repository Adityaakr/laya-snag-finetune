"""Hand-drawn (Excalidraw / Miro style) pipeline diagram for the laya-snag-finetune README.

Deterministic jitter gives sketchy double strokes; pastel sticky notes; curved arrows; handwriting font stack that
exists on macOS (Chalkboard SE, Bradley Hand), Windows (Segoe Print) and falls back to cursive. The SVG carries its
own background so it stays readable in GitHub's dark and light themes.
"""

import math
import random

random.seed(7)
W, H = 1180, 760
INK = "#1e1e2e"
FONT = "'Chalkboard SE','Segoe Print','Bradley Hand','Comic Sans MS','Comic Neue',cursive"
out = []


def j(v, a=1.6):
    return v + random.uniform(-a, a)


def rough_rect(x, y, w, h, fill, stroke=INK, r=14, width=2.2):
    """Two slightly different rounded rectangles: the sketchy look."""
    parts = []
    for k in range(2):
        a = 1.4 if k == 0 else 2.2
        x0, y0, x1, y1 = j(x, a), j(y, a), j(x + w, a), j(y + h, a)
        d = (
            f"M{x0 + r:.1f},{y0:.1f} L{x1 - r:.1f},{j(y0, .8):.1f} Q{x1:.1f},{y0:.1f} {x1:.1f},{y0 + r:.1f} "
            f"L{j(x1, .8):.1f},{y1 - r:.1f} Q{x1:.1f},{y1:.1f} {x1 - r:.1f},{y1:.1f} "
            f"L{x0 + r:.1f},{j(y1, .8):.1f} Q{x0:.1f},{y1:.1f} {x0:.1f},{y1 - r:.1f} "
            f"L{j(x0, .8):.1f},{y0 + r:.1f} Q{x0:.1f},{y0:.1f} {x0 + r:.1f},{y0:.1f} Z"
        )
        if k == 0:
            parts.append(f'<path d="{d}" fill="{fill}" stroke="none"/>')
        parts.append(
            f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width if k == 0 else width * .6:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{1 if k == 0 else .55}"/>'
        )
    out.extend(parts)


def sticky(x, y, w, h, fill, angle=0):
    cx, cy = x + w / 2, y + h / 2
    out.append(f'<g transform="rotate({angle} {cx} {cy})">')
    out.append(f'<rect x="{x + 5}" y="{y + 7}" width="{w}" height="{h}" rx="6" fill="#000" opacity=".10"/>')
    rough_rect(x, y, w, h, fill, r=8)
    out.append("</g>")


def text(x, y, s, size=22, weight=400, fill=INK, anchor="middle", opacity=1):
    out.append(
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" opacity="{opacity}">{s}</text>'
    )


def arrow(x0, y0, x1, y1, bend=0.0, color=INK, width=2.4, dashed=False):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    cx, cy = mx + nx * bend * L, my + ny * bend * L
    dash = ' stroke-dasharray="7 7"' if dashed else ""
    for k in range(2):
        a = .9 if k == 0 else 1.6
        out.append(
            f'<path d="M{j(x0, a):.1f},{j(y0, a):.1f} Q{j(cx, a):.1f},{j(cy, a):.1f} {x1:.1f},{y1:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{width if k == 0 else width * .55:.1f}" '
            f'stroke-linecap="round" opacity="{1 if k == 0 else .5}"{dash}/>'
        )
    tx, ty = x1 - cx, y1 - cy
    t = math.hypot(tx, ty) or 1
    ux, uy = tx / t, ty / t
    for s in (1, -1):
        hx = x1 - ux * 16 + (-uy) * 8 * s
        hy = y1 - uy * 16 + ux * 8 * s
        out.append(f'<path d="M{hx:.1f},{hy:.1f} L{x1:.1f},{y1:.1f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')


def chip(x, y, label, fill):
    w = 22 + 10.6 * len(label)
    rough_rect(x, y, w, 34, fill, r=16, width=1.6)
    text(x + w / 2, y + 23, label, size=17)
    return w


# Canvas
out.append(f'<rect width="{W}" height="{H}" rx="28" fill="#fffdf7"/>')
for gx in range(40, W, 36):  # dotted board, Miro style
    for gy in range(40, H, 36):
        out.append(f'<circle cx="{gx}" cy="{gy}" r="1.2" fill="#d9d4c7"/>')

text(W / 2, 62, "How Snag asks an engine about a pull request", size=30, weight=700)
text(W / 2, 94, "Laya is the local engine this repository tries to fine-tune", size=18, opacity=.65)

# Inputs (sticky notes)
sticky(60, 140, 170, 92, "#ffe8a3", -2)
text(145, 182, "Issue", size=26, weight=700)
text(145, 210, "what was asked", size=16, opacity=.7)
sticky(60, 300, 170, 92, "#bfe3ff", 2)
text(145, 342, "Diff", size=26, weight=700)
text(145, 370, "what changed", size=16, opacity=.7)

# Stage boxes
rough_rect(310, 145, 250, 82, "#ffffff")
text(435, 180, "Requirement", size=21, weight=700)
text(435, 206, "extraction", size=21, weight=700)
rough_rect(310, 305, 250, 82, "#ffffff")
text(435, 340, "Change units", size=21, weight=700)
text(435, 366, "tree-sitter per function", size=15, opacity=.7)

sticky(640, 145, 200, 82, "#fff3c4", 1.5)
text(740, 180, "Requirements", size=21, weight=700)
text(740, 206, "each with a quote", size=15, opacity=.7)

arrow(232, 186, 306, 186)
arrow(232, 346, 306, 346)
arrow(562, 186, 636, 186)

# Typed questions (the heart)
rough_rect(640, 290, 500, 150, "#f1ecff")
text(890, 326, "Typed questions per requirement", size=22, weight=700)
cx = 666
for label, fill in (("coverage", "#ffffff"), ("conflict", "#ffffff"), ("evidence", "#ffffff"), ("tests", "#ffffff")):
    cx += chip(cx, 348, label, fill) + 12
text(890, 418, "answered with a probability for every option", size=15, opacity=.7)

arrow(740, 230, 760, 286, bend=.1)
arrow(562, 350, 636, 360, bend=-.05)

# Engine
rough_rect(640, 492, 470, 104, "#d8f5e1")
text(875, 530, "Engine", size=24, weight=700)
text(875, 560, "Jev  ·  Laya (local, this repo)  ·  an LLM", size=17)
sticky(1000, 470, 140, 46, "#ffc9d6", 6)
text(1070, 500, "fine-tuned here", size=15, weight=700)
arrow(875, 442, 875, 488)

# Outputs
rough_rect(60, 640, 250, 76, "#ffffff")
text(185, 672, "Answer", size=20, weight=700)
text(185, 698, "probabilities", size=20, weight=700)
rough_rect(400, 640, 220, 76, "#ffffff")
text(510, 685, "Verdict rules", size=21, weight=700)
sticky(712, 634, 290, 88, "#c8f0c8", -1.5)
text(857, 671, "Findings", size=24, weight=700)
text(857, 701, "done · partial · missing · contradicted", size=15, opacity=.75)

arrow(636, 560, 250, 636, bend=.12)
arrow(312, 678, 396, 678)
arrow(622, 678, 708, 678)

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-label="Snag pipeline: issue and diff become requirements and change units, typed questions go '
    f'to an engine (Jev, Laya or an LLM), answer probabilities pass through verdict rules to findings">'
    + "".join(out)
    + "</svg>"
)
open(__import__("os").path.join(__import__("os").path.dirname(__file__), "pipeline.svg"), "w").write(svg)
print(len(svg), "bytes")
