# Policy ID Schema — Freedom and Dignity Project

**Version:** 2.0 (post full-renumber, April 2026)  
**Status:** Canonical — all 2,862 policy cards tagged  
**Maintainer:** Internal (do not hand-edit `data/policy_catalog.sqlite`)

---

## 1. ID Format

```
SCOPE-FAMILY-NNN
```

| Segment | Length | Description |
|---------|--------|-------------|
| `SCOPE` | 3 chars, uppercase | Pillar scope code (25 canonical values, see §2) |
| `FAMILY` | 2–6 chars, uppercase | Policy family within the pillar (see §3) |
| `NNN` | 3 digits, zero-padded | Sequential number within scope+family prefix |

**Examples:**
- `TEC-PRV-001` — Technology & AI pillar, Privacy family, first position
- `HLT-ACC-012` — Healthcare pillar, Access family, twelfth position
- `JUS-POL-003` — Equal Justice pillar, Policing family, third position
- `TAX-PMT-007` — Taxation & Wealth pillar, Progressive Marginal Tax family, seventh position

---

## 2. Scope Codes (25 canonical)

These are permanent. New pillars require a formal scope code assignment.

| Code | Pillar | HTML File |
|------|--------|-----------|
| `ADM` | Administrative State | `docs/pillars/administrative-state.html` |
| `ANT` | Antitrust & Corporate Power | `docs/pillars/antitrust-and-corporate-power.html` |
| `CHK` | Checks & Balances | `docs/pillars/checks-and-balances.html` |
| `CON` | Consumer Rights | `docs/pillars/consumer-rights.html` |
| `COR` | Anti-Corruption & Government Ethics | `docs/pillars/anti-corruption.html` |
| `EDU` | Education | `docs/pillars/education.html` |
| `ELE` | Elections & Representation | `docs/pillars/elections-and-representation.html` |
| `ENV` | Environment & Agriculture | `docs/pillars/environment-and-agriculture.html` |
| `EXP` | Executive Power | `docs/pillars/executive-power.html` |
| `FPL` | Foreign Policy & International Relations | `docs/pillars/foreign-policy.html` |
| `GUN` | Gun Policy | `docs/pillars/gun-policy.html` |
| `HLT` | Healthcare | `docs/pillars/healthcare.html` |
| `HOU` | Housing | `docs/pillars/housing.html` |
| `IMM` | Immigration | `docs/pillars/immigration.html` |
| `INF` | Infrastructure & Public Goods | `docs/pillars/infrastructure-and-public-goods.html` |
| `JUD` | Courts & Judicial System | `docs/pillars/courts-and-judicial-system.html` |
| `JUS` | Equal Justice & Policing | `docs/pillars/equal-justice-and-policing.html` |
| `LAB` | Labor & Workers' Rights | `docs/pillars/labor-and-workers-rights.html` |
| `LEG` | Legislative Reform | `docs/pillars/legislative-reform.html` |
| `MED` | Information & Media | `docs/pillars/information-and-media.html` |
| `RGT` | Rights & Civil Liberties | `docs/pillars/rights-and-civil-liberties.html` |
| `STS` | Science, Technology & Space | `docs/pillars/science-technology-space.html` |
| `TAX` | Taxation & Wealth | `docs/pillars/taxation-and-wealth.html` |
| `TEC` | Technology & AI | `docs/pillars/technology-and-ai.html` |
| `TRM` | Term Limits & Fitness for Office | `docs/pillars/term-limits-and-fitness.html` |

---

## 3. Legacy / Cross-Scope Codes (DB only — do not use in new IDs)

These codes appear in `data/policy_catalog.sqlite` from earlier drafts of the platform. They are preserved for provenance but all new IDs use canonical scope codes. Positions carrying these codes are migrated to the canonical pillar shown.

| Legacy Code | Meaning | Migrates To |
|-------------|---------|-------------|
| `AGR` | Agriculture | `ENV` (Environment & Agriculture) |
| `CIV` | Civil Rights (legacy) | `RGT` (Rights & Civil Liberties) |
| `ECO` | Economic Policy (legacy) | `TAX`, `LAB`, or `ANT` depending on content |
| `GOV` | Government Structure (legacy) | `CHK` (Checks & Balances) |
| `OVR` | Overarching / International | `FPL` (Foreign Policy) |
| `SYS` | System-Level Rules (legacy) | `CHK` or `EXP` depending on content |

