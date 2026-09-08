# CV ↔ Website unification plan

Branch: `cv-website-sync`

## Problem

Two disconnected hand-maintained sources:

- `drprojects.github.io` — Jekyll collections, partly structured (`_publications`),
  mostly unstructured one-line markdown blobs (`_talks`, `_teaching`, `_news`).
- `~/projects/public/academic_resume` — 7 pages of hand-typed LaTeX, no data layer,
  not even under version control.

They already drifted: the published PDF lists FORMSpoT as `arXiv`, the `.tex` says
`Remote Sensing of Environment`.

## Target architecture

One repo. One dataset. Two renderers.

```
_data/*.yml   ← the ONLY thing edited by hand
   │
   ├─► Jekyll ──► website (incl. a new /cv/ web page)
   └─► cv/build.py ──► Jinja2 ──► .tex ──► pdflatex ──► files/cv.pdf
```

Every item carries flags controlling where it appears:
`cv: true|false` and `web: true|false`. The CV and the site are therefore
*consistent* without being *identical* — which is the point.

## Data files

| File | Source today | Consumers |
|---|---|---|
| `profile.yml` | `_config.yml` author, `about.md`, CV heading | web + cv |
| `authors.yml` | already exists, kept | web + cv |
| `publications.yml` | `_publications/*.md` ∪ CV `3__publications.tex` | web + cv |
| `talks.yml` | `_talks/*.md` ∪ CV `4_talks.tex` | web + cv |
| `teaching.yml` | `_teaching/*.md` ∪ CV `3__teaching.tex` | web + cv |
| `news.yml` | `_news/*.md` | web only |
| `code.yml` | `_code/*.md` ∪ CV `3__repos.tex` | web + cv |
| `positions.yml` | CV `1_positions.tex` | cv (+ new web section) |
| `education.yml` | CV `2_education.tex` | cv |
| `awards.yml` | CV `3__awards.tex` | web + cv |
| `service.yml` | CV `3__reviewing.tex` | cv |
| `supervision.yml` | CV `3__supervision.tex` | cv |
| `skills.yml` | CV `5_skills.tex` | cv |

## Deleted

`markdown_generator/` (dead TSV→md layer), `_pages/cv.md` and `_pages/cv-json.md`
(untouched academicpages boilerplate: "Ph.D in Version Control Theory, GitHub
University" — currently live and publicly reachable), `_talks/`, `_teaching/`,
`_news/`, `_code/`, `_publications/`.

## CV redesign — 4 pages (was 7)

```
p1  Header · Summary · Positions · Education (MSc and above)
p2  Publications · Preprints & under review · Awards
p3  Supervision · Reviewing & chairing · Teaching · Open-source
p4  Selected talks (~15) · Skills strip
```

Content cut (all of it stays on the website):
- Education: high school (2006-09, 2009-11), Coursera, Udacity
- Talks: ~30 repeat internal seminars of the same title

Design changes:
- drop the raster icons8 clip-art; typographic hierarchy + one accent colour
- every publication becomes clickable (arXiv / project / code) — the URLs are
  already in the data and were simply unused by the CV
- GitHub stars fetched at build time instead of hardcoded and stale
- "Under review" / "WBF" split into their own block instead of being interleaved
  into the year-sorted published list
- citation metrics in the header (`profile.yml: metrics`)

## Build

- `make serve` — local site preview at :4000, never touches the live site
- `make cv`    — regenerate `files/cv.pdf`
- `make check` — fail if the PDF is older than `_data/`
- CI: on push to `_data/` or `cv/`, rebuild the PDF and commit it.
  GitHub Pages keeps doing the site build (no Action for that today).

## Phases

1. Schema + `_data` extraction  ← data correctness, verify against sources
2. Jekyll templates read `_data`; old collections deleted
3. New `/cv/` web page
4. LaTeX template + `cv/build.py`
5. Makefile, GitHub Action, staleness guard

---

## Status — implemented

All five phases are done on branch `cv-website-sync`.

**Data.** 12 YAML files in `_data/`. Publications went from 12 to 16 (the CV had
four entries the site did not). Talks are structured (type, venue, venue_url,
title, title_url, location) rather than prose blobs, and the website sentence is
generated from those fields.

**Website.** All listing pages and includes read `site.data.*`. Collections,
`markdown_generator/`, `scripts/`, the JSON-CV layer and the academicpages
boilerplate CV pages are deleted. New `/cv/` page. New `_config_dev.yml` so a
local build stops loading the live site's CSS.

**CV.** 7 pages -> 4. New `cv/drcv.sty` (Source Serif Pro + Source Sans Pro,
one accent colour, gutter grid, no raster icons). Publications are clickable.
GitHub stars fetched at build time.

**Build.** `make serve | cv | check`, plus a GitHub Action that rebuilds and
commits the PDF whenever `_data/` or `cv/` changes.

### Open items for Damien

1. `_data/talks.yml` — the NVIDIA entry has `_verify: location inferred`.
   Confirm the location and delete that key.
2. `_data/profile.yml` — `metrics.show` is `false`; fill in citations/h-index
   to print them in the CV header.
3. The old `/files/academic_resume_damien_robert.pdf` URL is gone; the CV is now
   at `/files/cv.pdf`.
4. Leftover academicpages demo pages still build and are publicly reachable:
   `_pages/markdown.md`, `non-menu-page.md`, `terms.md`,
   `archive-layout-with-content.md`, `portfolio.html`, `page-archive.html`,
   `collection-archive.html`, `year-archive.html`, `category-archive.html`,
   `tag-archive.html`. Worth deleting in a follow-up.
