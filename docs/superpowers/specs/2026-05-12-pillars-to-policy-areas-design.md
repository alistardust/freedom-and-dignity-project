# Design: Rename "Pillars" to "Policy Areas" — Full Codebase Migration

**Date:** 2026-05-12
**Status:** Approved for implementation

---

## Overview

The concept of a "pillar" is retired. Individual policy sections are now "policy areas" — unremarkable parts of each foundation, not a special structural concept. This migration removes the word "pillar" and all related identifiers from every layer of the codebase: URLs, file paths, CSS classes, JavaScript identifiers, prose content, navigation labels, test files, and generator scripts.

The migration is implemented via a single Node.js script (`scripts/migrate-pillars-to-policy.js`) that handles all mechanical changes in one pass, followed by a verify pass that flags any remaining occurrences for manual review. All changes land in one feature branch as one PR.

---

## Goals

- Remove "pillar/pillars" from all user-visible content (prose, headings, labels, nav, meta)
- Remove "pillar/pillars" from all code identifiers (CSS classes, JS variables, HTML IDs, test constants)
- Rename URL paths from `/pillars/` to `/policy/`
- Rename source templates from `src/pages/pillars/` to `src/pages/policy/`
- Rename `siteData.pillars` to `siteData.policyAreas` throughout
- Remove the `completion-status` development status block from all policy area pages
- Remove all pillar count badges and `data-dynamic="pillar-count"` spans
- Update all tests to use the new paths, class names, and data property names
- Leave old `/pillars/` URLs as broken links (site is early-stage; no redirect stubs needed)

---

## Out of scope

- Policy position IDs (`HLTH-COVR-0001` etc.) — do not contain "pillar"
- SQLite database schema column names — separate migration concern
- Git history
- GitHub Issues and PR text

---

## 1. File structure changes

### Moves
| From | To |
|---|---|
| `docs/pillars/*.html` (27 files) | `docs/policy/*.html` |
| `src/pages/pillars/*.njk` (27 files) | `src/pages/policy/*.njk` |

The script uses `fs.renameSync` / `fs.mkdirSync` to move all files. The old directories are removed after all files are moved.

### Generator scripts
| Old | New |
|---|---|
| `scripts/new-pillar.js` | `scripts/new-policy-area.js` |

`new-compare.js` is updated in-place (nav link templates and HTML comments reference "pillars").

---

## 2. URL and path replacements

Applied across all HTML, njk, JS, and test files:

| Old pattern | New pattern |
|---|---|
| `/pillars/` (in href, src, goto, page.goto) | `/policy/` |
| `pillars/` (relative paths in build.test.js examples) | `policy/` |
| `/(pillars\|compare)/` (app.js path detection regex) | `/(policy\|compare)/` |

---

## 3. CSS class renames

Applied in `docs/assets/css/style.css`, all HTML files, all njk files, and `app.js`. Replacements are applied longest-match-first to avoid partial collisions.

### .pil-* prefix renames
| Old class | New class |
|---|---|
| `.pil-pillar-card` | `.area-card` |
| `.pil-pillar-title` | `.area-card-title` |
| `.pil-pillar-desc` | `.area-card-desc` |
| `.pil-pillar-link` | `.area-link` |
| `.pil-pillar-grid` | `.area-grid` |
| `.pil-pillar-count` | *(removed — see Section 6)* |
| `.pil-foundation-accordion` | `.area-foundation-accordion` |
| `.pil-foundation-bar-left` | `.area-foundation-bar-left` |
| `.pil-foundation-bar-right` | `.area-foundation-bar-right` |
| `.pil-foundation-bar-text` | `.area-foundation-bar-text` |
| `.pil-foundation-bar` | `.area-foundation-bar` |
| `.pil-foundation-name` | `.area-foundation-name` |
| `.pil-foundation-num` | `.area-foundation-num` |
| `.pil-foundation-teaser` | `.area-foundation-teaser` |
| `.pil-fv-pill` | `.area-fv-pill` |
| `.pil-grid-closing` | `.area-grid-closing` |
| `.pil-idx-wrap` | `.area-idx-wrap` |
| `.pil-chevron` | `.area-chevron` |
| `.pil-hero` | `.area-hero` |
| `.pil-intro` | `.area-intro` |
| `.pil-summary` | `.area-summary` |
| `.pil-snav` | `.area-snav` |
| `.pil-title` | `.area-title` |

