# Freedom and Dignity Project

> ⚠️ **Name Notice — Placeholder Name**
>
> "Freedom and Dignity Project" is a working name derived from the repository slug while a permanent
> platform name is selected. It is **not a final name**. All references to it in this repository,
> website, and documentation are temporary and will be updated once a name is confirmed.

This repository contains the source code, policy content, and tooling for an active U.S. political platform in development. The platform is organized around 25 policy pillars grouped into 5 foundations. The live site is published at https://alistardust.github.io/freedom-and-dignity-project/.

## Repository layout

```text
/
├── docs/               Website source — served by GitHub Pages
│   ├── assets/         Shared CSS (style.css), JS (app.js, data.js), and images
│   ├── pillars/        25 pillar HTML pages
│   └── compare/        Party comparison pages
├── pillars/            Narrative markdown source (per-pillar overview and policy prose)
├── overview/           Project framing, current state, and high-level structure
├── strategy/           Roadmap and movement/communications planning
├── sources/            Historical chat log transcripts (used in initial catalog build)
├── data/               policy_catalog.sqlite — structured policy position catalog
├── scripts/            Import, generation, and maintenance scripts
├── tests/              Unit tests (Vitest) and E2E tests (Playwright/Firefox)
├── research/           Internal research files — gitignored, not committed
└── system_rules.md     Cross-domain system rule architecture summary
```

## Current state

- **Live site:** https://alistardust.github.io/freedom-and-dignity-project/
- **Pillars:** 25 active pillar pages across 5 foundations
- **Policy position cards:** 2,935 `.policy-card` elements across all pillar pages
- **Catalog:** `data/policy_catalog.sqlite` — 1,554 `policy_items`, 629 `prose_rule_mentions`, 36 `record_links` (pre-reconciliation; see below)

## Source of truth (phased model)

### Phase 1 — Current (pre-reconciliation)

HTML and the DB both contain valid content, but they have diverged:

- The site HTML (`docs/pillars/*.html`) has 2,935 policy cards, including positions added after the last DB rebuild.
- The DB (`data/policy_catalog.sqlite`) has 1,554 policy items, some of which are not yet reflected on the site.
- **A full 3-way reconciliation audit is required before either is treated as exclusively authoritative.**
- Divergences are flagged for human review. Neither source blindly overrides the other.

**During Phase 1:** HTML edits are valid. Any new positions added to HTML must be backfilled into the DB in the same commit. Do not treat DB status fields as definitive — `MISSING` in the DB does not mean the position is absent from the site.

### Phase 2 — Post-reconciliation (target)

Once reconciliation is complete:

- `data/policy_catalog.sqlite` is the **canonical source of truth** for all policy positions.
- `pillars/*/overview.md` and `pillars/*/policy.md` are the source for narrative prose.
- `docs/pillars/*.html` is **generated output** — do not hand-edit policy cards.
- New positions are authored in the DB first, then the site is regenerated at build time.

## Catalog

The catalog is stored in `data/policy_catalog.sqlite`. See `data/README.md` for full schema documentation.

Key tables:

- `policy_items` — structured policy positions with prefixed IDs (e.g., `HLT-COV-003`)
- `legacy_policy_items` — old numeric checkpoint items (preserved for provenance, not primary)
- `record_links` — legacy-to-structured ID conversions (36 entries)
- `prose_rule_mentions` — IDs mentioned in prose/context but not yet promoted to canonical records (629 entries)

Useful views:

- `deduped_catalog_entries` — canonical corpus without legacy numeric duplicates
- `unresolved_prose_rule_mentions` — IDs mentioned in context but not yet formalized

Historical reference sources (used in initial catalog build, retained for provenance):

- `sources/branch_branch_political_project_main.txt`
- `sources/branch_political_project_brainstorm.txt`

## Rebuilding the catalog

```bash
scripts/import_policy_catalog.py
```

The importer:

- preserves all source occurrences
- picks canonical records deterministically, preferring the main branch and later occurrences within a source when the same ID appears more than once
- seeds named structured IDs that were identified in the source logs but never formalized as pipe-delimited rows
- converts legacy numeric checkpoint items to structured IDs through `record_links`
- preserves prose-only ID mentions in a separate table so provisional or superseded IDs are not lost

See `data/README.md` for schema details and `overview/current-state.md` for the current audit state.

## Build architecture

### Current (Phase 1)

Policy card HTML in `docs/pillars/*.html` is hand-authored. `docs/assets/js/data.js` is the registry for foundations and pillars. `docs/assets/js/app.js` injects nav, footer, WIP banner, and dynamic counts at runtime.

### Target (Phase 2)

A build pipeline (`scripts/generate-site.py`, TBD) will render `docs/pillars/*.html` from `data/policy_catalog.sqlite` + pillar narrative markdown. Until that pipeline exists, HTML edits must be backfilled into the DB in the same commit.

## Documentation maintenance

Any commit that changes the following **must** update the relevant repo documentation in the same commit:

- Pillar count or structure → update `overview/current-state.md` pillar registry + `README.md`
- Policy card count or schema → update `data/README.md` + `overview/current-state.md`
- DB schema changes → update `data/README.md` + `system_rules.md` counts
- New architectural decisions → update `.github/copilot-instructions.md` + `overview/current-state.md`
- New scripts or tooling → update `README.md` "Scripts" section

"Repo documentation" = `README.md`, `system_rules.md`, `overview/*.md`, `data/README.md`, `.github/copilot-instructions.md`.  
"Docs" (without qualifier) = the website in `docs/`. Never confuse the two.

## Contributing

See `docs/get-involved.html` on the live site for contribution guidelines. All policy additions must follow the citation and quality standards in `.github/copilot-instructions.md`. New policy positions require a SCOPE-FAM-NNN structured ID before they are considered canonical.
