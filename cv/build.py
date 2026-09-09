#!/usr/bin/env python3
"""Render the CV PDF from the website's _data/*.yml — the single source of truth.

    python cv/build.py                # fetch GitHub stars, build files/cv.pdf
    python cv/build.py --offline      # skip the network, use the cached counts
    python cv/build.py --keep-tex     # leave cv/build/cv.tex for inspection

Nothing in this script contains CV *content*. All of it lives in _data/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
CVDIR = ROOT / "cv"
BUILD = CVDIR / "build"
OUT = ROOT / "files" / "cv.pdf"
# Written into _data/ so the website can show live star counts too.
STARS_CACHE = DATA / "github_stars.json"

DATASETS = [
    "profile", "authors", "publications", "talks", "teaching",
    "code", "positions", "education", "awards", "service",
    "supervision", "skills",
]

# --------------------------------------------------------------------------
# LaTeX-safe text handling
# --------------------------------------------------------------------------

_TEX_ESCAPES = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}

# Emoji and pictographs: pdflatex cannot typeset them.
_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\U00002190-\U000021FF\U0000FE0F\U0000200D\U000024C2]+"
)

_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_MD_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_MD_ITAL = re.compile(r"(?<!\w)[_*]([^_*]+)[_*](?!\w)")


def strip_emoji(text: str) -> str:
    return _EMOJI.sub("", str(text)).replace("  ", " ").strip()


def tex(value) -> str:
    """Escape a plain string for LaTeX."""
    if value is None:
        return ""
    # A literal NBSP cannot be declared via \newunicodechar, so map it here.
    value = str(value).replace("\u00a0", "~")
    out = []
    for ch in str(value):
        out.append(_TEX_ESCAPES.get(ch, ch))
    return "".join(out)


def md2tex(value) -> str:
    """Convert a small subset of markdown (links, bold, italic) to LaTeX.

    Escaping is applied to the *non-markup* text only, so that generated
    control sequences such as \\href survive.
    """
    if value is None:
        return ""
    text = strip_emoji(str(value))

    placeholders: list[str] = []

    def stash(latex: str) -> str:
        placeholders.append(latex)
        return f"\x00{len(placeholders) - 1}\x00"

    def on_link(m):
        label, url = m.group(1), m.group(2)
        # The URL goes in verbatim except for % and #, which LaTeX still eats.
        safe_url = url.replace("%", r"\%").replace("#", r"\#")
        return stash(r"\href{%s}{%s}" % (safe_url, tex(label)))

    text = _MD_LINK.sub(on_link, text)
    text = _MD_BOLD.sub(lambda m: stash(r"\textbf{%s}" % tex(m.group(1))), text)
    text = _MD_ITAL.sub(lambda m: stash(r"\textit{%s}" % tex(m.group(1))), text)
    text = tex(text)

    for i, latex in enumerate(placeholders):
        text = text.replace(tex(f"\x00{i}\x00"), latex).replace(f"\x00{i}\x00", latex)
    return text


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------

def load_data() -> dict:
    data = {}
    for name in DATASETS:
        path = DATA / f"{name}.yml"
        if not path.exists():
            sys.exit(f"missing data file: {path.relative_to(ROOT)}")
        with path.open(encoding="utf-8") as fh:
            data[name] = yaml.safe_load(fh)
    return data


def report_unlinked_people(data):
    """Name people the website cannot link, so a typo does not fail silently.

    supervision.yml records plain names and the site resolves them against
    authors.yml. That is one fewer thing to keep in sync than a duplicated key,
    but a rename can quietly drop a link -- which is exactly how Loic Landrieu's
    homepage disappeared once. Printing the misses makes them visible.
    """
    known = {
        f"{v.get('first_name', '')} {v.get('last_name', '')}".strip()
        for v in data["authors"].values()
        if isinstance(v, dict)
    }
    missing = [
        (group["label"], person["name"])
        for group in data["supervision"]["groups"]
        for person in group["people"]
        if person["name"] not in known
    ]
    if missing:
        print(f"  note: {len(missing)} name(s) not in authors.yml, so they render "
              f"without a homepage link:")
        for label, name in missing:
            print(f"        {label}: {name}")


def publication_histogram(publications):
    """(years, counts, max) for the bar chart next to the Publications heading.

    Counts every CV-visible publication, including preprints under review, so
    the chart reflects output rather than acceptance timing.
    """
    counts = {}
    for pub in publications:
        year = pub.get("year")
        if year:
            counts[year] = counts.get(year, 0) + 1
    if not counts:
        return [], 0
    years = sorted(counts)
    full = list(range(years[0], years[-1] + 1))
    return [(y, counts.get(y, 0)) for y in full], max(counts.values())


def for_cv(items, default=True):
    """Filter a list on its `cv` flag.

    `default=False` makes inclusion opt-in, which is how talks work: there are
    45 of them and the CV shows a selected ~17.
    """
    return [i for i in items if i.get("cv", default)]


def author_names(data, keys, me_key="me"):
    """Resolve author keys to 'F. Last' strings, marking the CV owner."""
    out = []
    for key in keys:
        person = data["authors"].get(key)
        if person is None:
            out.append((tex(key), False))
            continue
        first = str(person.get("first_name", "")).strip()
        last = str(person.get("last_name", "")).strip()
        initials = " ".join(f"{p[0]}." for p in first.split() if p)
        out.append((tex(f"{initials} {last}".strip()), key == me_key))
    return out


# --------------------------------------------------------------------------
# GitHub stars
# --------------------------------------------------------------------------

def fetch_stars(repos: list[str], offline: bool) -> dict:
    cache = {}
    if STARS_CACHE.exists():
        cache = json.loads(STARS_CACHE.read_text())

    if offline:
        print("  stars: offline, using cache")
        return cache

    updated = dict(cache)
    for repo in repos:
        url = f"https://api.github.com/repos/{repo}"
        try:
            headers = {"Accept": "application/vnd.github+json",
                       "User-Agent": "drprojects-cv-build"}
            token = os.environ.get("GITHUB_TOKEN")
            if token:
                headers["Authorization"] = f"Bearer {token}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                payload = json.load(resp)
            updated[repo] = {
                "stars": payload.get("stargazers_count", 0),
                "forks": payload.get("forks_count", 0),
            }
            print(f"  stars: {repo} -> {updated[repo]['stars']}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            kept = cache.get(repo)
            print(f"  stars: {repo} FAILED ({exc}); "
                  f"{'using cached value' if kept else 'no cached value'}")
    updated["_fetched"] = date.today().isoformat()
    STARS_CACHE.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n")
    return updated


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------

def build(offline: bool, keep_tex: bool) -> int:
    data = load_data()

    repos = [c["repo"] for c in for_cv(data["code"]) if c.get("repo")]
    stars = fetch_stars(repos, offline)

    env = Environment(
        loader=FileSystemLoader(CVDIR / "templates"),
        block_start_string="((*", block_end_string="*))",
        variable_start_string="(((", variable_end_string=")))",
        comment_start_string="((#", comment_end_string="#))",
        trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True,
        undefined=StrictUndefined, autoescape=False,
    )
    env.filters.update(tex=tex, md2tex=md2tex, strip_emoji=strip_emoji)

    report_unlinked_people(data)
    hist, hist_max = publication_histogram(for_cv(data["publications"]))

    template = env.get_template("cv.tex.j2")
    rendered = template.render(
        d=data,
        stars=stars,
        pub_hist=hist,
        pub_hist_max=hist_max,
        for_cv=for_cv,
        author_names=lambda keys: author_names(data, keys),
        today=date.today(),
    )

    BUILD.mkdir(parents=True, exist_ok=True)
    tex_path = BUILD / "cv.tex"
    tex_path.write_text(rendered, encoding="utf-8")
    shutil.copy(CVDIR / "drcv.sty", BUILD / "drcv.sty")

    # Assets referenced from the template (the portrait).
    assets = BUILD / "images"
    assets.mkdir(exist_ok=True)
    portrait_src = CVDIR / "assets" / "portrait.png"
    if portrait_src.exists():
        shutil.copy(portrait_src, assets / "portrait.png")

    logos_src = CVDIR / "assets" / "logos"
    if logos_src.exists():
        shutil.copytree(logos_src, BUILD / "logos", dirs_exist_ok=True)

    print("  latex: running pdflatex (2 passes)")
    for i in range(2):
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "cv.tex"],
            cwd=BUILD, capture_output=True, text=True, errors="replace",
        )
        if proc.returncode != 0:
            log = (BUILD / "cv.log")
            errors = [ln for ln in proc.stdout.splitlines()
                      if re.search(r"^(.*:\d+:|!)", ln)][:25]
            print("\n".join(errors) or proc.stdout[-3000:], file=sys.stderr)
            print(f"\npdflatex failed on pass {i + 1}. Full log: {log}", file=sys.stderr)
            return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(BUILD / "cv.pdf", OUT)

    pages = subprocess.run(["pdfinfo", str(OUT)], capture_output=True, text=True)
    npages = next((l.split()[-1] for l in pages.stdout.splitlines()
                   if l.startswith("Pages:")), "?")
    print(f"\n  wrote {OUT.relative_to(ROOT)}  ({npages} pages)")

    if not keep_tex:
        for suffix in (".aux", ".log", ".out"):
            (BUILD / f"cv{suffix}").unlink(missing_ok=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--offline", action="store_true",
                    help="skip the GitHub API, reuse cv/stars.json")
    ap.add_argument("--keep-tex", action="store_true",
                    help="keep the intermediate .tex and .log")
    args = ap.parse_args()
    print("building CV from _data/")
    return build(args.offline, args.keep_tex)


if __name__ == "__main__":
    raise SystemExit(main())
