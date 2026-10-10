# Publication protocol

**Stage (October 10, 2026):** operator-approved public source; website deployment pending external GitHub Actions organization policy. Public source is not proof that the website and feed are live. Future content and release changes still require human acceptance.

## Non-negotiable gates

1. Create and revise content on topic-specific branches.
2. Link directly to primary sources and fact-check claims, dates, and qualifiers.
3. Conduct a **public-boundary check**: exclude unpublished systems, credentials, private discussion transcripts, network topology, personal information, and internal repo names.
4. Ensure AI drafting or editing assistance is disclosed in the PR and, when relevant, the bulletin.
5. Run `python3 scripts/validate.py`; review the rendered site for clarity, accessibility, mobile layout, links, and feed validity.
6. Obtain Louis's explicit editorial acceptance. No agent may merge or authorize publicity on its own.
7. After acceptance, Louis merges approved editorial content to `main` and separately approves compiling and pushing the static release branch `gh-pages` as appropriate. The repository became public on October 10; current Pages source is `gh-pages:/` while organization Actions is disabled.
8. Record a public release URL and inspect the deployed post and feed. Until that verification, report publication as **not live**.

Automated checks are guardrails, not a proof that content is safe, correct, or licensed. Publication controls should be evaluated before broadening contributor access.

## Corrections

Correct factual errors promptly. For material corrections, add a visible dated note to the bulletin explaining what changed, while retaining ordinary Git history. Do not silently rewrite a claim that readers may have relied on.

## Editorial boundaries

Opinion is labeled as opinion. This board does not speak for referenced organizations. Ordinary criticism, disagreement, safety testing, and research are not treated as abuse. No personal attacks or private allegations. No analytics, ad networks, unsolicited data collection, or third-party comments in the initial release.

## Launch acceptance

- [ ] Independent editorial pass completed
- [ ] Primary-source details rechecked
- [ ] Privacy / public-boundary review completed
- [ ] Local validation passes
- [ ] Rendered website and feed inspected
- [ ] Human explicitly accepts editorial content and public release
- [ ] Visibility / Pages activation performed and verified

## October 10 release disposition

- GitHub PR #1 accepted and merged; public source release approved.
- Public repo and prebuilt `gh-pages` branch verified; Pages configured for `gh-pages:/`.
- Organization-wide new-Pages-creation prohibition restored after site configuration.
- Organization-wide Actions prohibition remains intact; repo-level activation is rejected by GitHub.
- Live website, article URL, and Atom feed returned HTTP 404. **Not live.**
- Remedy: organization owner enables Actions for the **selected `bulletin-board` repository**, allowing GitHub-owned deployment actions, and Pages deployment is retriggered. Independently verify all three public URLs before claiming completion.
- A no-Jekyll prebuilt branch is committed for reuse, but GitHub may still require Actions for the final deployment.
