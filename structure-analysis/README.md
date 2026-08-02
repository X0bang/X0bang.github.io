# Structure analysis

Finds the secondary structures drawn in the cover artwork and turns them into
the homepage's background animation.

The cover is pixel art — 6px squares on a 7px pitch — so it can be read back as
the grid it was drawn on. Each structure is cut out as a 1-bit silhouette and
laid back over the cells it came from, and a light is animated along its
backbone. Nothing is moved and nothing is invented: the shapes are the artwork's
own, which is the only version of this that has ever looked right.

## Running it

From the repository root:

```sh
python3 structure-analysis/gen_traces.py --seed 3   # silhouettes + the partial
python3 structure-analysis/render_map.py            # the maps, for checking
```

`gen_traces.py` writes `assets/images/bg/traces/s*.png` and
`layouts/_partials/fx/chain.html`. Both are committed, so the site builds
without Python; re-run only when the artwork or the detection changes.

`render_map.py` writes into `out/`:

| file | what it is |
| --- | --- |
| `numbered.png` | every element numbered and coloured by class, with every cell the animation never touches in red. The banner is cut in half and stacked so the labels are legible. |
| `classes.png` | the same colouring, unlabelled, at full width. |
| `elements.json` | one record per element — class, cell count, chain length, stroke width. |

The numbers in `numbered.png` match the `s0..sN` silhouettes, because both sort
by chain length.

## How detection works

`detect.py`, in order:

1. **Recover the grid.** The 7px pitch is known; the phase is found by taking
   whichever offset makes the cell centres brightest.
2. **Threshold at 24.** The cell-luminance histogram has a background mode at
   8–18 and a flat tail of structure cells from 24 up, with the valley at
   22–26. An earlier value of 42 sat in the middle of that tail and cut real
   structure away — chiefly the dimmer cells where one element runs into the
   next, which split single helices into three or four pieces.
3. **Separate by width, not by connectivity.** At a threshold low enough to
   keep every real cell, a whole protein is one connected component: the loops
   joining its helices and sheets are real pixels too. Chemically correct,
   useless here — one light would crawl over an entire domain. Loops run 1–2
   cells wide and helices and sheets 4–8, so a distance transform marks the
   cells at least 2 deep, those cores fall apart at the thin connectors into
   one piece per element, and every lit cell is then handed back to its nearest
   core by a simultaneous flood. Connectors that are thin end to end never
   reach a core, so anything long enough becomes a loop element of its own.
4. **Trace a centreline.** BFS finds the far end of the element, cells are
   binned by hop count from it, and the per-bin centroids are smoothed. That
   tracks the chain even where the ribbon is several cells wide.
5. **Classify.** Straightness (end-to-end over chain length) separates
   β-strands, which run ≥ 0.90, from anything that coils back. Total absolute
   turning then separates a winding coil from a single bend, one turn of a coil
   being 2π. Counting axis reversals instead — the obvious approach — misses a
   helix standing vertically, because it never reverses in x.

## How the animation is sized

- **Stroke** comes from each element's 95th-percentile cell distance, not its
  furthest. One outlying cell in a corner would otherwise demand a stroke half
  the chain's length, and a stroke that wide uncovers the whole shape at once —
  there is no travelling light left.
- **Acceptance** is either a small absolute stroke, or a stroke small against
  the chain. Requiring both rejects most of the picture: short stubby elements
  fail the ratio, long ones fail the absolute.
- **Period** is proportional to chain length against the same draw fraction the
  CSS uses, which holds the light at ~7.5 cells/s everywhere. `DRAW_FRACTION`
  here and the `8%` in the `cm-run` keyframes are the same number and must move
  together.
- **Periods repeat.** Forcing distinct values pushed the long chains past 170s —
  three minutes between showings — and broke the constant speed. Two elements
  sharing a period is invisible: their phases differ.

The CSS lives in `assets/css/main.css` under *Cover effect: in-situ chain
traces*, including the registration trick that keeps the silhouettes on their
cells at any viewport width.
