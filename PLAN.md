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


---

## Round 2 — design pass

Following review feedback:

**Landing page.** Distinctions strip (from `awards.yml`, ordered by `weight` so
the Best Paper Finalist leads) and a stats band computed from the data
(publications, talks, GitHub stars, countries presented in). The bare "All news
→" arrow became a proper underlined link.

**Talks.** Five hand-drawn 24×24 line icons for oral / poster / invited /
interview / tutorial, in `_includes/icon-type.html`. They inherit
`currentColor`, so they work in both themes. A legend sits at the top of the
page. Location moved to its own de-emphasised second line.

**Teaching.** Format and audience on a second line; teaching hours are kept in
the data but printed only in the PDF.

**CV.** No more HTML CV — the nav serves the PDF. One shared intro paragraph.
Full-bleed tinted header band, accent marker blocks on section headings, a
publications-per-year bar chart beside the Publications heading, and language
proficiency meters. Separator style unified to a single middot. Submission
counts removed from the Best Paper Finalist line.

**New `/community/` page.** Reviewing & chairing, organising committees,
supervision, collaborators, scientific advising, grants. `organizing.yml` and
`grants.yml` are empty with documented schemas and their sections stay hidden
until filled.

### Still open

1. `_data/talks.yml` — NVIDIA entry carries `_verify: location inferred`.
2. `_data/organizing.yml` and `_data/grants.yml` are waiting for real entries.
3. `_data/profile.yml` — `metrics.show` is `false`; add citations / h-index.
4. Leftover academicpages demo pages still build: `_pages/markdown.md` (which
   links to the now-deleted `/cv-json/`), `non-menu-page.md`, `terms.md`,
   `archive-layout-with-content.md`, `portfolio.html`, `page-archive.html`,
   `collection-archive.html`, `year-archive.html`, `category-archive.html`,
   `tag-archive.html`.


---

## Round 3 — review feedback

**Landing page.** Distinctions strip and stats band removed; back to intro plus
the eight most recent news items. The link reads "Browse all news items".

**Talk icons.** Redrawn as solid silhouettes (microphone, poster panel, speech
bubble, graduation cap, quote marks) — the thin outlines were fiddly at 1em.
Renamed `_includes/icon-type.html` since the Community page now shares it for
reviewer / area chair / organising committee.

**Dark mode.** Secondary text (talk locations, course formats, org names) used
`--global-text-color-light`, which is a 50%-darkened primary: fine on the light
background, close to unreadable on the dark one. Introduced `--dr-muted`, which
keeps the light value and switches to a brighter teal-grey under
`html[data-theme="dark"]`.

**Community.** New Awards & Recognitions section at the top, laid out like News,
each entry linking to public proof (the same URLs used in `news.yml`). Reviewing,
chairing and organising merged into one chronological list, one row per
commitment, with role icons and a legend. Outstanding-reviewer nominations moved
out of `service.yml` into `awards.yml` — they are recognitions, not duties.
Added the 2027 EarthVision organising committee.

**Data.** "Loïc Landrieu" normalised to "Loic Landrieu" throughout `_data/`.

**CV.** Open-source rows show stars and forks together, flush right, with a
`\faCodeBranch` fork icon. Skills section reworked: tools now render as a
four-column grid of logo + name (logos in `cv/assets/logos/`, referenced by a
`logo:` field in `skills.yml`), languages sit two per row with meters. Fixed the
overflow: `\chips` set the hyphenation penalties inside a group, so they were
restored before `\par` read them — hence "scikit-learn" still breaking. The new
`\nohyphens` is applied at the start of the entry body instead.

### Still open

1. `_data/talks.yml` — NVIDIA entry carries `_verify: location inferred`.
2. `_data/grants.yml` is empty; its section stays hidden until filled.
3. `_data/profile.yml` — `metrics.show` is `false`; add citations / h-index.
4. SLURM and LaTeX have no logo asset and render as text in the CV tools grid.
5. The academicpages demo pages listed above are still reachable.


---

## Round 4 — review feedback

- Landing page: distinctions strip and stats band removed, intro plus news only.
- Community: intro paragraph dropped; awards read "from AFRIF"; groups reordered
  to Collaborators, PhD, Master & interns, Advising.
- Area Chair icon changed from a gavel to a clipboard with a check.
- Page rhythm homogenised: every listing page uses `layout: archive`, the ad-hoc
  `<br/>` spacers are gone, and the gap under the title is owned by
  `.archive .page__title { margin-bottom: 1.4em }` with the first content element
  zeroed, so all six pages start content at the same height.

### The Loic Landrieu bug, and the fix

`supervision.yml` carried a `key:` into `authors.yml`, generated by a name
matcher that ran *before* "Loïc" was normalised to "Loic". The match silently
failed for that one person and his homepage link vanished.

The duplication is gone: people are now written as plain names and resolved
against `authors.yml` at build time by `_includes/author-link.html`. Adding
someone to `authors.yml` links them everywhere at once. Because name matching
can still miss (it did for "Jan D. Wegner" vs "Jan Dirk Wegner"), `cv/build.py`
now prints every supervision name it cannot resolve, so the failure is visible
rather than silent.

### Publications are not scraped

`publications.yml` was assembled from the existing `_publications/*.md` files and
the CV LaTeX source. Nothing is fetched from Google Scholar; the only network
call in the build is the GitHub API for star and fork counts.
