# drprojects.github.io

Personal website of Damien Robert, plus the generator for the PDF CV.
Forked from [academicpages](https://github.com/academicpages/academicpages.github.io)
and substantially reworked.

## How this repository works

`_data/*.yml` is the **single source of truth**. Both the website and the PDF CV
are rendered from it, so they cannot drift apart:

```
_data/*.yml   <- the only files you edit by hand
   |
   +--> Jekyll        --> the website, including the /cv/ page
   +--> cv/build.py   --> Jinja2 --> LaTeX --> files/cv.pdf
```

### Adding content

| To add a... | Edit | Appears on |
|---|---|---|
| paper | `_data/publications.yml` | /publications/, /cv/, PDF |
| talk | `_data/talks.yml` | /talks/, /cv/ and PDF *if* `cv: true` |
| course | `_data/teaching.yml` | /teaching/, /cv/, PDF |
| repository | `_data/code.yml` | /code/, /cv/, PDF |
| news item | `_data/news.yml` | homepage, /news/ |
| review, chair role | `_data/service.yml` | /community/, PDF |
| organising committee | `_data/organizing.yml` | /community/ |
| student, collaborator, advisee | `_data/supervision.yml` | /community/, PDF |
| grant | `_data/grants.yml` | /community/ |
| job, degree, award, skill | the matching `_data/*.yml` | homepage or PDF |

`organizing.yml` and `grants.yml` ship empty with their schema in comments; the
Community page hides a section until it has entries.

The homepage distinctions strip is driven by `awards.yml`. Its `weight` field
orders that strip only (highest first), so the strip can lead with the Best Paper
Finalist while the CV stays reverse-chronological.

New co-authors go in `_data/authors.yml`; publications reference them by key.

### Controlling where an item appears

Every entry accepts two optional flags:

- `cv: false` — keep it on the website, leave it out of the PDF
  (used for MOOCs and high-school entries in `education.yml`)
- `web: false` — the reverse

**Talks are the exception**: they are opt-in for the PDF. There are 45 of them
and the CV shows a selected ~17, so a talk needs an explicit `cv: true` to be
printed. Everything else defaults to appearing in both.

## Commands

```bash
make install   # Ruby + Python dependencies
make serve     # preview at http://localhost:4000 — never touches the live site
make cv        # regenerate files/cv.pdf from _data (fetches live GitHub stars)
make check     # fail if files/cv.pdf is older than the data behind it
```

`make serve` layers `_config_dev.yml` over `_config.yml` to override `url`.
Without that override a local build still loads the **live** site's CSS, and you
end up reviewing production styling instead of your own changes.

## The CV

There is no HTML CV page. The **CV** nav item serves `files/cv.pdf` directly, so
there is only one CV to design and maintain. The intro paragraph in
`profile.yml` is shared between the homepage and the PDF.

## How the PDF is built

- `cv/drcv.sty` — all typography and layout. Every tunable value (accent colour,
  gutter width, spacing) is in the `DESIGN TOKENS` block at the top.
- `cv/templates/cv.tex.j2` — content structure only. Jinja delimiters are
  remapped to `((* ... *))` and `((( ... )))` so they do not collide with LaTeX.
- `cv/build.py` — loads the data, fetches GitHub star counts, renders, runs
  pdflatex twice, writes `files/cv.pdf`.

GitHub star and fork counts are fetched at build time into
`_data/github_stars.json`, which the homepage stats band also reads. They are
never hardcoded.

Graphical elements in the CV — the tinted header band, the publications-per-year
bar chart, the language meters — are all TikZ, driven by the same data. The
chart's counts come from `publication_histogram()` in `cv/build.py`.

`.github/workflows/build-cv.yml` rebuilds and commits the PDF on any push that
touches `_data/` or `cv/`, so a single push updates the site and the CV together.
GitHub Pages continues to build the website itself.

## Citation metrics

`_data/profile.yml` has a `metrics` block (citations, h-index) that prints in the
CV header. Google Scholar cannot be scraped legitimately, so update those numbers
by hand a few times a year and set `show: true` to display them.

---

## Upstream template

Documentation for the original template lives at
<https://academicpages.github.io/>. The pieces of it this site no longer uses
(the TSV markdown generators, the JSON CV, the per-item collection pages) have
been removed.