### Other pillar-named classes
| Old class | New class |
|---|---|
| `.pillar-filter-btn` | `.policy-area-filter-btn` |
| `.pillar-filters` | `.policy-area-filters` |
| `.pillar-grid` | `.policy-area-grid` |
| `.pillar-card` | `.policy-area-card` |
| `.f-pillar-grid` | `.f-area-grid` |
| `.f-pillar-card` | `.f-area-card` |
| `.mission-pillars-grid` | `.mission-areas-grid` |
| `.cmp-th-pillar` | `.cmp-th-area` |
| `.cmp-td-pillar` | `.cmp-td-area` |
| `.fd-pillars` | `.fd-policy-areas` |
| `.fd-pillar-tag` | `.fd-policy-area-tag` |

**Note:** `.policy-card` already exists as the class for policy rule/position cards. `.policy-area-card` is used for area index cards to avoid collision.

---

## 4. JavaScript identifier renames

Applied in `docs/assets/js/data.js` and `docs/assets/js/app.js`:

| Old identifier | New identifier | File |
|---|---|---|
| `siteData.pillars` (array) | `siteData.policyAreas` | data.js |
| `foundation.pillars: [...]` | `foundation.policyAreas: [...]` | data.js (all 5 foundations) |
| `siteData.getPillarsByFoundation` | `siteData.getPolicyAreasByFoundation` | data.js |
| `siteData.pillars` (consumers) | `siteData.policyAreas` | app.js |
| `pillarCount` variable | `policyAreaCount` | app.js |
| `case 'pillar-count':` | *(removed — see Section 6)* | app.js |
| `pillarGrid` / `#pillar-grid` | `policyAreaGrid` / `#policy-area-grid` | app.js + HTML |
| `pillarFilters` / `#pillar-filters` | `policyAreaFilters` / `#policy-area-filters` | app.js + HTML |
| `.pillar-filter-btn` (in JS querySelector) | `.policy-area-filter-btn` | app.js |
| `.pillar-card` (in JS-generated HTML) | `.policy-area-card` | app.js |
| `pillarOverlays` | `policyAreaOverlays` | app.js |
| `"apply to this pillar"` (string literal) | `"apply to this policy area"` | app.js |
| `/(pillars\|compare)/` (regex) | `/(policy\|compare)/` | app.js |

---

## 5. Content and prose replacements

Applied in all HTML and njk files. Case-sensitive variants handled explicitly:

| Old text | New text |
|---|---|
| `Policy Pillar` | `Policy Area` |
| `Policy Pillars` | `Policy Areas` |
| `policy pillar` | `policy area` |
| `policy pillars` | `policy areas` |
| `Pillar` (standalone title case) | `Policy Area` |
| `Pillars` (standalone title case) | `Policy Areas` |
| `pillar` (standalone lowercase) | `policy area` |
| `pillars` (standalone lowercase) | `policy areas` |
| Navigation labels referencing "Pillars" | "Policy Areas" |

The script applies word-boundary replacements (`\bpillar\b`, `\bpillars\b`) to avoid corrupting identifiers in mid-replacement. After all replacements, a verify pass scans for any remaining "pillar" occurrences across all source files and prints them for manual review.

---

## 6. Elements removed entirely

These are deleted, not renamed:

- `<div class="completion-status">...</div>` — development status block with progress bar, present on all 26 area pages and their njk counterparts. Removed entirely. The div is uniquely named and self-contained; regex removal is safe.
- `<span class="pil-pillar-count">N pillars</span>` — per-foundation count badges on the index page (5 instances in HTML + njk). Removed entirely.
- `<span data-dynamic="pillar-count">25</span> pillars` — in `policy-library.html` and `policy-library.njk`. The surrounding sentence is reworded to remove the count.
- `case 'pillar-count':` branch in app.js dynamic counts block — no remaining consumers.
- Prose sentences referencing "25 pillars" or "N pillars" in meta descriptions and body text — reworded to describe content without counting policy areas.

---

## 7. Test updates

### tests/e2e/shared.js
- `SAMPLE_PILLARS` → `SAMPLE_POLICY_AREAS`
- Comment updated: "slug matches the filename at `docs/policy/<slug>.html`"

