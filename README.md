# Poulin Systems Bulletin Board

A small, source-led publication surface for research notes, engineering observations, and governance commentary from [Poulin Systems](https://github.com/poulin-systems).

**Publication status (October 10, 2026): LIVE.** The source repository and inaugural article are public following operator-approved PR #1. The GitHub Pages website uses the manually prebuilt `gh-pages` branch. Home, article, About, CSS, and Atom feed were independently fetched over HTTPS and each returned HTTP 200 with the expected content. Organization-wide GitHub Actions remains disabled; no policy relaxation was required.

## What this is

- Dated bulletins with direct references to primary sources
- A readable archive and Atom feed
- No analytics, ads, account system, or public commenting surface
- Static GitHub Pages source with a manually prebuilt no-Jekyll release branch; no application server or secrets

The initial bulletin examines Anthropic's [October 8, 2026 Usage Policy update](https://www.anthropic.com/news/2026-usage-policy-update), with a clear separation between what Anthropic said and Poulin Systems' interpretation.

## Editorial and publication process

Read [PUBLICATION.md](PUBLICATION.md). Propose changes on a branch, run `python3 scripts/validate.py`, and submit a pull request. A successful automated check is **not** publication approval. Poulin Systems' human owner reviews, accepts, merges, and authorizes making this repository and Pages site public.

Changes drafted with AI assistance must be disclosed in the PR and remain the responsibility of the human publisher.

## Local preview

If Jekyll is available:

```bash
bundle exec jekyll serve --baseurl /bulletin-board
```

For an installed `jekyll` binary, `jekyll serve --baseurl /bulletin-board` also works. This site uses only native Liquid/Jekyll features (no theme dependency or remote assets).

## Deployment without GitHub Actions

Organization policy currently disables GitHub Actions, so the source's Jekyll/Liquid pages cannot be built by GitHub Pages. A **compiled static release** was committed on orphan branch `gh-pages` (release commit `463a4c0`), with `.nojekyll`, pre-rendered article pages, a feed, and build provenance. Pages points to `gh-pages:/`. The static `.nojekyll` publishing route succeeded while organization-wide Actions remained disabled. The live pages and feed were verified by HTTP and content checks.

The generator is `scripts/build_static.py` (Python 3 plus PyYAML). It refuses nonempty output and never pushes or changes Pages:

```bash
python3 -B scripts/validate.py
python3 -B scripts/build_static.py /absolute/new/empty/output-directory
```

Inspect the produced HTML, links, CSS, Atom feed, source commit provenance, and `.nojekyll` before an independently approved push of those files to `gh-pages`. Rebuild after content changes; merging to `main` **does not automatically deploy** while Actions remains disabled. Do not treat a queued Pages build request as successful deployment. A deployment is accepted only after verifying the actual public homepage, article, CSS and Atom feed.

Verified public website: https://poulin-systems.github.io/bulletin-board/. Public editorial source: [first bulletin](_posts/2026-10-10-the-other-half-of-ai-safety-is-us.md).

© 2026 Poulin Systems. No reuse license is granted by this repository unless explicitly stated.
