# Policy Card Completion Design

**Issue:** #7
**Date:** 2026-05-10
**Status:** Approved

## Problem

1,121 policy cards across 26 pillars are at `class="policy-card proposal"` status. These cards have substantive content (`rule-title`, `rule-plain`, `rule-body` with citations) but are in a different structural format from the canonical card format, have not been through adversarial review, and are not represented completely in the policy catalog database.

Additionally, the site currently uses status classes (`status-included`, `proposal`) and badge labels (`Included`, `Proposal`) on all cards. The status system is being redesigned as part of the human review workflow effort. This work strips all status markers site-wide and standardizes card structure before the new system is designed.

---

## Goals

1. Standardize all policy cards to a single format with no status markers
2. Convert all 1,121 proposal cards to the canonical card format with adversarial review
3. Add a `rule_notes` column to the database and keep it in sync with HTML

---

## Card Format

All cards after this work use a single unified format:

```html
<div class="policy-card" id="XXXX-YYYY-0000">
  <div class="rule-header">
    <code class="rule-id">XXXX-YYYY-0000</code>
  </div>
  <p class="rule-title">Specific, descriptive title in plain language</p>
  <p class="rule-plain">1-3 sentences, ~8th grade. What does this do and why does it matter?</p>
  <p class="rule-stmt">Formal policy statement with precise language, thresholds, and enforcement detail.</p>
  <p class="rule-notes">Research-backed rationale: legal basis (statutes, case law), empirical evidence,
  enforcement mechanisms, implementation notes, and adversarial review findings
  (gaps addressed, loopholes closed, failure modes considered).</p>
</div>
```

No `class="status-included"`, no `class="proposal"`, no `rule-badge` span, no `rule-status` div.

### Field mapping (HTML to DB)

| HTML class | DB column | Notes |
|---|---|---|
| `rule-title` | `short_title` | |
| `rule-plain` | `plain_language` | |
| `rule-stmt` | `full_statement` | |
| `rule-notes` | `rule_notes` (new column) | |
| `rule-body` | (none) | Removed in Phase 4 during conversion |
| `rule-citations` | (none) | Removed in Phase 4; content folded into `rule-notes` |

---

## Adversarial Review Requirement (PAOS-TEST-0008)

Every proposal card conversion must include in `rule-notes`:

- **Gap:** what the rule fails to cover or whom it fails to protect
- **Loophole:** how a bad-faith actor could technically comply while defeating the rule's purpose
- **Unintended consequence:** perverse incentives, burden-shifting, or foreseeable second-order harms
- **Abuse path:** how government, institutions, or employers could exploit the rule

If no issues found in any category, document that the review was conducted and explain why.

---

## Phases

### Phase 1: DB schema migration

Add `rule_notes` column to the `positions` table:

```sql
ALTER TABLE positions ADD COLUMN rule_notes TEXT;
```

File: `policy/catalog/policy_catalog_v2.sqlite`

Commit: `chore(db): add rule_notes column to positions table`

### Phase 2: Mechanical HTML cleanup (script)

New script: `scripts/strip-card-status.js` (Node.js, to be created in Phase 2).

Processes every `docs/pillars/*.html` file and:

- Removes the status class modifier from all cards: `class="policy-card status-included"` and `class="policy-card proposal"` and all other `status-*` variants become `class="policy-card"`
- Removes all `<span class="rule-badge">...</span>` elements
- Removes all `<div class="rule-status">...</div>` elements (present on proposal cards only)
- Leaves `rule-body` and `rule-citations` on proposal cards intact (handled in Phase 4)

CSS changes in `docs/assets/css/style.css`:

- Remove `.policy-card.status-included` border rule
- Remove `.policy-card.proposal` border rule
- Remove `.status-included .rule-badge` rule
- Remove `.proposal .rule-badge` rule
- Remove all other `.rule-badge` rules

After Phase 2, proposal cards are in a valid intermediate state: `class="policy-card"` with `rule-body` and `rule-citations` instead of `rule-stmt` and `rule-notes`. This is expected and temporary.

The script must be idempotent: running it twice on the same file must produce the same result. This ensures safe re-runs if interrupted mid-pillar.

Tests must pass after Phase 2. Commit: `refactor(cards): strip status classes and badges from all policy cards`

### Phase 3: Backfill existing rule_notes to DB

New script: `scripts/backfill-rule-notes.js` (Node.js, to be created in Phase 3).

Reads every card from all 26 pillar HTML files, finds cards with a `rule-notes` paragraph, matches on the `id` attribute of the `<div class="policy-card">` element (e.g. `id="HLTH-ACCS-0001"`), and writes the `rule-notes` text content to the new `rule_notes` DB column.

Miss-handling policy: if a card ID found in HTML has no matching row in the DB, log a warning to stdout and continue. After the run, print a summary of all unmatched IDs for review. Do not fail the script on a miss. Unmatched IDs should be investigated manually and backfilled into the DB separately.