### tests/e2e/site.spec.js
- `const { SAMPLE_PILLARS }` → `const { SAMPLE_POLICY_AREAS }`
- `PILLAR_COUNT` constant removed; tests that asserted exact link counts are replaced with dynamic assertions using `siteData.policyAreas.length` (imported from data.js) or, where appropriate, removed if they were testing the count concept rather than behavior
- All `/pillars/` paths → `/policy/`
- All `.pil-pillar-link`, `.pil-pillar-card`, `.f-pillar-card` selectors updated to new class names
- Test descriptions updated: "pillar page" → "policy area page", "Pillars index" → "Policy areas index", etc.
- Line 85 comment updated: the existing assertion that nav does NOT contain "pillars" becomes a clean correctness check; the caveat comment is removed
- "pillar PolicyOS overlay" describe block renamed to "policy area PolicyOS overlay"

### tests/e2e/mobile.spec.js
- All `/pillars/` paths → `/policy/`
- `SAMPLE_PILLARS` → `SAMPLE_POLICY_AREAS`
- `SPOT_PILLARS` → `SPOT_AREAS`
- Test descriptions updated: "pillar page" → "policy area page", "pillar sub-nav" → "area sub-nav"
- Path detection comment updated: `/(pillars|compare)/` → `/(policy|compare)/`

### tests/unit/data.test.js
- `siteData.pillars` → `siteData.policyAreas` throughout
- `f.pillars` → `f.policyAreas`
- `PILLAR_COUNT` → `POLICY_AREA_COUNT` (derived dynamically: `siteData.policyAreas.length`)
- `siteData.getPillarsByFoundation` → `siteData.getPolicyAreasByFoundation`
- All describe/test descriptions: "pillar" → "policy area"
- `policyosOverlays` test: "has exactly 25 pillar entries" → "has one entry per policy area"

### tests/unit/build.test.js
- Example paths: `docs/pillars/healthcare.html` → `docs/policy/healthcare.html`
- `pillars/healthcare.html` → `policy/healthcare.html`

---

## 8. Migration script design

**File:** `scripts/migrate-pillars-to-policy.js`

**Usage:**
```bash
node scripts/migrate-pillars-to-policy.js          # dry run (prints changes, no writes)
node scripts/migrate-pillars-to-policy.js --apply  # apply all changes
node scripts/migrate-pillars-to-policy.js --verify # scan for remaining "pillar" occurrences
```

**Phases (in order):**

1. **Move files** — `docs/pillars/` → `docs/policy/`, `src/pages/pillars/` → `src/pages/policy/`
2. **URL/path replacements** — `/pillars/` → `/policy/` across all source files
3. **CSS class renames** — longest-match-first to prevent partial collisions (e.g., `.pil-pillar-card` before `.pil-pillar`, `.pil-pillar-grid` before `.pil-pillar`)
4. **JS identifier renames** — `siteData.pillars`, `pillarCount`, `pillarGrid`, etc.
5. **Content/prose replacements** — word-boundary aware, case variants handled explicitly
6. **Element removals** — `completion-status` divs, count spans, dead `case 'pillar-count':` branch
7. **Verify pass** — scan all source files for remaining "pillar" occurrences, print report

**Scope of files processed:** `docs/**/*.html`, `src/pages/**/*.njk`, `docs/assets/js/*.js`, `docs/assets/css/style.css`, `tests/**/*.js`, `scripts/*.js`

**Exclusions:** `node_modules/`, `.git/`, `*.png`, `*.sqlite`, `policy/catalog/`, `policy/policyos/`, `policy/foundations/` (markdown content), `docs/superpowers/` (spec/plan docs)

After the script runs, the implementer commits with `refactor(site): rename pillars to policy areas`.

---

## 9. Visual regression baselines

After the rename, visual regression baselines in `tests/visual/visual.spec.js-snapshots/` will need refreshing because:
- Class names on the policy areas index page changed
- The `completion-status` block is removed from all area pages

Run `npx playwright test --project=visual-firefox --update-snapshots` after verifying the site renders correctly.

---

## 10. Verification checklist

Before merging:

- [ ] `npm run test:unit` passes
- [ ] `npm run test:e2e` passes across all browser projects
- [ ] `node scripts/migrate-pillars-to-policy.js --verify` reports zero remaining "pillar" occurrences in source files
- [ ] `/policy/healthcare.html` loads correctly in browser
- [ ] `/policy/index.html` loads correctly in browser
- [ ] Nav links point to `/policy/` paths
- [ ] Foundation page pillar cards (on platform page) link to `/policy/` paths
- [ ] PolicyOS overlay still appears on policy area pages
- [ ] `completion-status` block is absent from all policy area pages
- [ ] No "pillar" text visible anywhere on the live site