---

## 4. Family Codes

Family codes are derived from the `id` attribute of `div.policy-family` containers in each pillar's HTML file, with the `fam-` prefix stripped.

### Derivation algorithm

```
fam-acc           → ACC            (single segment → use as-is)
fam-hlt-acc       → ACC            (first segment = pillar scope → strip it)
fam-cor-mpy       → MPY            (first segment = known scope but not this pillar → strip old scope)
fam-agr-sub       → AGR-SUB        (first segment = not a known scope → keep full thing)
(no id on div)    → GEN            (orphan cards outside any policy-family)
```

### Family code registry

Family codes are **defined by the HTML**, not centrally registered. Add new families by creating a new `<div class="policy-family" id="fam-XXX">` in the appropriate pillar file.

Family codes should be:
- 2–6 uppercase ASCII letters
- Descriptive abbreviations (e.g., `PRV` = Privacy, `ACC` = Access, `POL` = Policing)
- Unique within a pillar (two families in the same pillar must not share a code)

---

## 5. Numbering Rules

- **Sequential within prefix:** `SCOPE-FAMILY-001`, `002`, `003`, …
- **Zero-padded to 3 digits:** `001`–`999` (no leading zeros beyond padding)
- **Shared counter across duplicate `fam-*` div ids:** if a pillar has two `<div class="policy-family" id="fam-acc">` sections (allowed for organizational grouping), they share a single counter — numbering is continuous, not restarted.
- **Full clean-slate renumber:** when `tag-policy-cards.py` runs, it assigns IDs from `001` across all cards in order of DOM appearance. Existing IDs are replaced.
- **IDs are permanent once status = `INCLUDED`:** do not renumber without updating `record_links`.

---

## 6. Status Values

Stored in `data/policy_catalog.sqlite` → `policy_items.status`.

| Status | Meaning | Rendered as |
|--------|---------|-------------|
| `INCLUDED` | Position is in the HTML with a structured ID | Standard `policy-card` |
| `PROPOSED` | Proposed for inclusion; not yet reviewed | `policy-card proposal` with 🔵 badge |
| `MISSING` | In source logs / DB but not yet in HTML | `policy-card proposal` once added |
| `PARTIAL` | Some sub-points present, others absent | Mixed — parent card included, sub-points as proposals |
| `RETIRED` | Deprecated — do not delete, mark only | Not rendered (or marked `[RETIRED]`) |

---

## 7. HTML Rendering

### 7a. Standard position card

```html
<div class="policy-card" id="SCOPE-FAM-NNN">
  <div class="rule-header">
    <code class="rule-id">SCOPE-FAM-NNN</code>
    <span class="rule-badge">Core</span>
  </div>
  <p class="rule-title">Short title of the position</p>
  <p class="rule-stmt">Full canonical statement of the position.</p>
  <p class="rule-notes">Additional context, cross-references, implementation notes.</p>
</div>
```

### 7b. Proposal card (PROPOSED or MISSING → added to site for review)

```html
<div class="policy-card proposal" id="SCOPE-FAM-NNN">
  <div class="rule-header">
    <code class="rule-id">SCOPE-FAM-NNN</code>
    <span class="rule-badge">Proposal</span>
  </div>
  <div class="rule-status">🔵 Proposal — Under Review</div>
  <p class="rule-title">Short title of the position</p>
  <p class="rule-stmt">Full canonical statement of the position.</p>
  <p class="rule-notes">Rationale, source reference, cross-references.</p>
</div>
```

### 7c. Container structure (for reference)

```html
<section id="pil-policy"> <!-- the policy section of a pillar page -->
  <div class="wrap">
    <div class="policy-family" id="fam-FAMILY-CODE">
      <h3>Family Name</h3>
      <div class="rule-grid">
        <div class="policy-card" id="SCOPE-FAM-001"> … </div>
        <div class="policy-card" id="SCOPE-FAM-002"> … </div>
        <div class="policy-card proposal" id="SCOPE-FAM-003"> … </div>
      </div>
    </div>
  </div>
</section>
```

---

