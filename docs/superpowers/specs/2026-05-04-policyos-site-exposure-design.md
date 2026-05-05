# Design Spec: PolicyOS Site Exposure

**Date:** 2026-05-04
**Revised:** 2026-05-05
**Status:** Under review (revised)
**Author:** Sam (GitHub Copilot)

---

## Problem Statement

PolicyOS is the meta-layer governing how all policy on this platform is designed, scoped, and enforced. It has three locked layers (Platform Values, System Principles, Authoring OS) and 11 rule families covering 25 pillars. The site currently exposes only a 3-row summary table on `classification.html` with stale "Under review" status badges. The actual rules, intent, and pillar-specific overlay mappings are not accessible to visitors.

The PolicyOS rules currently live in `.md` files under `policy/policyos/`. The policy catalog DB is the established source of truth for structured content. PolicyOS rules should live there too — and `docs/policyos.html` should be generated from the DB, consistent with how policy cards are generated from the catalog.

---

## Goal

Expose PolicyOS fully on the site:

1. A dedicated `docs/policyos.html` page with the full three-layer rule system, generated from the DB
2. Each pillar page showing the domain-specific PolicyOS overlay families that apply to it
3. `classification.html` updated with correct status and a link to the new page
4. PolicyOS added to "The Platform" nav dropdown
5. Hard-coded policy position counts removed from prose throughout the site

---

## Approach

**DB-sourced generation**

PolicyOS rules are added to `policy_catalog_v2.sqlite` under a new schema. A generation script (`scripts/generate-policyos.py`) reads from the DB and writes `docs/policyos.html` as committed static HTML — consistent with how `scripts/generate-pillar-cards.py` works. The same script also updates the PolicyOS sections of `docs/assets/js/data.js` (family metadata and per-pillar overlay mappings), so all PolicyOS data flows from a single source.

The `.md` source files in `policy/policyos/` are retained as the migration source and for provenance, but are no longer the authoritative source after migration.

---

## Architecture

### New files

- `docs/policyos.html` — generated output; do not hand-edit; re-run `scripts/generate-policyos.py` to update
- `scripts/generate-policyos.py` — reads PolicyOS rules and overlay mappings from the DB; writes `docs/policyos.html` and updates PolicyOS sections in `data.js`

### Modified files

| File | Change |
|------|--------|
| `policy/catalog/policy_catalog_v2.sqlite` | New tables: `policyos_layers`, `policyos_families`, `policyos_rules`, `policyos_pillar_overlays` |
| `docs/assets/js/data.js` | `siteData.policyosFamilies` and per-pillar `policyosOverlays` fields added/updated by generation script |
| `docs/assets/js/app.js` | Inject PolicyOS nav link under "The Platform" dropdown; inject `#pil-policyos` section into pillar pages |
| `docs/classification.html` | Update two "Under review" badges to "Locked"; remove stale "not yet canonicalized" prose; add link to `policyos.html` |
| `docs/pillars/*.html` | No manual edits — overlay section is injected by `app.js` at runtime |
| `tests/unit/data.test.js` | Tests for new overlay data structure in `siteData` |
| `tests/e2e/site.spec.js` | Tests for `policyos.html`, nav link, per-pillar injection, classification.html badges |
| Various `docs/*.html` | Remove hard-coded aggregate policy position counts from prose |
| `README.md` | Add `migrate-policyos-to-db.py` and `generate-policyos.py` to Scripts section; document execution order |
| `scripts/requirements.txt` | Create file (if absent); add `markdown2` dependency |

### Data flow

```
policy_catalog_v2.sqlite
  (policyos_layers, policyos_families, policyos_rules, policyos_pillar_overlays)
  → scripts/generate-policyos.py
    → docs/policyos.html          (committed static HTML)
    → data.js policyosFamilies    (11 family metadata objects)
    → data.js pillar[].policyosOverlays  (per-pillar overlay mappings)
      → app.js (reads pillar slug, injects #pil-policyos section at runtime)
        → pillar pages (shows applicable families, links to policyos.html#anchor)
```

---

## DB Schema

Four new tables in `policy_catalog_v2.sqlite`:

### `policyos_layers`

```sql
CREATE TABLE policyos_layers (
    id          TEXT PRIMARY KEY,   -- 'values', 'principles', 'authoring'
    title       TEXT NOT NULL,      -- 'Platform Values', 'System Principles', 'Authoring OS'
    description TEXT,
    sort_order  INTEGER NOT NULL
);
```

### `policyos_families`

