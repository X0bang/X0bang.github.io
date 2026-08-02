#!/usr/bin/env python3
"""Draw the maps used to check structure detection by eye.

Run from the repository root:

    python3 structure-analysis/render_map.py

Writes into structure-analysis/out/:

    numbered.png   every element numbered and coloured by class, with every
                   cell the animation never touches in red. The banner is cut
                   in half and stacked so the labels are legible.
    classes.png    the same colouring without labels, at full width.
    elements.json  one record per element, for reference without re-running.

The numbers match the s0..sN silhouettes gen_traces.py writes, because both
sort the same way.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect import (LIT, MAX_STROKE, MAX_STROKE_RATIO, MIN_CELLS,
                    NARROW_STROKE, PITCH, SQUARE, SRC, cell_grid, centreline,
                    classify, elements, stroke_cells)
from gen_traces import load_groups
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
# Loops are detected but never lit, so they are not drawn here either — the
# numbering has to match the s0..sN the generator writes.
COLOUR = {"helix": (80, 245, 140), "strand": (80, 175, 255),
          "turn": (255, 190, 70)}
UNCOVERED = (255, 60, 60, 200)
K = 2  # the labels are unreadable at 1:1


def collect(grid, rows, cols):
    """The elements the animation will actually use, in the same order."""
    out = []
    for cs in elements(grid, rows, cols):
        if len(cs) < MIN_CELLS:
            continue
        line, chain = centreline(cs)
        if len(line) < 3:
            continue
        kind = classify(cs, line, chain)
        if kind not in COLOUR:
            continue
        sw = stroke_cells(cs, line)
        if sw > MAX_STROKE or (sw > NARROW_STROKE
                               and sw / max(1, chain) > MAX_STROKE_RATIO):
            continue
        out.append({"cells": cs, "line": line, "kind": kind,
                    "chain": chain, "stroke": sw})
    out = load_groups(out)      # same grouping the generator applies
    out.sort(key=lambda e: e["chain"])
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    im = Image.open(SRC).convert("RGB")
    grid, rows, cols, ox, oy = cell_grid(im)
    picked = collect(grid, rows, cols)

    lit = {(r, c) for r in range(rows) for c in range(cols) if grid[r][c] > LIT}
    covered = set()
    for e in picked:
        covered.update(e["cells"])

    canvas = im.resize((im.width * K, im.height * K), Image.NEAREST).convert("RGBA")
    over = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)

    def stamp(cells, colour):
        for r, c in cells:
            x, y = (ox + c * PITCH) * K, (oy + r * PITCH) * K
            d.rectangle([x, y, x + SQUARE * K - 1, y + SQUARE * K - 1], fill=colour)

    for e in picked:
        stamp(e["cells"], COLOUR[e["kind"]] + (215,))
    stamp(lit - covered, UNCOVERED)
    canvas = Image.alpha_composite(canvas, over)
    canvas.convert("RGB").save(os.path.join(OUT, "classes.png"))

    d = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
    except OSError:
        font = ImageFont.load_default()
    for i, e in enumerate(picked):
        rs = [r for r, _ in e["cells"]]
        ct = [c for _, c in e["cells"]]
        cx = (ox + sum(ct) / len(ct) * PITCH) * K
        cy = (oy + sum(rs) / len(rs) * PITCH) * K
        for dx in (-2, 0, 2):          # a halo, or the label vanishes on a bright cell
            for dy in (-2, 0, 2):
                d.text((cx + dx, cy + dy), str(i), font=font,
                       fill=(0, 0, 0, 255), anchor="mm")
        d.text((cx, cy), str(i), font=font, fill=(255, 255, 255), anchor="mm")

    half = canvas.width // 2
    stacked = Image.new("RGB", (half, canvas.height * 2 + 14), (22, 22, 26))
    stacked.paste(canvas.crop((0, 0, half, canvas.height)).convert("RGB"), (0, 0))
    stacked.paste(canvas.crop((half, 0, canvas.width, canvas.height)).convert("RGB"),
                  (0, canvas.height + 14))
    stacked.save(os.path.join(OUT, "numbered.png"))

    json.dump([{"n": i, "kind": e["kind"], "cells": len(e["cells"]),
                "chain": e["chain"], "stroke": round(e["stroke"], 1)}
               for i, e in enumerate(picked)],
              open(os.path.join(OUT, "elements.json"), "w"), indent=1)

    counts = {}
    for e in picked:
        counts[e["kind"]] = counts.get(e["kind"], 0) + 1
    print(f"{len(picked)} elements: " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    print(f"covered {len(covered)}/{len(lit)} = {len(covered) / len(lit):.0%} of lit cells")
    print(f"wrote {OUT}/numbered.png, classes.png, elements.json")


if __name__ == "__main__":
    main()
