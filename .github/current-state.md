# Current State

_Last updated: April 2026_

## Source-of-truth order (phased model)

### Phase 1 — Current (pre-canonicalization)

Reconciliation between HTML and DB is complete (HTML→DB gap = 0, DB→HTML gap = 0 as of April 2026). Both are valid sources; keep them in sync.

1. Site HTML (`docs/pillars/*.html`) — rendered policy cards; most recently edited content
2. `policy/catalog/policy_catalog_v2.sqlite` — 3,810 positions in v2 ID format; canonical structured catalog
3. `policy/foundations/pillars/` narrative markdown — prose source; may lag behind site HTML

**Any new position added to HTML must be backfilled into the DB in the same commit.**

### Phase 2 — Post-canonicalization (target)

Once PolicyOS and the generation pipeline are complete:

1. `policy/catalog/policy_catalog_v2.sqlite` — canonical source of truth for all policy positions
2. `policy/foundations/pillars/*/overview.md` and `policy/foundations/pillars/*/policy.md` — source for narrative prose
3. `docs/pillars/*.html` — generated output; do not hand-edit policy cards

## Site structure (live)

The site (`docs/`) serves the published platform at https://alistardust.github.io/freedom-and-dignity-project/.

**Current pillar count: 25** across 5 foundations. All live at `docs/pillars/<slug>.html`.

Each pillar page uses:
- `<style>:root { --accent-color: #...; }</style>` — per-pillar accent color only
- All other styles from `docs/assets/css/style.css` (shared, DRY)
- `docs/assets/js/data.js` — `window.ARP` — source of truth for foundations + pillar registry
- `docs/assets/js/app.js` — injects nav links, WIP banner, Roadmap link, scrollspy, dynamic counts

## Pillar registry (data.js)

| # | ID | Title | Foundation | Scope codes |
|---|----|-------|------------|-------------|
| 1 | `executive_power` | Executive Power | Accountable Power (I) | GOV, EXE |
| 2 | `elections_and_representation` | Elections & Representation | Accountable Power (I) | ELE |
| 3 | `anti_corruption` | Anti-Corruption | Accountable Power (I) | COR |
| 4 | `checks_and_balances` | Checks & Balances | Accountable Power (I) | SYS, OVR |
| 5 | `courts_and_judicial_system` | Courts & Judicial System | Accountable Power (I) | JUD |
| 6 | `term_limits_and_fitness` | Term Limits & Fitness | Accountable Power (I) | TRM |
| 7 | `administrative_state` | Administrative State | Accountable Power (I) | ADM |
| 8 | `antitrust_and_corporate_power` | Antitrust & Corporate Power | We the People (II) | COR-FIN, MED |
| 9 | `information_and_media` | Information & Media | We the People (II) | MED, INF |
| 10 | `equal_justice_and_policing` | Equal Justice & Policing | Equal Justice (III) | JUS |
| 11 | `immigration` | Immigration | Equal Justice (III) | IMM |
| 12 | `rights_and_civil_liberties` | Rights & Civil Liberties | Equal Justice (III) | RGT |
| 13 | `foreign_policy` | Foreign Policy | Equal Justice (III) | FPL |
| 14 | `gun_policy` | Gun Policy | Real Freedom (IV) | GUN (cross-scope) |
| 15 | `technology_and_ai` | Technology & AI | Real Freedom (IV) | TEC, PAT |
| 16 | `consumer_rights` | Consumer Rights | Real Freedom (IV) | CON, RPR |
| 17 | `healthcare` | Healthcare | Freedom to Thrive (V) | HLT |
| 18 | `taxation_and_wealth` | Taxation & Wealth | Freedom to Thrive (V) | ECO, TAX |
| 19 | `environment_and_agriculture` | Environment & Agriculture | Freedom to Thrive (V) | ENV, AGR, EWT |
| 20 | `infrastructure_and_public_goods` | Infrastructure & Public Goods | Freedom to Thrive (V) | INF |
| 21 | `education` | Education | Freedom to Thrive (V) | EDU |
| 22 | `labor_and_workers_rights` | Labor & Workers' Rights | Freedom to Thrive (V) | LAB |
| 23 | `housing` | Housing | Freedom to Thrive (V) | HOU |
| 24 | `legislative_reform` | Legislative Reform | Accountable Power (I) | LEG |
| 25 | `science_technology_space` | Science, Technology & Space | Real Freedom (IV) | STS |

## Site page inventory

```
docs/
  index.html              — Homepage (foundations + pillar cards)
  foundations.html        — 5-foundation deep dive
  mission.html            — Platform mission statement
  constitution.html       — Framework & governing principles
  classification.html     — Rule ID system explanation
  about-ai.html           — AI use transparency page
  about-us.html           — About the project
  get-involved.html       — Contribution guidelines
  roadmap.html            — Project roadmap (tracks, pillar status)
  adversarial-review.html — Adversarial policy review
  pillars/index.html      — Full pillar index (fullview grid)
  pillars/*.html          — 25 pillar pages
  compare/index.html      — Party comparison index
  compare/*.html          — 6 party comparison pages (DSA, Green, Libertarian, Democrat, Republican, Working Families)
```