```sql
CREATE TABLE policyos_families (
    code        TEXT PRIMARY KEY,   -- 'KERN', 'GEOG', 'NORM', etc.
    layer_id    TEXT NOT NULL REFERENCES policyos_layers(id),
    label       TEXT NOT NULL,      -- 'Core Kernel', 'Geography & Access', etc.
    anchor      TEXT NOT NULL,      -- page anchor on policyos.html, e.g., 'kern'
    summary     TEXT NOT NULL,      -- one-sentence description for UI use
    sort_order  INTEGER NOT NULL
);
```

### `policyos_rules`

```sql
CREATE TABLE policyos_rules (
    id           TEXT PRIMARY KEY,  -- 'PLOS-KERN-0001', 'PAOS-NORM-0001', etc.
    layer_id     TEXT REFERENCES policyos_layers(id),         -- set for Platform Values rows; NULL otherwise
    family_code  TEXT REFERENCES policyos_families(code),     -- NULL for Platform Values rows
    value_name   TEXT,              -- e.g., 'Human Dignity'; set for Platform Values rows; NULL otherwise
    rule_text    TEXT NOT NULL,
    rule_subtype TEXT,              -- 'floor' or 'duty' for Platform Values rows; NULL otherwise
    sort_order   INTEGER NOT NULL,
    CHECK (layer_id IS NOT NULL OR family_code IS NOT NULL)   -- every row must belong to a layer or a family
);
```

- **System Principles and Authoring OS rules:** `layer_id = NULL`, `family_code` set, `value_name = NULL`, `rule_subtype = NULL`.
- **Platform Values rules:** `layer_id = 'values'`, `family_code = NULL`, `value_name` set to the named value (e.g., `'Human Dignity'`), `rule_subtype` set to `'floor'` or `'duty'`.

`value_name` groups floor/duty pairs under their named value so the generation script can produce correctly headed sections.

### `policyos_pillar_overlays`

```sql
CREATE TABLE policyos_pillar_overlays (
    pillar_id      TEXT NOT NULL,   -- matches siteData.pillars[].id, e.g., 'healthcare'
    family_code    TEXT NOT NULL REFERENCES policyos_families(code),
    overlay_type   TEXT NOT NULL CHECK (overlay_type IN ('mandatory', 'conditional')),
    notes          TEXT,
    PRIMARY KEY (pillar_id, family_code)
);
```

Only System Principles family codes (KERN, GEOG, FEDR, REGD, ENFA, AIGV, ECOL, THRV, DEMO, PRIV, ECON) are valid in this table. Authoring OS codes must not appear — `app.js` looks up overlay families in `siteData.policyosFamilies` which contains System Principles only. SQLite does not support subquery-based CHECK constraints, so this restriction is enforced in the migration script: before inserting each row, the script validates `family_code` against the set of codes in `policyos_families WHERE layer_id = 'principles'` and raises an error if a non-matching code is found.

---

## DB Migration

Source data:
- Rules and family content: `policy/policyos/policyos_1_0_rules_proposal.md`, `policy/policyos/policyos_authoring_os_v1.md`, `policy/policyos/policyos_platform_values_v1.md`
- Pillar overlay mappings: `policy/policyos/policyos_1_0_inheritance_matrix.csv` (pipe-delimited `mandatory_families` and `conditional_families` columns; split on `|` to get arrays)

A migration script (`scripts/migrate-policyos-to-db.py`) parses the source files and populates the four new tables. The migration is idempotent — it uses `INSERT OR REPLACE` so it can be re-run safely if source content changes before the `.md` files are fully retired.

**Platform Values migration:** Each Platform Values statement is stored with `family_code = NULL` and `layer_id = 'values'`. The `rule_subtype` column distinguishes `'floor'` statements (negative prohibitions) from `'duty'` statements (positive obligations). The migration script parses the floor/duty structure from the markdown — each value section has clearly labeled floor and duty statements.

**Sentinel initialization:** As part of migration, the script also inserts the two sentinel comment blocks into `data.js` if they are not already present. They are appended immediately after the `window.siteData = siteData;` line at the end of the file. The sentinels must exist before `generate-policyos.py` can run.

```js
/* POLICYOS-FAMILIES-START */
/* POLICYOS-FAMILIES-END */

/* POLICYOS-OVERLAYS-START */
/* POLICYOS-OVERLAYS-END */
```

After migration is verified, the `.md` files are retained for provenance but marked in their headers as superseded by the DB.

---

## `scripts/generate-policyos.py`

