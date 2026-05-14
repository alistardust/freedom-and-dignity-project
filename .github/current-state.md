# Current State

_Last updated: May 2026_

## Source-of-truth order (phased model)

### Phase 1 — Current (pre-canonicalization)

Reconciliation between HTML and DB is complete (HTML→DB gap = 0, DB→HTML gap = 0 as of April 2026). Both are valid sources; keep them in sync.

1. Site HTML (`docs/policy/*.html`) — rendered policy cards; most recently edited content
2. `policy/catalog/policy_catalog_v2.sqlite` — canonical structured catalog (`SELECT COUNT(*) FROM positions` for current count)
3. `policy/foundations/<foundation>/<policy-area>/` narrative markdown — prose source; may lag behind site HTML

**Any new position added to HTML must be backfilled into the DB in the same commit.**

### Phase 2 — Post-canonicalization (target)

Once PolicyOS and the generation pipeline are complete:

1. `policy/catalog/policy_catalog_v2.sqlite` — canonical source of truth for all policy positions
2. `policy/foundations/<foundation>/<policy-area>/overview.md` and `policy/foundations/<foundation>/<policy-area>/policy.md` — source for narrative prose
3. `docs/policy/*.html` — generated output; do not hand-edit policy cards

## Site structure (live)

The site (`docs/`) serves the published platform at https://alistardust.github.io/freedom-and-dignity-project/.

