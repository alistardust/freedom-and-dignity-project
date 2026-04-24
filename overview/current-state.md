# Current State

_Last updated: April 2026_

## Source-of-truth order

1. Formal structured IDs in `sources/branch_political_project_brainstorm.txt` and `sources/branch_branch_political_project_main.txt` (primary sources)
2. Later contextual summary blocks in those chats when earlier mappings conflict
3. `data/policy_catalog.sqlite`
4. Pillar HTML under `docs/pillars/` (live site source — this is the current canonical policy text)
5. Pillar markdown under `pillars/` (legacy research source; may be outdated relative to site HTML)

## Site structure (live)

The site (`docs/`) serves the published platform at https://alistardust.github.io/american-renewal-project/.

**Current pillar count: 24** across 5 foundations. All live at `docs/pillars/<slug>.html`.

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

**Pillars in progress / stub stage:**
- `foreign_policy` (FPL) — 50 rules, 9 families, added April 2026. Compare page coverage rows added; narrative "strengths/weaknesses" sections not yet expanded.
- Science, Technology & Space (STS) — in development; agent in progress.

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
  pillars/*.html          — 24 pillar pages
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

## Catalog state (data/policy_catalog.sqlite)

The DB was last rebuilt from chat logs in July 2025. It is **pre-expansion** — it does not reflect rules added to the site HTML after that point.

### Pre-expansion totals
- 101 `policy_items` (legacy numeric checkpoint items)
- 1,095 `policy_items` (structured IDs, 20 scope codes)
- 138 `record_links`
- 888 `prose_rule_mentions`

**Note:** Significant new rules added after July 2025 (HLT-COV, HLT-RTT, FPL-*, STS-* pending) are in site HTML but not yet in the DB. Rebuild with `scripts/import_policy_catalog.py` once the chat logs are updated to include these additions.

## Known issues for human review

- **Orphan footnotes** — several pillar pages have footnotes defined in the reference list but never cited inline. Pages: `immigration.html` (fn1, fn3), `technology-and-ai.html` (fn1–fn3), `consumer-rights.html` (fn3), `courts-and-judicial-system.html` (fn5–fn6), `elections-and-representation.html` (fn4–fn7), `environment-and-agriculture.html` (fn3), `gun-policy.html` (fn4–fn5), `legislative-reform.html` (fn4), `term-limits-and-fitness.html` (fn3–fn4). These may represent content that was removed without updating the reference list, or inline citations that were accidentally omitted.
- **Rule ID audit** — a systematic scan of all `.policy-card` IDs for duplicates or format violations has not been done. Spot checks pass; a full audit is warranted before v1.0.
- **Foreign policy in related pillars** — `foreign-policy.html` is not yet referenced in "Related Pillars" sections of other pillar pages.
- **Compare page narratives** — the strengths/weaknesses narrative sections in compare pages do not yet discuss the foreign policy pillar.
- **Science/Technology/Space** — pending `science-space` agent; once complete, register in `data.js`, add to pillars index, update E2E counts.

## Test suite

- **Unit (Vitest):** `npm run test:unit` — 41 tests, all passing
- **E2E (Playwright/Firefox):** `npm run test:e2e` — 222 tests, all passing
- `PILLAR_COUNT` constant in both test files — update when adding pillars

## Scaffolding tools

- `scripts/new-pillar.js` — generate a new pillar HTML page from CLI args
- `scripts/import_policy_catalog.py` — rebuild `data/policy_catalog.sqlite` from chat logs
