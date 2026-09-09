# drprojects.github.io

Personal website of Damien Robert, and the generator for the PDF CV that goes
with it. Forked from [academicpages](https://github.com/academicpages/academicpages.github.io)
and substantially reworked: the Jekyll collections, the TSV generators and the
demo content are gone, and both outputs are now rendered from one dataset.

---

## The idea

`_data/*.yml` is the **single source of truth**. The website and the PDF CV are
two renderings of it, so they cannot drift apart. Nothing is scraped from any
external service; every fact on the site is a line in one of these files.

```
                    WHAT YOU EDIT                      WHERE IT SHOWS UP
                    ─────────────                      ─────────────────

              ┌── profile.yml ──────────────┐─────▶  home intro + CV header
              │     name, links, intro,     │
              │     interests, cv_options   │
              │                             │
              ├── news.yml ─────────────────┤─────▶  home + /news/
              ├── publications.yml ─────────┤─────▶  /publications/ + CV
              ├── talks.yml ────────────────┤─────▶  /talks/  + CV if cv: true
              ├── teaching.yml ─────────────┤─────▶  /teaching/ + CV
              ├── code.yml ─────────────────┤─────▶  /code/ + CV
              │                             │
   _data/ ────┤   ── the Community page ──  │
              ├── awards.yml ───────────────┤─────▶  /community/ + CV
              ├── service.yml ──────────────┤─────▶  /community/ + CV
              ├── organizing.yml ───────────┤─────▶  /community/ + CV
              ├── supervision.yml ──────────┤─────▶  /community/ + CV
              ├── leadership.yml ───────────┤─────▶  /community/ + CV   (empty)
              ├── grants.yml ───────────────┤─────▶  /community/ + CV   (empty)
              │                             │
              ├── positions.yml ────────────┤─────▶  CV + sidebar employer
              ├── education.yml ────────────┤─────▶  CV only
              ├── skills.yml ───────────────┤─────▶  CV only
              │                             │
              │   ── registries, pointed at by everything above ──
              ├── authors.yml ──────────────┤─────▶  people: name, homepage, org
              └── organizations.yml ────────┘─────▶  institutions, labs,
                                                      companies, venues

              cv/stars.json ── generated, never edited by hand


   RENDERERS
   ─────────
   Jekyll        _pages/*.html + _includes/archive-single-*.html  →  website
   cv/build.py   cv/templates/cv.tex.j2 + cv/drcv.sty → pdflatex  →  files/cv.pdf
```

There are **no Jekyll collections**. The site builds exactly eight pages: the
seven real ones plus `404`.

---

## Adding content

| To add a… | Edit | Appears on |
|---|---|---|
| paper | `publications.yml` | /publications/ + CV |
| talk | `talks.yml` | /talks/, and the CV **only** with `cv: true` |
| course | `teaching.yml` | /teaching/ + CV |
| repository | `code.yml` | /code/ + CV |
| news item | `news.yml` | homepage (latest 8) + /news/ |
| award or recognition | `awards.yml` | /community/ + CV |
| review or chair role | `service.yml` | /community/ + CV |
| organising committee | `organizing.yml` | /community/ + CV |
| student, collaborator, advisee | `supervision.yml` | /community/ + CV |
| project lead, recruitment | `leadership.yml` | /community/ + CV |
| grant | `grants.yml` | /community/ + CV |
| job | `positions.yml` | CV + the sidebar's employer line |
| degree, skill, language | `education.yml`, `skills.yml` | CV |
| a person | `authors.yml` | wherever they are referenced |
| an institution or company | `organizations.yml` | likewise |

`leadership.yml` and `grants.yml` ship **empty, with their schema in comments**.
Both the website and the CV hide those sections entirely until the file has at
least one entry, so adding the first item is the only step needed.

### Choosing where an item appears

Every entry accepts two optional flags:

- `cv: false` — keep it on the website, leave it out of the PDF. Used for the
  MOOCs and high-school entries in `education.yml`.
- `web: false` — the reverse.

**Talks invert this.** There are 45 of them and the CV prints a selected 17, so
a talk needs an explicit `cv: true` to be printed. Everything else defaults to
appearing in both.

---

## Two registries, referenced by key

`authors.yml` holds **people**; `organizations.yml` holds **institutions, labs,
companies and venues**. Nothing else stores their details:

```
supervision.yml            authors.yml                organizations.yml
  - person: ──────────▶   loic_landrieu:              enpc:
      loic_landrieu         first_name: Loic            name: École des Ponts…
      with: [...]           last_name: Landrieu         short: ENPC
                            url: https://…              url: …
positions.yml               org: enpc ──────────────▶
  - person: ──────────▶
      loic_landrieu       organizations.yml is also pointed at directly by
                          positions.yml, education.yml, teaching.yml,
publications.yml          leadership.yml and grants.yml
  authors: [loic_landrieu, …] ─▶
```

Rename someone in `authors.yml` and every page follows. `supervision.yml`'s
advising group accepts `organization:` as well as `person:`, since advising can
be for an individual or for a company, and a `with:` list resolves against
either registry.

**Everything is validated.** `cv/build.py` refuses to write anything if a key
does not resolve — a person, an organisation or a publication id — and names the
file and the offending key. It also rejects an empty list entry, which is what a
stray `-` in a YAML file becomes.

This matters. An earlier version matched people by full name instead of by key,
and normalising "Loïc" to "Loic" silently removed his homepage link from the
site with no error anywhere.

### Cross-references between content files

- a **talk** can carry `publication: <id>` instead of repeating the paper's
  project URL — that URL appeared nine times for DeepViewAgg alone. An explicit
  `title_url:` still wins when a talk links somewhere else.
- a **repo** can carry `publication: <id>`, which adds a "Paper page" button on
  /code/. It keeps its own `code_url` and teaser, because a codebase can serve
  several papers (`superpoint_transformer` serves three) and can outlive any of
  them.

### Identity lives in one file

Name, bio, location and every profile link come from `profile.yml`. The sidebar
(`_includes/author-profile.html`) and the CV both read it; `_config.yml`'s
`author:` block no longer holds a second copy. The **current role and employer
are derived** from the open-ended entry in `positions.yml` rather than restated,
so a job change is one edit.

---

## Working locally

```bash
make install     # Ruby + Python dependencies
make serve       # preview at http://localhost:4000, live reload
make cv          # regenerate files/cv.pdf (fetches live GitHub star counts)
make cv-offline  # same, without touching the network
make check       # fail if files/cv.pdf is older than the data behind it
make build-prod  # build the site exactly as GitHub Pages will
make clean
```

`make serve` layers `_config_dev.yml` over `_config.yml` to override `url`.
**Without that override a local build silently loads the live site's CSS**, and
you end up reviewing production styling instead of your own changes.

Note that `make build-prod` writes to `_site/`, which is what `make serve` is
serving — run it while the preview is up and the preview starts showing
production URLs until the next rebuild.

---

## Deployment

**Editing content is `git commit` + `git push`. There is nothing else to run.**

Two mechanisms, only one of which is a workflow:

- the **website** is built by GitHub Pages itself. There is no Action for it.
  `bundle` resolves Jekyll to the same version Pages uses (3.10 via the
  `github-pages` gem), so a local build is faithful.
- the **PDF** cannot be built by Pages, which has no LaTeX. So
  `.github/workflows/build-cv.yml` runs on any push touching `_data/**` or
  `cv/**`, rebuilds `files/cv.pdf` and commits it back.

Because that workflow pushes a commit of its own, **`git pull --rebase` before
your next edit**. If the rebase stops on a conflict in `files/cv.pdf`, take
either side — both were generated from the same data — and continue:

```bash
git checkout --ours files/cv.pdf && git add files/cv.pdf && git rebase --continue
```

The workflow needs *Settings → Actions → General → Workflow permissions* set to
**Read and write**, or its push fails with a 403. It pins `ubuntu-24.04` and
checks every required LaTeX package up front, so a missing one fails with a
named list rather than an obscure `Undefined control sequence`.

---

## The CV

There is no HTML CV page. The **CV** nav item serves `files/cv.pdf` directly, so
there is only one CV to design and maintain, and the intro paragraph in
`profile.yml` is shared between the homepage and the PDF.

- `cv/drcv.sty` — all typography and layout. Every tunable value lives in the
  `DESIGN TOKENS` block at the top: accent colour, gutter width, spacing.
- `cv/templates/cv.tex.j2` — content structure only. Jinja delimiters are
  remapped to `((* … *))` and `((( … )))` so they do not collide with LaTeX.
- `cv/build.py` — loads and validates the data, fetches star counts, renders,
  runs pdflatex twice, writes `files/cv.pdf`.

The graphical elements — the tinted header band, the highlight chips, the
keyword chips, the role icons — are TikZ, driven by the same data. Emoji are
rendered by `twemojis`, which works under pdflatex; `build.py` derives each
glyph's codepoint from the emoji already in `profile.yml`.

The header band's height is **derived, not fixed**: the header marks its end with
a TikZ coordinate and the band fills down to it. An earlier hand-tuned constant
drifted out of place every time the header content changed.

### Switches

`profile.yml` carries a `cv_options` block. The data and both renderers keep the
plumbing either way; these only decide what is printed:

```yaml
cv_options:
  show_teaching_hours: false     # per-course hours in the CV
  show_publication_links: false  # Paper / Project / Code links — a printed CV
                                 # cannot be clicked, and they are on the site
```

### Star counts

Stars and forks are fetched at build time into `cv/stars.json`, never hardcoded.
That file exists **only for the PDF**: a PDF is static and cannot call the GitHub
API when a reader opens it, so the numbers must be baked in. The `/code/` page
ignores it entirely and uses live shields.io badges. You never edit it; CI
refreshes it on every push.

### Citation metrics

`profile.yml` has a `metrics` block that prints beside the Publications heading.
Google Scholar has no API and cannot be scraped legitimately, so these are typed
in by hand and carry their own source and date:

```yaml
metrics:
  show: true
  citations: 487
  h_index: 7
  source: Google Scholar
  updated: 2026-09-09
```

Refresh them a couple of times a year, or set `show: false` to hide the line.

---

## Upstream template

Documentation for the original template is at <https://academicpages.github.io/>.
Most of it no longer applies here: the collections, the TSV markdown generators,
the JSON CV, the per-item pages, the demo blog and portfolio, and the talk map
have all been removed.