**Policy areas:** Active pages across 5 foundations. All live at `docs/policy/<slug>.html`. See [Policy area registry](#policy-area-registry-datajs) below for the current list.

Each policy area page uses:
- `<style>:root { --accent-color: #...; }</style>` — per-policy-area accent color only
- All other styles from `docs/assets/css/style.css` (shared, DRY)
- `docs/assets/js/data.js` — `window.ARP` — source of truth for foundations + policy area registry
- `docs/assets/js/app.js` — injects nav links, WIP banner, Roadmap link, scrollspy, dynamic counts

## Policy area registry (data.js)

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
  index.html              — Homepage (foundations + policy area cards)
  foundations.html        — 5-foundation deep dive
  mission.html            — Platform mission statement
  plan.html               — The Plan: strategic brief and three-phase roadmap (nav: "The Plan")
  approach.html           — Legacy page; de-navved; still accessible at direct URL
  constitution.html       — Framework & governing principles
  classification.html     — Rule ID system explanation
  about-ai.html           — AI use transparency page
  about-us.html           — About the project
  get-involved.html       — Contribution guidelines
  roadmap.html            — Project roadmap (tracks, policy area status)
  adversarial-review.html — Adversarial policy review
  policyos.html           — PolicyOS system rules layer (generated)
  policy/index.html       — Full policy area index (fullview grid)
  policy/*.html           — Policy area pages
  compare/index.html      — Party comparison index
  compare/*.html          — 6 party comparison pages (DSA, Green, Libertarian, Democrat, Republican, Working Families)
```

**Nav links (4-link primary nav):** Home, Problem, The Plan (`policy/plan.html`), Get Involved

## Frontend architecture

### JavaScript
- `app.js` — central injection hub: nav/footer links, WIP banner, Roadmap link, section-reveal IntersectionObserver, pil-snav scrollspy, `[data-dynamic]` count fills
- `data.js` — `window.ARP` object: foundations array, policyAreas array, helper methods
- No frameworks. Vanilla ES5-compatible JS.

### CSS
- `style.css` — all shared styles (no inline CSS in HTML except `--accent-color` per policy area)
- `--accent-color` CSS variable used throughout for per-policy-area theming of policy cards, nav pills, research headings

### Dynamic values
- `[data-dynamic="policy-area-count"]` — filled from `ARP.policyAreas.length`
- `[data-dynamic="foundation-count"]` — filled from `ARP.foundations.length`
- `[data-dynamic="policy-count"]` — counts `.policy-card` elements on current page
- `[data-dynamic="family-count"]` — counts unique family prefixes on current page

## Catalog state (`policy/catalog/policy_catalog_v2.sqlite`)

Rebuilt April 2026. Reconciliation gap = 0 (HTML and DB in sync).

### Current totals

- Positions in `XXXX-XXXX-0000` v2 ID format — run `sqlite3 policy/catalog/policy_catalog_v2.sqlite "SELECT COUNT(*) FROM positions"` for current count
- 506 subdomains
- `plain_language` column populated for all positions (backfill complete)

To rebuild: `python3 scripts/build-catalog-v2.py`

## PolicyOS

System-rules layer in development. Three-layer hierarchy:

1. **Platform values** — `policy/policyos/policyos_platform_values_v1.md`
2. **System principles** — `policy/policyos/policyos_1_0_rules_proposal.md` — 11 families (KERN/GEOG/FEDR/REGD/ENFA/AIGV/ECOL/THRV/DEMO/PRIV/ECON)
3. **Authoring OS** — `policy/policyos/policyos_authoring_os_v1.md`
4. **Governance** — `policy/policyos/policyos_governance_v1.md` — amendment process and policy area compliance review gate

All three layers are canonicalized as of 2026-04-27. Amendments follow the process in `policyos_governance_v1.md`.

## Known open items

- **Policy card completion (Issue #7)** — **PHASE 4 COMPLETE**. All remaining `rule-body` cards were converted to canonical `rule-stmt` + `rule-notes` in policy area source files and merged to `main` (May 2026). Build and test suite pass. DB sync ran for valid rows; remaining catalog edge cases are tracked in Known issues.
- **154 DB-gap IDs** — backfill script found 154 HTML card IDs with no matching DB row (81 v2-format, 73 v1-format). These are status-included cards with rule_notes already in HTML; they do not block Phase 4. v2-format IDs can be upserted; v1-format require migration first. Track as post-Phase-4 cleanup.
- **Policy card audit** — **complete** as of May 2026; zero `status-missing` cards remain; all cards are `status-included`
- **Consumer Rights BNPL family** — 9 proposal cards added (CNSR-BNPL-0001 through 0009); CNSR-PDLS-0007 retired; DB and HTML in sync
- **PolicyOS canonicalization** — **complete** as of 2026-04-27; all three layers locked; governance process defined
- **Plain language** — all positions have `rule-plain` descriptions
- **Science/Technology/Space content** — live page; content expanded May 2026
- **Citation fixes** — orphan footnote wiring and uncited statistics; see Known issues below
- **[VERIFY] markers** — adversarial review agents left `[VERIFY]` markers on uncertain thresholds throughout policy cards; requires human review before publication

## Research documents

Background research committed to `policy/research/`:

- `us-constitution-adversarial-review.md` — structural failures, loopholes, exploitation vectors in the U.S. Constitution (incl. *Trump v. United States*, 2024 immunity ruling)
- `new-bill-of-rights-adversarial-review.md` — per-amendment adversarial analysis of the project's proposed New Bill of Rights; 15 issues identified (some critical: standing, enforcement, horizontal application)
- `senate-reform-research.md` — malapportionment data (68.5:1 WY-CA ratio), filibuster history, reform proposals, comparative democracy analysis; ⚠ several calculated figures flagged for human verification before publication
- `research/` — per-policy-area background research used to draft policy cards
- `bnpl/bnpl_policy_overview.md` — BNPL market analysis, regulatory framework gaps, enforcement history; source document for CNSR-BNPL-0001 through 0009


## Known issues for human review

- **154 HTML-only card IDs** — 154 card IDs exist in HTML source but have no DB row: 81 are valid v2-format (can be upserted), 73 are v1-format (need migration). All have rule_notes in HTML; flagged during Phase 3 backfill. Post-Phase-4 cleanup task.
- **Catalog FK/domain drift in legacy rows** — some `positions` rows still carry legacy domain/subdomain pairings (for example `CRTS-*`) that do not satisfy current FK mappings; these rows block full automated upsert until normalized.
- **[VERIFY] markers in policy cards** — adversarial review agents left `[VERIFY]` markers on uncertain legal thresholds and regulatory figures throughout policy cards across all policy areas; requires human review before publication
- **Policy card ID audit** — a systematic scan of all `.policy-card` IDs for duplicates or format violations has not been done; spot checks pass; a full audit is warranted before v1.0
- **Orphan footnotes** — several policy area pages have footnotes defined in the reference list but never cited inline: `policy/immigration.html` (fn1, fn3), `policy/technology-and-ai.html` (fn1–fn3), `policy/consumer-rights.html` (fn3), `policy/courts-and-judicial-system.html` (fn5–fn6), `policy/elections-and-representation.html` (fn4–fn7), `policy/environment-and-agriculture.html` (fn3), `policy/gun-policy.html` (fn4–fn5), `policy/legislative-reform.html` (fn4), `policy/term-limits-and-fitness.html` (fn3–fn4)
- **Senate reform research figures** — `policy/research/senate-reform-research.md` contains ⚠ `[FLAG FOR HUMAN VERIFICATION]` markers on calculated figures (e.g., "17-18% of population controls 51 seats") that need primary source checking before publication
- **New Bill of Rights adversarial review** — 15 issues identified in `policy/research/new-bill-of-rights-adversarial-review.md`, some critical (standing, enforcement, horizontal application); draft needs revision
- **Foreign policy in related pillars** — `policy/foreign-policy.html` is not yet referenced in "Related Policy Areas" sections of other policy area pages
- **Compare page narratives** — strengths/weaknesses sections in compare pages do not yet discuss the foreign policy pillar

## Test suite

- **Unit (Vitest):** `npm run test:unit` — 132 tests, all passing
- **E2E (Playwright/Firefox):** `npm run test:e2e` — 271 tests, all passing
- `POLICY_AREA_COUNT` constant in both test files — update when adding policy areas

## Scaffolding tools

- `scripts/new-policy-area.js` — generate a new policy area HTML page from CLI args
- `scripts/import_policy_catalog.py` — rebuild `policy/catalog/policy_catalog_v2.sqlite` from chat logs