## Frontend architecture

### JavaScript
- `app.js` — central injection hub: nav/footer links, WIP banner, Roadmap link, section-reveal IntersectionObserver, pil-snav scrollspy, `[data-dynamic]` count fills
- `data.js` — `window.ARP` object: foundations array, pillars array, helper methods
- No frameworks. Vanilla ES5-compatible JS.

### CSS
- `style.css` — all shared styles (no inline CSS in HTML except `--accent-color` per pillar)
- `--accent-color` CSS variable used throughout for per-pillar theming of policy cards, nav pills, research headings

### Dynamic values
- `[data-dynamic="pillar-count"]` — filled from `ARP.pillars.length`
- `[data-dynamic="foundation-count"]` — filled from `ARP.foundations.length`
- `[data-dynamic="policy-count"]` — counts `.policy-card` elements on current page
- `[data-dynamic="family-count"]` — counts unique family prefixes on current page

## Catalog state (`policy/catalog/policy_catalog_v2.sqlite`)

Rebuilt April 2026. Reconciliation gap = 0 (HTML and DB in sync).

### Current totals

- 3,810 positions (`XXXX-XXXX-0000` v2 ID format)
- 506 subdomains
- 3,810 legacy ID mappings (provenance)
- `plain_language` column populated for all positions (backfill complete)

To rebuild: `python3 scripts/build-catalog-v2.py`

## PolicyOS

System-rules layer in development. Three-layer hierarchy:

1. **Platform values** — `policy/policyos/policyos_platform_values_v1.md`
2. **System principles** — `policy/policyos/policyos_1_0_rules_proposal.md`
3. **Authoring OS** — `policy/policyos/policyos_authoring_os_v1.md`

See the handoff file and README in `policy/policyos/` for current status.

## Known open items

- **Citation fixes** — orphan footnote wiring and uncited statistics in progress (automated agents running)
- **PolicyOS canonicalization** — values layer locked; principles and authoring OS under review
- **Plain language** — all 3,810 positions have `rule-plain` descriptions
- **Science/Technology/Space content** — live page; content in development


## Site structure (live)

The site (`docs/`) serves the published platform at https://alistardust.github.io/freedom-and-dignity-project/.

**Current pillar count: 25** across 5 foundations. All live at `docs/pillars/<slug>.html`.

Each pillar page uses:
- `<style>:root { --accent-color: #...; }</style>` — per-pillar accent color only
- All other styles from `docs/assets/css/style.css` (shared, DRY)
- `docs/assets/js/data.js` — `window.ARP` — source of truth for foundations + pillar registry
- `docs/assets/js/app.js` — injects nav links, WIP banner, Roadmap link, scrollspy, dynamic counts

## Pillar registry (data.js)

| # | ID | Title | Foundation | Scope codes |
|---|----|-------|------------|-------------|
| 1 | `executive_power` | Executive Power | Accountable Power (I) | GOV, EXE |
| 2 | `elections_and_representation` | Elections & Representation | Accountable Power (I) | ELE |
| 3 | `anti_corruption` | Anti-Corruption | Accountable Power (I) | COR |
| 4 | `checks_and_balances` | Checks & Balances | Accountable Power (I) | SYS, OVR |
| 5 | `courts_and_judicial_system` | Courts & Judicial System | Accountable Power (I) | JUD |
| 6 | `term_limits_and_fitness` | Term Limits & Fitness | Accountable Power (I) | TRM |
| 7 | `administrative_state` | Administrative State | Accountable Power (I) | ADM |
| 8 | `antitrust_and_corporate_power` | Antitrust & Corporate Power | We the People (II) | COR-FIN, MED |
| 9 | `information_and_media` | Information & Media | We the People (II) | MED, INF |
| 10 | `equal_justice_and_policing` | Equal Justice & Policing | Equal Justice (III) | JUS |
| 11 | `immigration` | Immigration | Equal Justice (III) | IMM |
| 12 | `rights_and_civil_liberties` | Rights & Civil Liberties | Equal Justice (III) | RGT |
| 13 | `foreign_policy` | Foreign Policy | Equal Justice (III) | FPL |
| 14 | `gun_policy` | Gun Policy | Real Freedom (IV) | GUN (cross-scope) |
| 15 | `technology_and_ai` | Technology & AI | Real Freedom (IV) | TEC, PAT |
| 16 | `consumer_rights` | Consumer Rights | Real Freedom (IV) | CON, RPR |
| 17 | `healthcare` | Healthcare | Freedom to Thrive (V) | HLT |
| 18 | `taxation_and_wealth` | Taxation & Wealth | Freedom to Thrive (V) | ECO, TAX |
| 19 | `environment_and_agriculture` | Environment & Agriculture | Freedom to Thrive (V) | ENV, AGR, EWT |
| 20 | `infrastructure_and_public_goods` | Infrastructure & Public Goods | Freedom to Thrive (V) | INF |
| 21 | `education` | Education | Freedom to Thrive (V) | EDU |
| 22 | `labor_and_workers_rights` | Labor & Workers' Rights | Freedom to Thrive (V) | LAB |
| 23 | `housing` | Housing | Freedom to Thrive (V) | HOU |
| 24 | `legislative_reform` | Legislative Reform | Accountable Power (I) | LEG |
| 25 | `science_technology_space` | Science, Technology & Space | Real Freedom (IV) | STS |