Reads from the DB and produces two outputs:

**1. `docs/policyos.html`**

The page uses the same HTML shell as `approach.html` and `platform.html` (doctype, `<html lang="en">`, shared CSS/JS, injected nav and footer). Sections:

1. **Hero** — "PolicyOS: The Rules Behind the Rules" — one-paragraph intro
2. **How it fits** — relationship between PolicyOS and the five foundations; why a meta-layer exists
3. **Layer 1: Platform Values** — intro to the floor/duty model; each value with its floor prohibition and positive duty statement
4. **Layer 2: System Principles** — intro on the overlay inheritance model; each of the 11 families as its own subsection with label, summary, applicability note, and all rules listed with IDs
5. **Layer 3: Authoring OS** — same treatment for NORM, AUTH, TEST, ENFC, PLAC, MAINT
6. **Governance** — the amendment process from `policyos_governance_v1.md` (governance rules are not in the DB; this section is generated by reading `policyos_governance_v1.md` at script run time)
7. **Pillar compliance** — brief note that all pillars must satisfy applicable families; link to `classification.html`

Each family section has a stable lowercase anchor derived from `policyos_families.anchor`: `#kern`, `#geog`, `#fedr`, etc.

**2. PolicyOS sections of `docs/assets/js/data.js`**

The script locates two delimited regions in `data.js` using sentinel comments (initialized by `migrate-policyos-to-db.py`). If either sentinel block is absent, the script exits non-zero and writes nothing.

```js
/* POLICYOS-FAMILIES-START */
siteData.policyosFamilies = { ... };
/* POLICYOS-FAMILIES-END */
```

```js
/* POLICYOS-OVERLAYS-START */
// per-pillar policyosOverlays populated below
/* POLICYOS-OVERLAYS-END */
```

On each run, the script replaces the content between the sentinels with freshly generated data from the DB. This allows the rest of `data.js` to be maintained by hand while keeping PolicyOS data DB-authoritative.

**`siteData.policyosFamilies` filter:** The script populates this object from `policyos_families WHERE layer_id = 'principles'` only (the 11 System Principles families). Authoring OS families are rendered on `policyos.html` but are not needed in the runtime JS — they are not used by `app.js` for pillar injection.

**`siteData.policyosFamilies` format:**

```js
siteData.policyosFamilies = {
  'KERN': { label: 'Core Kernel', anchor: 'kern', summary: '...' },
  'GEOG': { label: 'Geography & Access', anchor: 'geog', summary: '...' },
  // ... 9 more entries
};
```

**Per-pillar overlay format:** The inheritance matrix CSV covers all 25 pillars. After migration, all 25 pillars will have rows in `policyos_pillar_overlays`. The script determines the list of pillar IDs from the distinct `pillar_id` values in `policyos_pillar_overlays` — not by parsing `data.js`. For each pillar ID, the script emits an overlay IIFE. If a pillar in the DB has no overlay rows (only possible if migration is incomplete), the script emits a KERN-only fallback:

```js
(function() {
  const p = siteData.pillars.find(x => x.id === 'healthcare');
  if (p) p.policyosOverlays = { mandatory: ['KERN'], conditional: ['GEOG', 'REGD', 'ENFA'] };
})();
```

One IIFE per pillar, emitted inside the POLICYOS-OVERLAYS sentinel block. Using `find` keeps this independent of array index and safe across future pillar reorderings.

**Governance section:** The Governance section of `policyos.html` reads from `policyos_governance_v1.md` at generation time. If the file is absent, the script exits non-zero and writes no output. The script converts the markdown to HTML using the `markdown2` Python library, then post-processes the output with a regex pass to shift heading levels by +2 (`<h1>` → `<h3>`, `<h2>` → `<h4>`) so that governance headings stay below the `<h2>`-level section headings used elsewhere on the page. Add `markdown2` to `scripts/requirements.txt` (create the file if it does not exist). This is the only markdown-to-HTML conversion in the script; all other content comes from the DB as plain text and is HTML-escaped before insertion.

**Script execution order:**

```
1. python3 scripts/migrate-policyos-to-db.py    # populates DB tables + inserts data.js sentinels
2. python3 scripts/generate-policyos.py          # reads DB, writes policyos.html, updates data.js
```

This order is enforced by `generate-policyos.py` failing fast (non-zero exit, no output written) if the sentinels are absent. The error message names `migrate-policyos-to-db.py` as the prerequisite. This execution order must also be documented in `README.md` under the Scripts section.

