# Damien Robert — website + CV
#
# _data/*.yml is the single source of truth. The website and the PDF CV are both
# rendered from it, so editing one file updates both.

SHELL := /bin/bash
JEKYLL := bundle exec jekyll
DEV_CONFIG := _config.yml,_config_dev.yml

.DEFAULT_GOAL := help

.PHONY: help serve build build-prod cv cv-offline check clean install

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install:  ## Install Ruby and Python dependencies
	bundle install
	python3 -m pip install -r cv/requirements.txt

serve:  ## Preview the site at http://localhost:4000 (live reload, never touches production)
	$(JEKYLL) serve --livereload --config $(DEV_CONFIG)

build:  ## Build the site into _site using the local-preview config
	$(JEKYLL) build --config $(DEV_CONFIG)

build-prod:  ## Build the site exactly as GitHub Pages will
	$(JEKYLL) build

cv:  ## Regenerate files/cv.pdf from _data (fetches live GitHub star counts)
	python3 cv/build.py

cv-offline:  ## Regenerate files/cv.pdf without hitting the network
	python3 cv/build.py --offline

check:  ## Fail if files/cv.pdf is older than the data it is built from
	@newest=$$(ls -t _data/*.yml cv/templates/*.j2 cv/drcv.sty 2>/dev/null | head -1); \
	if [ ! -f files/cv.pdf ]; then \
	  echo "files/cv.pdf is missing — run 'make cv'"; exit 1; \
	elif [ "$$newest" -nt files/cv.pdf ]; then \
	  echo "files/cv.pdf is STALE: $$newest is newer. Run 'make cv'."; exit 1; \
	else \
	  echo "files/cv.pdf is up to date."; \
	fi

clean:  ## Remove build artefacts
	rm -rf _site cv/build .jekyll-cache .jekyll-metadata
