#!/usr/bin/env python3
"""Generate the cover's in-situ chain traces.

Exports 1-bit silhouettes to assets/images/bg/traces/ and writes the partial
layouts/_partials/fx/chain.html.

    python3 tools/gen-traces.py --seed 3 --count 5

What this makes: the artwork's own secondary structures lighting up, one chain
at a time, exactly where they already are. Nothing is duplicated and nothing is
invented — each silhouette is laid back over the structure it was cut from, and
what animates is a light travelling along that structure's backbone.

Everything else was tried first and is worse:

* Drawing shapes by hand. A smooth curve beside pixel art reads as a foreign
  object, and a hand-built pixel helix loses the occlusion between near and far
  turns that is the only reason a coil is legible.
* Cutting structures out and redrawing them somewhere else. That is a clone
  stamp: the same shape appears twice in one picture. It also targets the empty
  lower third, which does not exist above ~2100px wide — `max-height` crops the
  band before it gets there.

Sizing and rhythm are derived, not guessed:

* The stroke that reveals a chain is 7 cells wide, chosen as the smallest width
  that covers >=97% of every accepted structure's cells. Narrower leaves cells
  permanently dark.
* Each period is proportional to its chain's length, so the light travels at
  the same ~7.5 cells/s along all of them, from one keyframe set.
* Periods are snapped to distinct primes, so the group never falls into a
  repeating rhythm.
"""

import argparse
import math
import os
import random
from collections import deque

from PIL import Image, ImageDraw

SRC = "assets/images/bg/background-cover.png"
OUTDIR = "assets/images/bg/traces"
PARTIAL = "layouts/_partials/fx/chain.html"

PITCH = 7        # the artwork's cell pitch, in source px
SQUARE = 6       # lit part of a cell; the remainder is the grid gap
LIT = 42         # luminance above which a cell belongs to a structure
STROKE_CELLS = 7  # reveal stroke width
MIN_COVER = 0.97  # a structure is rejected if the stroke misses more than this
MIN_CELLS = 40
CELLS_PER_SEC = 7.5
DRAW_FRACTION = 0.10  # share of the period spent drawing
PRIMES = [17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83]


def cell_grid(im):
    """Quantise the artwork back onto its own grid, recovering the phase."""
    w, h = im.size
    best = None
    for ox in range(PITCH):
        for oy in range(PITCH):
            s = 0
            for cy in range(5, 95, 7):
                for cx in range(5, 300, 7):
                    x, y = ox + cx * PITCH + PITCH // 2, oy + cy * PITCH + PITCH // 2
                    if x < w and y < h:
                        s += sum(im.getpixel((x, y)))
            if best is None or s > best[0]:
                best = (s, ox, oy)
    _, ox, oy = best
    cols, rows = (w - ox) // PITCH, (h - oy) // PITCH
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            box = (ox + c * PITCH + 1, oy + r * PITCH + 1,
                   ox + c * PITCH + PITCH - 1, oy + r * PITCH + PITCH - 1)
            d = list(im.crop(box).getdata())
            row.append(sum(sum(p) for p in d) / (3 * len(d)))
        grid.append(row)
    return grid, rows, cols, ox, oy


def components(grid, rows, cols):
    seen = [[False] * cols for _ in range(rows)]
    out = []
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] > LIT and not seen[r0][c0]:
                seen[r0][c0] = True
                q, cs = deque([(r0, c0)]), []
                while q:
                    r, c = q.popleft()
                    cs.append((r, c))
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            r2, c2 = r + dr, c + dc
                            if (0 <= r2 < rows and 0 <= c2 < cols
                                    and grid[r2][c2] > LIT and not seen[r2][c2]):
                                seen[r2][c2] = True
                                q.append((r2, c2))
                out.append(cs)
    return out


def bfs(cs, start):
    adj, dist, q = set(cs), {start: 0}, deque([start])
    while q:
        r, c = q.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                n = (r + dr, c + dc)
                if n in adj and n not in dist:
                    dist[n] = dist[(r, c)] + 1
                    q.append(n)
    return dist


def centreline(cs):
    """Polyline end to end along the chain, plus its length in cells."""
    d0 = bfs(cs, cs[0])
    far = max(d0, key=d0.get)
    d = bfs(cs, far)
    bins = {}
    for cell, hops in d.items():
        bins.setdefault(hops, []).append(cell)
    # Per-hop centroids track the chain even where the ribbon is several cells
    # wide; a 3-tap mean settles the jitter where the width changes.
    pts = [(sum(c for _, c in b) / len(b), sum(r for r, _ in b) / len(b))
           for _, b in sorted(bins.items())]
    sm = []
    for i in range(len(pts)):
        w = pts[max(0, i - 1):i + 2]
        sm.append((sum(p[0] for p in w) / len(w), sum(p[1] for p in w) / len(w)))
    return sm, max(d.values())


def coverage(cs, line):
    """Share of the structure's cells within half a stroke of the centreline."""
    half = STROKE_CELLS / 2
    hit = 0
    for r, c in cs:
        for i in range(len(line) - 1):
            (x0, y0), (x1, y1) = line[i], line[i + 1]
            dx, dy = x1 - x0, y1 - y0
            L = dx * dx + dy * dy
            t = 0 if L == 0 else max(0, min(1, ((c - x0) * dx + (r - y0) * dy) / L))
            if math.hypot(c - (x0 + t * dx), r - (y0 + t * dy)) <= half:
                hit += 1
                break
    return hit / len(cs)


