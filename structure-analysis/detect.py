"""Find the secondary structures in the cover artwork.

The cover is pixel art — 6px squares on a 7px pitch — so it can be read back as
the grid it was drawn on. This module recovers that grid, separates it into
secondary-structure elements, classifies them, and traces a centreline along
each one. `gen_traces.py` turns the result into the site's animation;
`render_map.py` draws the maps used to check it by eye.

Two decisions carry most of the weight:

* **Threshold.** The cell-luminance histogram has a background mode at 8-18 and
  a flat tail of structure cells from 24 up, with the valley at 22-26. An
  earlier value of 42 sat in the middle of that tail and cut real structure
  away — chiefly the dimmer cells where one element runs into the next, which
  split single helices into three or four pieces.

* **Separation by width, not connectivity.** At a threshold low enough to keep
  every real cell, a whole protein is one connected component: the loops that
  join its helices and sheets are real pixels too. Chemically correct, useless
  here — one light would crawl over an entire domain. Loops run 1-2 cells wide
  and helices and sheets 4-8, so a distance transform separates them cleanly.
"""

import math
import os
from collections import deque

from PIL import Image, ImageDraw

SRC = "assets/images/bg/background-cover.png"
OUTDIR = "assets/images/bg/traces"
PARTIAL = "layouts/_partials/fx/chain.html"

PITCH = 7        # the artwork's cell pitch, in source px
SQUARE = 6       # lit part of a cell; the remainder is the grid gap
# The cell-luminance histogram has a background mode at 8-18 and a flat tail of
# structure cells from 24 up, with the valley at 22-26. The old value of 42 sat
# in the middle of that tail and cut real structure away — chiefly the dimmer
# cells where one secondary structure runs into the next, which split single
# helices into three or four pieces.
# Raising this also straightens out ordering: the gaps the artwork draws between
# a coil's turns have to stay dark, or the shape becomes solid and the path
# short-circuits across it.
LIT = 32         # luminance above which a cell belongs to a structure
LIFT = 1.45      # how far a lit cell is raised above its own colour
CORE_D = 2       # a cell this far inside the ribbon is "wide", i.e. not a loop
MIN_CORE = 6     # cells; smaller cores are noise, not a structure element
MIN_CELLS = 20        # below this a component is noise, not structure
# Two ways to be acceptable, because they catch different shapes. A stroke
# small in absolute terms is fine however stubby the element — it simply reads
# as lighting up as a unit, which for a two-turn fragment is right. A stroke
# large in absolute terms is still fine if it is small against the chain, since
# that is what decides whether the light travels: 27 cells over a 67-cell chain
# travels, the same 27 over a 20-cell chain floods. Requiring both at once
# rejects most of the picture; the hard cap is only a backstop.
NARROW_STROKE = 16.0     # small enough on its own
MAX_STROKE_RATIO = 0.45  # or small enough against the chain
MAX_STROKE = 30.0
MIN_LOOP = 12    # cells; a connector shorter than this is not worth animating
CELLS_PER_SEC = 7.5   # chain speed, held constant across every structure
DRAW_FRACTION = 0.08  # share of the period spent drawing
# With 19 traces each lit for ~11% of its period, about two are alight at once.
PRIMES = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
          149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
          223, 227, 229, 233, 239, 241, 251]


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


