# Pillars — Source Markdown

This directory contains the source markdown prose for each policy pillar.

Each subdirectory maps to one pillar and contains two files:

- `overview.md` — Narrative overview: why this area matters, the project's
  core argument, and what the platform stands for. Public-facing, accessible prose.

- `policy.md` — Policy section: the detailed policy positions, organized
  by policy family. This is the source for the rule cards rendered in
  `docs/pillars/<pillar>.html`.

## Relationship to the live site

During Phase 1 (pre-reconciliation), `docs/pillars/*.html` is the most
recently edited content and takes precedence over these markdown files where
they diverge.

During Phase 2 (post-reconciliation), `data/policy_catalog_v2.sqlite` will
be the canonical source for policy positions, and these markdown files will
be the source for narrative prose. The HTML will be generated output.

## Source of truth guidance

See `overview/ai-repo-context.md` for the current source-of-truth hierarchy
and phase status.