The migration script must enable FK enforcement with `PRAGMA foreign_keys = ON` at connection time so that invalid `layer_id` values in `policyos_families` and other FK relationships are caught at insert time rather than silently accepted.

---

## `app.js` Injection

### Nav injection

Add "PolicyOS" as the fourth item in the "The Platform" dropdown (after "Rights", "Policy Library", "Platform Overview"). Follows the same path-resolution pattern used for existing injected links.

### Per-pillar section injection

On pillar pages (detected by the presence of `#pil-snav` in the DOM):

**Injection position:** `#pil-policyos` is appended after `#pil-related` (the final section on all pillar pages), making it the last section. A "PolicyOS" nav item is also injected into `#pil-snav` as the final list item.

**Empty conditional overlay case:** If `policyosOverlays.conditional` is empty, the section still renders with only the KERN baseline note — it is never suppressed.

1. Derive the pillar slug from `location.pathname`: take the filename without extension, replace hyphens with underscores (e.g., `executive-power` → `executive_power`). This matches `siteData.pillars[].id`.
2. Find the current pillar in `siteData.pillars` by matching the normalized slug against `pillar.id`.
3. Read `pillar.policyosOverlays`.
4. Inject `<section id="pil-policyos">` into the page.

**Rendered section structure:**

- Heading: "PolicyOS Overlays"
- Note: "KERN applies to all pillars. [View KERN rules →](policyos.html#kern)"
- If `policyosOverlays.mandatory` contains any families beyond KERN, render those as mandatory cards before the conditional list.
- List of conditional families: each as a card showing family code, label, summary, and a "View rules →" link to `base + 'policyos.html#' + anchor`

**Path resolution:** Links use the `base` variable already established in `app.js`, resolving correctly from both root pages and `docs/pillars/` subdirectory.

**Error handling:** Two guards apply:
- If the pillar slug has no matching entry in `siteData.pillars`, injection is silently skipped.
- If the slug IS found but `pillar.policyosOverlays` is `undefined` (generate script not yet run), injection is silently skipped — no broken page, no console error.

---

## `classification.html` Changes

1. Update the two "Under review" status badges (Layer 2: System Principles; Layer 3: Authoring OS) to "Locked". Layer 1 is already "Locked".
2. Remove the full paragraph containing that stale sentence — both sentences: "PolicyOS rules will not be canonicalized into the main platform until the structural review is complete. For the current status and working files, see the `policyos/` directory in the project repository."
3. Add after the summary table: `For the full PolicyOS documentation, including all rule families and individual rules, see <a href="policyos.html">PolicyOS</a>.`

---

## Hard-Coded Count Removal

Scan `docs/*.html` and `docs/pillars/*.html` for aggregate policy position counts in prose. `docs/compare/*.html` is excluded.

**Scope:** The following files contain aggregate counts to remove: `equal-justice-and-policing.html`, `technology-and-ai.html`, `foreign-policy.html`, `science-technology-space.html`, `about-ai.html`. The developer should verify this list with a scan (`grep -r "positions" docs/*.html docs/pillars/*.html`) and treat the list as a reference, not a guaranteed-complete inventory.

- Where the count was the substance: remove the sentence or replace with "the full policy catalog"
- Where the count was incidental: drop the number

Dynamic `[data-dynamic]` spans are unaffected.

---

## Testing

### Unit tests (`data.test.js`)

- All 25 pillar entries have `policyosOverlays` with at least `mandatory: ['KERN']`
- `siteData.policyosFamilies` has exactly 11 keys
- Each family object has `label`, `anchor`, and `summary`

### E2E tests (`site.spec.js`)

- `policyos.html` loads; has correct title; nav and footer visible
- All 11 System Principles family anchors exist on `policyos.html`
- All 6 Authoring OS family anchors exist on `policyos.html`
- A sample pillar page (e.g., `healthcare.html`) has `#pil-policyos` section injected after load, and it appears after `#pil-related` in document order (assert `#pil-related` precedes `#pil-policyos` in the DOM)
- The same sample pillar page has a "PolicyOS" item in `#pil-snav` after load, and it is the last list item
- PolicyOS nav link appears in "The Platform" dropdown
- `classification.html` status badges read "Locked", not "Under review"

---

## Out of Scope

- Making PolicyOS rules editable through the site
- Linking individual policy positions to the specific PLOS/PAOS rules that shaped them
- Pillar compliance audit or scoring
- Migrating Platform Values governance prose to the DB (governance section of `policyos.html` reads from `policyos_governance_v1.md` directly, or is templated inline)

