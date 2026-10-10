# Publication protocol

**Stage:** private candidate. Nothing in this repository is approved for public release merely because it has passed validation, been pushed, or received a pull request.

## Non-negotiable gates

1. Create and revise content on topic-specific branches.
2. Link directly to primary sources and fact-check claims, dates, and qualifiers.
3. Conduct a **public-boundary check**: exclude unpublished systems, credentials, private discussion transcripts, network topology, personal information, and internal repo names.
4. Ensure AI drafting or editing assistance is disclosed in the PR and, when relevant, the bulletin.
5. Run `python3 scripts/validate.py`; review the rendered site for clarity, accessibility, mobile layout, links, and feed validity.
6. Obtain Louis's explicit editorial acceptance. No agent may merge or authorize publicity on its own.
7. After acceptance, Louis merges to `main`, explicitly changes repository visibility to public, and separately enables Pages for `main` root (or directs an authorized operator to do those actions).
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