## 8. Database Schema

### Table: `policy_items` (canonical structured-ID table)

| Column | Type | Description |
|--------|------|-------------|
| `rule_id` | TEXT PRIMARY KEY | Structured ID (e.g., `TEC-PRV-001`) |
| `scope_code` | TEXT | 3-letter pillar scope |
| `family_code` | TEXT | Family within scope |
| `canonical_statement` | TEXT | Full policy statement |
| `status` | TEXT | `INCLUDED` / `MISSING` / `PROPOSED` / `PARTIAL` / `RETIRED` |
| `canonical_source_id` | INTEGER | FK → `source_files` |
| `canonical_line_number` | INTEGER | Line in source where first found |
| `occurrence_count` | INTEGER | Times seen in all source logs |
| `source_count` | INTEGER | Number of distinct sources mentioning it |

### Table: `legacy_policy_items` (old numeric checkpoint system)

Pre-ID numeric items from the original policy catalog import. Preserved for provenance. Do not use for new work.

### Table: `record_links`

Maps legacy numeric IDs to structured IDs. Preserves continuity when renumbering occurs.

| Column | Description |
|--------|-------------|
| `legacy_id` | Old numeric or pre-canonical ID |
| `structured_id` | Canonical `SCOPE-FAM-NNN` |
| `link_type` | `exact`, `partial`, `deprecated` |

### Table: `prose_rule_mentions`

IDs that appeared only in prose context in the source logs — not promoted to `policy_items` yet. Used for audit: these may represent future positions, stale references, or optional variants.

### Views

| View | Purpose |
|------|---------|
| `deduped_catalog_entries` | Canonical corpus without legacy numeric duplicates — use for most queries |
| `catalog_entries` | All entries including legacy |
| `unresolved_prose_rule_mentions` | Prose-only IDs not yet in `policy_items` — for gap auditing |

---

## 9. Tooling

| Tool | Purpose |
|------|---------|
| `scripts/tag-policy-cards.py` | Assigns canonical IDs to all `div.policy-card` elements across all 25 pillar HTML files. Run after any HTML structural changes. Supports `--dry-run`. |
| `scripts/import_policy_catalog.py` | Rebuilds `data/policy_catalog.sqlite` from source chat logs. Run after source log changes or after tagging to reconcile statuses. |
| `scripts/new-pillar.js` | Generates a new pillar HTML scaffold with correct structure. Always use this; never copy-paste an existing pillar. |

### Running the tools

```bash
# Dry-run tagging (validate only, no writes):
python3 scripts/tag-policy-cards.py --dry-run

# Full tagging run (assigns IDs to all untagged cards):
python3 scripts/tag-policy-cards.py

# Rebuild catalog DB:
python3 scripts/import_policy_catalog.py

# Create a new pillar:
node scripts/new-pillar.js --id my-pillar --title "My Pillar" \
  --foundation freedom-to-thrive --color "#1a6b8a" --prefix "MPL"
```

---

## 10. Governance

- **IDs are permanent once `INCLUDED`.** Renaming a family code requires updating all affected IDs in HTML and `record_links`.
- **Do not hand-edit `data/policy_catalog.sqlite`.** Use `import_policy_catalog.py` to rebuild from source.
- **Proposals require review** before promotion to `INCLUDED`. The review process is manual: change `class="policy-card proposal"` → `class="policy-card"` and update status in DB.
- **Do not delete deprecated positions.** Set status to `RETIRED` and leave in place for historical provenance.
- **Cross-scope migrations** (legacy → canonical) must be recorded in `record_links` with `link_type = 'deprecated'`.

---

## 11. Coverage Stats (as of April 2026 full renumber)

| Metric | Count |
|--------|-------|
| Total policy cards in HTML | 2,862 |
| Cards with structured IDs | 2,862 (100%) |
| Status: INCLUDED | 293 |
| Status: MISSING (in DB, not yet in HTML) | 1,045 |
| Status: PROPOSED | 203 |
| Status: PARTIAL | 9 |
| Unresolved prose mentions | *see `unresolved_prose_rule_mentions` view* |

**Target:** All MISSING and PROPOSED positions added to the site as proposal cards, reviewed, and promoted to INCLUDED. Any policy position not on the website is a transparency violation.