def silhouette(cs, path):
    """1-bit mask of the structure's cells, at the artwork's own pitch."""
    rs = [r for r, _ in cs]
    ct = [c for _, c in cs]
    r0, c0 = min(rs), min(ct)
    w, h = max(ct) - c0 + 1, max(rs) - r0 + 1
    im = Image.new("LA", (w * PITCH, h * PITCH), (0, 0))
    d = ImageDraw.Draw(im)
    for r, c in cs:
        x, y = (c - c0) * PITCH, (r - r0) * PITCH
        d.rectangle([x, y, x + SQUARE - 1, y + SQUARE - 1], fill=(255, 255))
    im.save(path, optimize=True)
    return w, h, r0, c0


HEAD = '''{{{{- /*
  In-situ chain traces. Generated by tools/gen-traces.py (seed {seed}).

  The shapes are the artwork's own. The cover is quantised back onto its 7px
  cell grid, flood-filled into {ncomp} connected components, and {n} of them are
  exported as 1-bit silhouettes. Each is laid back exactly over the structure it
  was cut from, so nothing is duplicated and nothing is invented — the picture
  simply lights up along one chain at a time, from the head of that chain.

  Each silhouette masks a stroke drawn along the structure's own centreline
  (found by BFS through the cell adjacency), and `pathLength="1"` normalises
  every chain, so one keyframe set drives them all. Periods are proportional to
  chain length, which makes the light travel at the same speed along each, and
  are distinct primes, so the group never falls into a rhythm.

  Registration lives in css/main.css (§ cover): `.fx-chain` is laid out as the
  artwork's rendered rectangle rather than as the band, so every child is placed
  in plain % of the {sw}x{sh} source and stays exact at any viewport width.

  Tunables live on `.fx-chain` in css/main.css (§ cover).
*/ -}}}}
<div class="fx-chain" aria-hidden="true">'''

SVG = '''
  {{{{- with resources.Get "images/bg/traces/{name}.png" }}}}
  <svg class="cm" viewBox="0 0 {w} {h}" preserveAspectRatio="none"
    aria-hidden="true" focusable="false"
    style="--x: {x:.3f}%; --y: {y:.3f}%; --w: {pw:.3f}%; --h: {ph:.3f}%; --d: {d}s; --dl: -{dl}s">
    <mask id="tc{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
      <image href="{{{{ .RelPermalink }}}}" width="{w}" height="{h}" />
    </mask>
    <path class="cm-run" mask="url(#tc{i})" d="{chain}" pathLength="1" fill="none"
      stroke-width="{sw}" stroke-linecap="butt" stroke-linejoin="round" />
  </svg>
  {{{{- end }}}}'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--count", type=int, default=5)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    im = Image.open(SRC).convert("RGB")
    SW, SH = im.size
    grid, rows, cols, ox, oy = cell_grid(im)
    comps = components(grid, rows, cols)

    ok = []
    for cs in comps:
        if len(cs) < MIN_CELLS:
            continue
        line, chain_cells = centreline(cs)
        if len(line) < 4 or coverage(cs, line) < MIN_COVER:
            continue
        ct = [c for _, c in cs]
        ok.append((cs, line, chain_cells, sum(ct) / len(ct)))
    print(f"{len(comps)} structures, {len(ok)} pass the >={MIN_COVER:.0%} "
          f"coverage test at a {STROKE_CELLS}-cell stroke")

    # Spread the picks across the width so the events are not all in one place.
    ok.sort(key=lambda t: t[3])
    n = min(args.count, len(ok))
    chosen = []
    for k in range(n):
        lo = int(len(ok) * k / n)
        hi = max(lo + 1, int(len(ok) * (k + 1) / n))
        chosen.append(max(ok[lo:hi], key=lambda t: len(t[0])))

    os.makedirs(OUTDIR, exist_ok=True)
    for f in os.listdir(OUTDIR):
        os.remove(os.path.join(OUTDIR, f))

    used = set()
    parts = [HEAD.format(seed=args.seed, ncomp=len(comps), n=n, sw=SW, sh=SH)]
    total = 0
    for i, (cs, line, chain_cells, _) in enumerate(chosen):
        name = f"s{i}"
        w, h, r0, c0 = silhouette(cs, os.path.join(OUTDIR, name + ".png"))
        total += os.path.getsize(os.path.join(OUTDIR, name + ".png"))
        # Period from chain length, so every trace travels at the same speed.
        want = chain_cells / CELLS_PER_SEC / DRAW_FRACTION
        period = min((p for p in PRIMES if p not in used),
                     key=lambda p: (abs(p - want), p))
        used.add(period)
        d = "M" + "L".join(
            f"{(x - c0) * PITCH + PITCH // 2:.0f} {(y - r0) * PITCH + PITCH // 2:.0f}"
            for x, y in line)
        parts.append(SVG.format(
            i=i, name=name, w=w * PITCH, h=h * PITCH,
            x=(ox + c0 * PITCH) / SW * 100, y=(oy + r0 * PITCH) / SH * 100,
            pw=w * PITCH / SW * 100, ph=h * PITCH / SH * 100,
            d=period, dl=rng.randrange(period), chain=d,
            sw=STROKE_CELLS * PITCH))
        print(f"  {name}  {len(cs):4d} cells  chain {chain_cells:3d}  "
              f"period {period:2d}s  draw {period * DRAW_FRACTION:.1f}s  "
              f"({chain_cells / (period * DRAW_FRACTION):.1f} cells/s)")
    parts.append("\n</div>\n")
    open(PARTIAL, "w").write("".join(parts))
    print(f"wrote {PARTIAL} ({len(''.join(parts))} bytes) "
          f"+ {n} silhouettes ({total} bytes)")


if __name__ == "__main__":
    main()
