# Poulin Systems Bulletin Board

A small, source-led publication surface for research notes, engineering observations, and governance commentary from [Poulin Systems](https://github.com/poulin-systems).

**Publication status:** private staging, not approved for public release. The launch proposal lives on `editorial/bulletin-board-launch`. Public publication requires a separate human acceptance decision.

## What this is

- Dated bulletins with direct references to primary sources
- A readable archive and Atom feed
- No analytics, ads, account system, or public commenting surface
- Static GitHub Pages/Jekyll implementation; no application server or secrets

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

Public address **after approval and Pages activation:** `https://poulin-systems.github.io/bulletin-board/`. Until then, that URL is not claimed to be active.

© 2026 Poulin Systems. No reuse license is granted by this repository unless explicitly stated.