The script must be idempotent. Phase 3 modifies only the database, not HTML -- no test run is required after it. Backfills only `status-included` cards (those with `rule-notes` already present in HTML); proposal cards (`rule-body`/`rule-citations`) are out of scope here and handled in Phase 4.

Before Phase 4 begins, review the unmatched ID summary printed by this script. Any unmatched IDs should be investigated and backfilled into the DB manually before Phase 4 starts (or tracked as known gaps).

Commit: `chore(db): backfill rule_notes from existing status-included cards (status-included only; proposal cards deferred to Phase 4)`

### Phase 4: Per-pillar proposal card content conversion

Phase 4 uses one subagent per pillar. **Subagents run serially, one at a time, in the priority order in the table below.** Parallel execution is not permitted: SQLite does not support concurrent writers, and parallel DB commits on the same branch produce unresolvable merge conflicts.

Each subagent works sequentially through all families in its assigned pillar. Within each family, the subagent:

1. Reads all cards with `rule-body` (the unconverted proposal cards). Policy families are groupings of related cards within a pillar, each contained in a `<div class="policy-family">` element with a `family-header`. Work proceeds family by family within each pillar.
2. For each card in the family:
   - Extracts a `rule-stmt` (formal, precise policy statement with thresholds and enforcement detail) from `rule-body`
   - Converts `rule-body` + `rule-citations` into `rule-notes` prose with inline citations and adversarial review
   - Removes `rule-body` and `rule-citations` from the HTML
3. Updates the DB for all cards in the family in a single transaction:
   - `rule_notes` is set from the new `rule-notes` content
   - `full_statement` is set from the new `rule-stmt` content
   - `short_title` and `plain_language` are confirmed to be populated; if missing, backfill from the card's existing HTML `rule-title` and `rule-plain` fields respectively

   If the transaction fails, roll back the entire family and surface the error -- do not partially commit DB updates.
4. Writes the converted HTML for all cards in the family. HTML is written **after** a successful DB commit. If HTML writing fails after DB commit, log the error and surface it for manual recovery (the DB is already correct; re-running Phase 4 on that family will re-derive the HTML and skip cards that already have `rule-stmt`).
5. Runs `npm run test:unit`. If tests pass, commits that family: `policy(<pillar>): complete <FAMILY> cards`. If tests fail, stop immediately and surface the failure with the test output. Do not commit, do not proceed to the next family, and do not attempt to auto-fix. Leave the DB changes and HTML writes in place -- they are safe to leave uncommitted because Phase 4 is idempotent (cards with `rule-stmt` are skipped on re-run). Fix the test failure manually and re-run the family from step 5.
6. Moves to the next family and repeats.

Phase 4 is idempotent per family: remaining work is detected by the presence of `rule-body` on a card. Cards that already have `rule-stmt` are skipped.

Research must use primary sources (federal statutes, court opinions, government data) and academic databases (Google Scholar, SSRN, NBER, PubMed where applicable). All citations go inline in `rule-notes` prose.

---

## Pillar Priority Order (Phase 4)

26 pillars total; 25 require Phase 4 content work. `data-rights-and-privacy` requires Phase 2 mechanical cleanup only (its 34 cards already have `rule-stmt` and `rule-notes`). Total proposal cards requiring Phase 4 conversion: 1,121.

| Priority | Pillar | Proposal cards |
|---|---|---|
| P1 | equal-justice-and-policing | 98 |
| P1 | consumer-rights | 91 |
| P1 | environment-and-agriculture | 82 |
| P1 | antitrust-and-corporate-power | 79 |
| P1 | healthcare | 79 |
| P1 | education | 67 |
| P1 | labor-and-workers-rights | 61 |
| P1 | housing | 60 |
| P2 | taxation-and-wealth | 52 |
| P2 | rights-and-civil-liberties | 50 |
| P2 | foreign-policy | 49 |
| P2 | infrastructure-and-public-goods | 41 |
| P2 | immigration | 39 |
| P2 | information-and-media | 35 |
| P2 | technology-and-ai | 34 |
| P2 | elections-and-representation | 34 |
| P2 | anti-corruption | 33 |
| P3 | checks-and-balances | 25 |
| P3 | administrative-state | 25 |
| P3 | science-technology-space | 23 |
| P3 | gun-policy | 17 |
| P3 | executive-power | 16 |
| P3 | legislative-reform | 14 |
| P3 | courts-and-judicial-system | 13 |
| P3 | term-limits-and-fitness | 4 |
| P3 | data-rights-and-privacy | 0 -- all 34 cards already have rule-stmt + rule-notes; Phase 2 mechanical cleanup only |

---

## Testing

After Phase 2: `npm run test:unit` must pass.
After each Phase 4 pillar: `npm run test:unit` must pass.
After all Phase 4 work: `npm run test:e2e` full site check.

---

## Out of Scope

- Redesigning the status system (tracked separately as part of the human review workflow)
- Adding new policy positions
- Changing existing `rule-stmt` or `rule-plain` content on formerly `status-included` cards
- Renaming DB columns to match HTML field names (deferred)