def elements(grid, rows, cols):
    """Secondary-structure elements, not connected components.

    At a threshold low enough to keep every real cell, a whole protein is one
    connected component: the loops that join its helices and sheets are real
    pixels too. Chemically correct, useless here — one light would crawl over an
    entire domain.

    So the split is by ribbon width instead, which is what actually separates
    them: loops run 1-2 cells wide, helices and sheets 4-8. A distance transform
    marks every cell at least CORE_D inside the shape; those cores fall apart at
    the thin connectors into one piece per element. Every lit cell is then
    handed back to its nearest core by a simultaneous flood, so each element
    recovers its full width and the connectors are shared out between the
    elements they join.
    """
    lit = {(r, c) for r in range(rows) for c in range(cols) if grid[r][c] > LIT}

    # Chessboard distance from each lit cell to the nearest unlit one.
    dist, q = {}, deque()
    for (r, c) in lit:
        if any((r + dr, c + dc) not in lit
               for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
            dist[(r, c)] = 1
            q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                n = (r + dr, c + dc)
                if n in lit and n not in dist:
                    dist[n] = dist[(r, c)] + 1
                    q.append(n)

    core = {p for p, d in dist.items() if d >= CORE_D}
    seen, cores = set(), []
    for start in core:
        if start in seen:
            continue
        seen.add(start)
        q, cur = deque([start]), []
        while q:
            r, c = q.popleft()
            cur.append((r, c))
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    n = (r + dr, c + dc)
                    if n in core and n not in seen:
                        seen.add(n)
                        q.append(n)
        if len(cur) >= MIN_CORE:
            cores.append(cur)

    # Grow every core at once; the first to reach a cell claims it.
    owner, q = {}, deque()
    for i, cur in enumerate(cores):
        for p in cur:
            owner[p] = i
            q.append(p)
    while q:
        r, c = q.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                n = (r + dr, c + dc)
                if n in lit and n not in owner:
                    owner[n] = owner[(r, c)]
                    q.append(n)

    out = [[] for _ in cores]
    for p, i in owner.items():
        out[i].append(p)

    # Connectors that are thin end to end never touch a core, so the flood never
    # reaches them. They are still real chain — the loops between structures —
    # so anything long enough becomes an element in its own right.
    rest, seen2 = lit - set(owner), set()
    for start in rest:
        if start in seen2:
            continue
        seen2.add(start)
        q, cur = deque([start]), []
        while q:
            r, c = q.popleft()
            cur.append((r, c))
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    n = (r + dr, c + dc)
                    if n in rest and n not in seen2:
                        seen2.add(n)
                        q.append(n)
        if len(cur) >= MIN_LOOP:
            out.append(cur)
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


def thin(cs):
    """Zhang-Suen thinning: reduce the element to a one-cell-wide skeleton.

    Ordering has to follow the ribbon, and on the filled shape it does not. In a
    coil, two turns that are far apart along the chain sit next to each other on
    the page, so a breadth-first walk hops the gap between them and the path
    cuts straight across the spiral instead of winding along it. Thinning first
    removes the width that makes those shortcuts possible.
    """
    img = set(cs)

    def nbrs(r, c):
        return [(r - 1, c), (r - 1, c + 1), (r, c + 1), (r + 1, c + 1),
                (r + 1, c), (r + 1, c - 1), (r, c - 1), (r - 1, c - 1)]

    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            drop = []
            for (r, c) in img:
                p = [1 if n in img else 0 for n in nbrs(r, c)]
                b = sum(p)
                if not 2 <= b <= 6:
                    continue
                a = sum(1 for i in range(8)
                        if p[i] == 0 and p[(i + 1) % 8] == 1)
                if a != 1:
                    continue
                if step == 0:
                    if p[0] * p[2] * p[4] or p[2] * p[4] * p[6]:
                        continue
                else:
                    if p[0] * p[2] * p[6] or p[0] * p[4] * p[6]:
                        continue
                drop.append((r, c))
            if drop:
                img.difference_update(drop)
                changed = True
    return img or set(cs)


def centreline(cs):
    """Polyline end to end along the chain, plus its length in cells."""
    skel = thin(cs)
    d0 = bfs(skel, next(iter(skel)))
    far = max(d0, key=d0.get)
    d = bfs(skel, far)
    end = max(d, key=d.get)
    # Walk back from the far end along decreasing hop count: on a skeleton that
    # is the ribbon's own path, so the order is the chain's order.
    path, cur = [end], end
    while d[cur] > 0:
        cur = min((n for n in ((cur[0] + dr, cur[1] + dc)
                               for dr in (-1, 0, 1) for dc in (-1, 0, 1))
                   if n in d and d[n] == d[cur] - 1), key=lambda n: n)
        path.append(cur)
    path.reverse()
    pts = [(c, r) for r, c in path]
    # A 3-tap mean settles the staircase of a one-cell-wide skeleton.
    sm = []
    for i in range(len(pts)):
        w = pts[max(0, i - 1):i + 2]
        sm.append((sum(q[0] for q in w) / len(w), sum(q[1] for q in w) / len(w)))
    return sm, len(path) - 1


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


def silhouette(cs, src, ox, oy, path, lift=LIFT):
    """Cut the structure out of `src`, keeping each cell's own colour.

    A flat ink would paint every cell the same, flattening the artwork's
    blue-to-green gradients into one stripe. Sampling the source instead means a
    lit cell brightens from whatever colour it already is — the page composites
    these with `screen`, so the result is that cell's own hue, raised. `lift`
    only sets how far.
    """
    rs = [r for r, _ in cs]
    ct = [c for _, c in cs]
    r0, c0 = min(rs), min(ct)
    w, h = max(ct) - c0 + 1, max(rs) - r0 + 1
    im = Image.new("RGBA", (w * PITCH, h * PITCH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for r, c in cs:
        box = (ox + c * PITCH + 1, oy + r * PITCH + 1,
               ox + c * PITCH + PITCH - 1, oy + r * PITCH + PITCH - 1)
        px = list(src.crop(box).getdata())
        col = tuple(min(255, int(sum(q[i] for q in px) / len(px) * lift))
                    for i in range(3))
        x, y = (c - c0) * PITCH, (r - r0) * PITCH
        d.rectangle([x, y, x + SQUARE - 1, y + SQUARE - 1], fill=col + (255,))
    im.save(path, optimize=True)
    return w, h, r0, c0


