# Phase 2 Build Architecture

## Overview

Phase 2 transitions `docs/pillars/*.html` from hand-authored source files to
**generated output**. The canonical source of truth becomes
`data/policy_catalog_v2.sqlite`. Policy positions are authored in the DB and
the site HTML is rendered from it.

The generator for Phase 2 is `scripts/generate-pillar-cards.py`.

---

## Data Model

### Positions table → HTML card mapping

| DB column        | HTML element                                   |
|------------------|------------------------------------------------|
| `id`             | `<div class="policy-card" id="…">` and `<code class="rule-id">` |
| `plain_language` | `<p class="rule-plain">`                        |
| `short_title`    | `<p class="rule-title">`                        |
| `full_statement` | `<p class="rule-stmt">`                         |

Position IDs use the v2 format: `XXXX-XXXX-0000`  
Regex: `^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$`  
Example: `HLTH-COVR-0001`

The first four-character segment is the **domain code**, which maps 1:1 to a
pillar HTML file via `domains.html_file`. The second segment is the
**subdomain code**, which maps to a `<div class="rule-grid">` section within
the pillar page.

### Subdomain → rule-grid mapping

Within each pillar's `<section id="pil-policy">` section, cards are grouped
into `<div class="rule-grid">` containers, each preceded by a
`<div class="family-header">`. The generator identifies which rule-grid
corresponds to which subdomain by examining the IDs of existing v2 cards
within each grid.

When a subdomain has no existing grid in the HTML, the generator creates a new
`family-header` + `rule-grid` pair at the end of `pil-policy`.

### Cross-pillar appearances

Positions that appear in multiple pillars are tracked in
`position_pillar_appearances`. The generator currently processes each pillar
independently by its primary domain. Cross-domain appearances are not yet
rendered by the generator (Phase 2.1 target).

---

## Generation strategy

### Idempotent rendering

The generator is safe to run repeatedly. Before appending a card it checks
whether a `<div class="policy-card">` with that v2 ID already exists anywhere
in the HTML document. If it does, the card is skipped.

Running the generator twice produces identical output.

### Preservation of non-card content

The generator uses BeautifulSoup to parse and modify HTML in-place. It only:

1. Appends new `<div class="policy-card">` elements to existing `rule-grid`
   containers (or newly created ones), inside `<section id="pil-policy">`.
2. When a subdomain has no grid, appends a new `family-header` + `rule-grid`
   block at the end of `pil-policy`.

It never modifies:
- Existing policy cards (any card whose ID is already in the HTML is untouched)
- Prose sections, pull quotes, stat bars, reform grids
- Page headers, navigation, footers, intro sections
- CSS classes, IDs, or attributes on any existing element
- Accent colors (`--accent-color`) or any `<style>` block
- Sections outside `pil-policy` (e.g. `pil-proposals-*`, `pil-intro`)

### Card order within a family

Within each rule-grid, new cards are appended after any cards already in the
grid, ordered by subdomain then `seq` (the integer sequence within the
subdomain, as stored in the `positions` table). This preserves existing card
order and appends new ones in canonical DB order.

---

## The `plain_language` field gap

The `positions` table does not yet have a `plain_language` column. This column
is required by the Phase 2 card template:

```html
<p class="rule-plain">[plain language summary]</p>
```

### Action items

1. **`data/schema_v2.sql`** — Add `plain_language TEXT` to the `positions`
   table definition. Default is `NULL`.
2. **`scripts/build-catalog-v2.py`** — Add `plain_language` to:
   - The `PositionRecord` NamedTuple (as `plain_language: str | None = None`)
   - `parse_html_cards()`: read `<p class="rule-plain">` from each card
   - `populate_db()`: include `plain_language` in `INSERT INTO positions`
3. **`scripts/generate-pillar-cards.py`** — Already handles the missing column
   gracefully via a try/except fallback (falls back to `plain_language=None`
   if the column does not exist).

Until `plain_language` is populated in the DB, generated cards render an empty
`<p class="rule-plain"></p>`. This is valid HTML and signals a data gap that
must be filled before the position is considered content-complete.

A null `plain_language` is a **data gap**, not an acceptable final state for
any CANONICAL position.

---

## Migration path: Phase 1 → Phase 2

### Phase 1 (current)

- Policy cards in `docs/pillars/*.html` are hand-authored.
- The DB has 3,810 CANONICAL positions; HTML cards use v2 IDs.
- A ~91-position DB→HTML gap exists (positions in DB with no HTML card yet).
- `generate-pillar-cards.py --dry-run --all` reports the gap without modifying
  files.

### Transition checklist

1. **Add `plain_language` column** to `schema_v2.sql` and
   `build-catalog-v2.py` (see above).
2. **Rebuild the DB** — run `scripts/build-catalog-v2.py` to incorporate
   `plain_language` values read from HTML.
3. **Run the generator** — `python3 scripts/generate-pillar-cards.py --all`
   to backfill the ~91 missing cards. Verify HTML output in browser and tests.
4. **Freeze hand-editing of policy cards** — After Phase 2 is active, edits
   to policy card content must go through the DB (`positions` table), not the
   HTML. Add a comment to the top of each pillar HTML file:
   ```html
   <!-- GENERATED FILE — do not hand-edit policy-card elements.
        Edit positions in data/policy_catalog_v2.sqlite and re-run
        scripts/generate-pillar-cards.py -->
   ```
5. **CI enforcement** — Add a CI step that runs `generate-pillar-cards.py
   --dry-run --all` and fails if the output is non-zero (i.e., if any DB
   position lacks an HTML card).

### Phase 2 (target)

- `data/policy_catalog_v2.sqlite` is the single source of truth for all
  policy positions.
- `pillars/*/overview.md` and `pillars/*/policy.md` are the source for
  narrative prose.
- `docs/pillars/*.html` is generated output — do not hand-edit policy cards.
- New positions are authored in the DB first, then the site is regenerated
  with `scripts/generate-pillar-cards.py`.

---

## Script reference

| Script                           | Purpose                                      |
|----------------------------------|----------------------------------------------|
| `scripts/build-catalog-v2.py`   | Build/rebuild `policy_catalog_v2.sqlite`     |
| `scripts/generate-pillar-cards.py` | Render DB positions into pillar HTML       |
| `scripts/tag-policy-cards.py`   | Normalize v2 IDs on existing HTML cards      |

### `generate-pillar-cards.py` flags

| Flag              | Description                                          |
|-------------------|------------------------------------------------------|
| `--all`           | Process all 25 pillar HTML files                     |
| `--pillar SLUG`   | Process a single pillar by pillar_id (e.g. `healthcare`) |
| `--dry-run`       | Print what would change; do not write any files      |
