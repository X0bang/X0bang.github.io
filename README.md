# boyuezhang.com

Personal academic homepage of Boyue Zhang. Hugo, no third-party theme, no
JavaScript framework.

## Running it

Needs Hugo **extended** 0.164.0 or newer — the version pinned in the deploy
workflow.

```bash
hugo server -D        # http://localhost:1313/
hugo build --gc       # production build into ./public
```

## Where things live

| What | Where |
| --- | --- |
| Site config, social links, cover artwork | `hugo.toml` |
| Home page bio | `content/_index.md` |
| Projects | `content/projects/*.md` |
| CV page and PDF | `content/cv/_index.md`, `static/files/` |
| Timeline, honours | `data/timeline.yml`, `data/honors.yml` |
| Layouts, styles, behaviour | `layouts/`, `assets/css/main.css`, `assets/js/main.js` |
| Cover animation | `structure-analysis/` (see its README) |
| Custom domain | `static/CNAME` |

## Deployment

Every push to `main` runs `.github/workflows/hugo.yml`, which builds with the
pinned Hugo version and publishes to GitHub Pages. `baseURL` comes from
`hugo.toml`, so the custom domain always wins.

Repository settings → Pages → Build and deployment → Source must be
**GitHub Actions**.

## Third-party material

Institution and competition logos under `assets/images/logos/` are the
trademarks of their respective owners, reproduced unaltered to identify the
institutions attended and the awards received. No affiliation or endorsement is
implied. Inter and IBM Plex Mono are used under the SIL Open Font License.
