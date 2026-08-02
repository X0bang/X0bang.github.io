#!/usr/bin/env python3
"""Generate the cover's in-situ chain traces.

Exports 1-bit silhouettes to assets/images/bg/traces/ and writes the partial
layouts/_partials/fx/chain.html.

    python3 tools/gen-traces.py --seed 3

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

* Structures are classified first — helix, strand, turn, loop, fragment — from
  mean ribbon width, how far the chain doubles back on itself, and how many
  times it reverses direction. Of 213 components only 19 are real secondary
  structure; the other 185 are single-cell noise carrying 16% of the lit area.
  All 19 are animated, so the picture lights up everywhere it has structure
  rather than in five places.
* Each stroke is sized from its own structure's widest point, so every cell is
  reachable. A single width for all of them either leaves cells permanently
  dark or bleeds far past the thin ones.
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
MIN_CELLS = 20        # below this a component is noise, not structure
# Wider than this and the stroke floods the whole component at once. Short,
# stubby structures where the stroke approaches the chain length are kept: they
# simply read as lighting up as a unit, which for a two-turn fragment is right.
MAX_STROKE = 16.0
CELLS_PER_SEC = 7.5   # chain speed, held constant across every structure
DRAW_FRACTION = 0.08  # share of the period spent drawing
# With 19 traces each lit for ~11% of its period, about two are alight at once.
PRIMES = [13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
          83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]


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


def split4(cs):
    """Re-split a component using 4-connectivity.

    Structures that merely touch at a corner are one component under the
    8-connected fill. That is usually what is wanted — it keeps a diagonal
    ribbon whole — but where several structures pile up it produces a blob with
    no meaningful chain through it. Dropping the diagonals separates them
    without fragmenting the ribbons, so this is used only as a fallback."""
    adj, seen, parts = set(cs), set(), []
    for start in cs:
        if start in seen:
            continue
        seen.add(start)
        q, cur = deque([start]), []
        while q:
            r, c = q.popleft()
            cur.append((r, c))
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (r + dr, c + dc)
                if n in adj and n not in seen:
                    seen.add(n)
                    q.append(n)
        parts.append(cur)
    return parts


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


def stroke_cells(cs, line):
    """Stroke wide enough to reach the structure, sized off its 95th-percentile
    cell rather than its furthest. One cell in a blob's far corner would
    otherwise set a width half the chain's length, and a stroke that wide
    uncovers the whole shape at once — there is no travelling light left."""
    d = []
    for r, c in cs:
        best = 1e9
        for i in range(len(line) - 1):
            (x0, y0), (x1, y1) = line[i], line[i + 1]
            dx, dy = x1 - x0, y1 - y0
            L = dx * dx + dy * dy
            t = 0 if L == 0 else max(0, min(1, ((c - x0) * dx + (r - y0) * dy) / L))
            best = min(best, math.hypot(c - (x0 + t * dx), r - (y0 + t * dy)))
        d.append(best)
    d.sort()
    return 2 * d[int(len(d) * 0.95)] + 1.2


def classify(cs, line, chain):
    """helix | strand | turn | loop | fragment, from the chain's own shape.

    Two measurements separate them cleanly on this artwork:

      straightness  end-to-end distance over chain length. A beta-strand runs
                    >= 0.94; everything that coils back sits at 0.38-0.80.
      turning       total absolute heading change along the chain. A single
                    turn of a coil is 2*pi, so anything past ~5 rad is winding.
                    Strands measure 2.3-5.8, coils 4.0-22.5.

    Counting axis reversals instead — the obvious approach — misses a coil
    standing vertically, because it never reverses in x.
    """
    n = len(cs)
    if n < 10:
        return "fragment"
    if n / max(1, chain) < 1.9:      # one or two cells wide: a connector
        return "loop"
    (ex, ey), (fx, fy) = line[0], line[-1]
    straight = math.hypot(fx - ex, fy - ey) / max(1, chain)
    if straight > 0.90:
        return "strand"
    turning, prev = 0.0, None
    for i in range(1, len(line)):
        dx, dy = line[i][0] - line[i - 1][0], line[i][1] - line[i - 1][1]
        if math.hypot(dx, dy) < 0.4:
            continue
        a = math.atan2(dy, dx)
        if prev is not None:
            turning += abs((a - prev + math.pi) % (2 * math.pi) - math.pi)
        prev = a
    return "helix" if turning >= 5.0 else "turn"


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
    args = ap.parse_args()
    rng = random.Random(args.seed)

    im = Image.open(SRC).convert("RGB")
    SW, SH = im.size
    grid, rows, cols, ox, oy = cell_grid(im)
    comps = components(grid, rows, cols)

    kinds = {}
    ok = []

    def consider(cs, allow_split=True):
        if len(cs) < MIN_CELLS:
            return False
        line, chain_cells = centreline(cs)
        if len(line) < 3:
            return False
        k = classify(cs, line, chain_cells)
        if k not in ("helix", "strand", "turn"):
            return False
        sw = stroke_cells(cs, line)
        if sw <= MAX_STROKE:
            ok.append((cs, line, chain_cells, k, sw))
            return True
        if allow_split:
            # Too fat to have a chain through it — try it as separate structures.
            return any(consider(p, False) for p in split4(cs))
        return False

    for cs in comps:
        line, chain_cells = centreline(cs)
        k = classify(cs, line, chain_cells) if len(line) >= 2 else "fragment"
        kinds[k] = kinds.get(k, 0) + len(cs)
        consider(cs)
    lit = sum(len(c) for c in comps)
    print(f"{len(comps)} components, {lit} lit cells")
    for k in ("helix", "strand", "turn", "loop", "fragment"):
        print(f"   {k:9s} {kinds.get(k, 0):5d} cells  {kinds.get(k, 0) / lit:5.1%}")
    # Assign periods shortest-chain first, so each structure gets the prime
    # nearest its own ideal and the light keeps the same speed on all of them.
    chosen = sorted(ok, key=lambda t: t[2])
    n = len(chosen)
    print(f"animating {n} structures = "
          f"{sum(len(t[0]) for t in chosen) / lit:.0%} of the lit area")

    os.makedirs(OUTDIR, exist_ok=True)
    for f in os.listdir(OUTDIR):
        os.remove(os.path.join(OUTDIR, f))

    used = set()
    parts = [HEAD.format(seed=args.seed, ncomp=len(comps), n=n, sw=SW, sh=SH)]
    total = 0
    for i, (cs, line, chain_cells, kind, sw_cells) in enumerate(chosen):
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
            sw=round(sw_cells * PITCH)))
        print(f"  {name:4s} {kind:7s} {len(cs):4d} cells  chain {chain_cells:3d}  "
              f"stroke {sw_cells:4.1f}c  period {period:3d}s  "
              f"draw {period * DRAW_FRACTION:4.1f}s")
    parts.append("\n</div>\n")
    open(PARTIAL, "w").write("".join(parts))
    print(f"wrote {PARTIAL} ({len(''.join(parts))} bytes) "
          f"+ {n} silhouettes ({total} bytes)")


if __name__ == "__main__":
    main()
