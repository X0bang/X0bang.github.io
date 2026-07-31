# bang.x0bang.com

Personal academic homepage of Boyue Zhang — built with [Hugo](https://gohugo.io/),
deployed to GitHub Pages by the workflow in `.github/workflows/hugo.yml`.

The theme is not a third-party one: the layouts in `layouts/` and the styles in
`assets/` are this site's own monochrome, editorial design.

## Running it locally

Hugo **extended** v0.164.0 or newer (the version pinned in the deploy workflow):

```bash
hugo server -D        # http://localhost:1313/
hugo build --gc       # one-off production build into ./public
```

macOS without Homebrew: grab `hugo_extended_<version>_darwin-universal.pkg` from
the [releases page](https://github.com/gohugoio/hugo/releases) and install it, or
extract the binary from the package without installing:

```bash
xar -xf hugo_extended_0.164.0_darwin-universal.pkg -C /tmp/hugo-pkg
cd /tmp/hugo-pkg && cat Payload | gzip -dc | cpio -idmu
install -m 0755 hugo ~/bin/hugo
```

## Where things live

| What | Where |
| --- | --- |
| Site config, social links, epigraph | `hugo.toml` |
| Home page bio ("About") | `content/_index.md` — `bioShort` in front matter is the always-visible paragraph, the body is the expanded text |
| Timeline entries | `data/timeline.yml` |
| Invited talks | `data/talks.yml` |
| Honors and awards | `data/honors.yml` |
| News entries | `data/news.yml` |
| Projects | `content/projects/*.md` |
| CV page | `content/cv/_index.md` (PDF in `static/files/`) |
| Contact page | `content/contact/_index.md` |
| Styles | `assets/css/main.css` |
| Behaviour (theme toggle, switches) | `assets/js/main.js` |
| Custom domain | `static/CNAME` |

## Adding content

**A project** — create `content/projects/<slug>.md`:

```yaml
---
title: "Project title"
date: 2026-07-31
year: "2026"        # drives the "By Year" grouping and the year pill
weight: 1           # lower = higher in the list
selected: true      # include in the default "Selected" view
tags: ["protein engineering"]   # drives the "By Topic" grouping
summary: "One line shown on the card."
thumb: "images/projects/foo.png"   # optional; a placeholder tile shows without it
venue: "iGEM 2025"  # optional pill
status: "Ongoing"   # optional highlighted pill
authors: "With A. Person, B. Person"   # optional collaborators line
links:              # optional chips: Paper / Code / Wiki / Webpage / …
  - name: "Code"
    url: "https://github.com/…"
draft: false
---
```

Keep `summary` to one compressed, verb-first sentence — it is the line that does
the work on the card.

The Projects section has three views — **Selected**, **By Year**, **By Topic**.
"Selected" lists the projects marked `selected: true`, and falls back to showing
every project while none are marked.

**A news item** — prepend to `data/news.yml`. The first five show; the rest sit
behind "Show all".

**A timeline entry** — add to `data/timeline.yml`, newest first. `brief: true`
keeps it visible while the timeline is collapsed; everything else appears when
the "More about me" button expands the About/Timeline block.

**A talk or an honor** — add to `data/talks.yml` or `data/honors.yml`, newest
first; each file documents its own fields at the top. Honors use the same
`brief: true` convention: marked entries are the "selected" ones on show, the
rest sit behind "Show all".

**The epigraph** — `[params.epigraph]` in `hugo.toml`. It is hidden until the
portrait is hovered (or tapped / focused), which fades the cover card into its
dark state.

**The cover artwork** — `[params.cover]` in `hugo.toml`, with paths relative to
`assets/`. `image` is always behind the profile card; `imageDeep` is the optional
"painted twin" that fades in with the epigraph. Both are converted to WebP at
build time, so commit the full-quality source and let Hugo do the compressing —
the originals are never published. Leave `image` empty to fall back to the plain
gradient cover.

**Any aspect ratio works.** The cover reads the artwork's real dimensions and
takes that shape (`--cover-ratio`, set inline), so the composition is shown whole
rather than cropped into a fixed band. Both images should share a ratio, since
they crossfade in the same box. Compose so the **lower third stays quiet** — the
profile card sits there, and on wide screens the top two thirds are what shows.
Around 1800–2900 px wide is plenty; below ~1400 px it softens on retina screens.

## Sections that are currently hidden

Three sections are written and working but not rendered, because there is nothing
to put in them yet: **News**, **Junior Collaborators & Interns**, and
**Academic Service**.

To bring one back:

1. create the data file named in the partial's header comment —
   `data/news.yml`, `data/collaborators.yml`, or `data/service.yml`;
2. uncomment the matching `partial` line in `layouts/home.html`.

Section numbers (`01`, `02`, …) come from a CSS counter, so they renumber
themselves. Each partial also renders nothing when its data file is absent, so
step 2 alone is harmless.

## Deployment

Every push to `main` triggers `.github/workflows/hugo.yml`, which builds with the
pinned Hugo version and publishes to GitHub Pages. `baseURL` is set in `hugo.toml`
and deliberately *not* overridden in the workflow, so the custom domain always
wins.

In the repository settings, **Settings → Pages → Build and deployment → Source**
must be set to **GitHub Actions**.