**Pillars in progress / stub stage:**
- `science_technology_space` (STS) — live page; content in development.

## Site page inventory

```
docs/
  index.html              — Homepage (foundations + pillar cards)
  foundations.html        — 5-foundation deep dive
  mission.html            — Platform mission statement
  constitution.html       — Framework & governing principles
  classification.html     — Rule ID system explanation
  about-ai.html           — AI use transparency page
  about-us.html           — About the project
  get-involved.html       — Contribution guidelines
  roadmap.html            — Project roadmap (tracks, pillar status)
  adversarial-review.html — Adversarial policy review
  pillars/index.html      — Full pillar index (fullview grid)
  pillars/*.html          — 25 pillar pages
  compare/index.html      — Party comparison index
  compare/*.html          — 6 party comparison pages (DSA, Green, Libertarian, Democrat, Republican, Working Families)
```

## Frontend architecture

### JavaScript
- `app.js` — central injection hub: nav/footer links, WIP banner, Roadmap link, section-reveal IntersectionObserver, pil-snav scrollspy, `[data-dynamic]` count fills
- `data.js` — `window.ARP` object: foundations array, pillars array, helper methods
- No frameworks. Vanilla ES5-compatible JS.

### CSS
- `style.css` — all shared styles (no inline CSS in HTML except `--accent-color` per pillar)
- `--accent-color` CSS variable used throughout for per-pillar theming of policy cards, nav pills, research headings

### Dynamic values
- `[data-dynamic="pillar-count"]` — filled from `ARP.pillars.length`
- `[data-dynamic="foundation-count"]` — filled from `ARP.foundations.length`
- `[data-dynamic="policy-count"]` — counts `.policy-card` elements on current page
- `[data-dynamic="family-count"]` — counts unique family prefixes on current page

## Catalog state (policy/catalog/policy_catalog_v2.sqlite)

The DB was last rebuilt from source logs in 2025. It is **pre-reconciliation** — it does not fully reflect policy cards added to the site HTML after that point, and some DB entries are not yet on the site.

### Current totals (pre-reconciliation)

- 1,554 `policy_items` (structured positions with prefixed IDs)
- `legacy_policy_items` (old numeric checkpoint items, preserved for provenance)
- 36 `record_links`
- 629 `prose_rule_mentions`

**Important:** DB status fields (`MISSING`, `INCLUDED`, etc.) reflect the state at last catalog build and have not been reconciled against the current site HTML. A `MISSING` entry may already be present on the site under a policy card. Do not treat DB status as authoritative until after the reconciliation audit. Rebuild the catalog with `scripts/import_policy_catalog.py` once source logs and HTML are reconciled.

## Known issues for human review

- **Reconciliation audit** — HTML (2,935 policy cards) and DB (1,554 policy_items) have diverged. A full 3-way reconciliation (HTML ↔ DB ↔ source logs) is the primary open infrastructure item. Until complete, treat both sources as valid and flag divergences for human review.
- **Policy card ID audit** — a systematic scan of all `.policy-card` IDs for duplicates or format violations has not been done. Spot checks pass; a full audit is warranted before v1.0.
- **Orphan footnotes** — several pillar pages have footnotes defined in the reference list but never cited inline. Pages: `immigration.html` (fn1, fn3), `technology-and-ai.html` (fn1–fn3), `consumer-rights.html` (fn3), `courts-and-judicial-system.html` (fn5–fn6), `elections-and-representation.html` (fn4–fn7), `environment-and-agriculture.html` (fn3), `gun-policy.html` (fn4–fn5), `legislative-reform.html` (fn4), `term-limits-and-fitness.html` (fn3–fn4). These may represent content removed without updating the reference list, or inline citations accidentally omitted.
- **Foreign policy in related pillars** — `foreign-policy.html` is not yet referenced in "Related Pillars" sections of other pillar pages.
- **Compare page narratives** — the strengths/weaknesses narrative sections in compare pages do not yet discuss the foreign policy pillar.
- **Science/Technology/Space content** — `science-technology-space.html` is live but content is in development.

## Test suite

- **Unit (Vitest):** `npm run test:unit` — 42 tests, all passing
- **E2E (Playwright/Firefox):** `npm run test:e2e` — 222 tests, all passing
- `PILLAR_COUNT` constant in both test files — update when adding pillars

## Scaffolding tools

- `scripts/new-pillar.js` — generate a new pillar HTML page from CLI args
- `scripts/import_policy_catalog.py` — rebuild `policy/catalog/policy_catalog_v2.sqlite` from chat logs
