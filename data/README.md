# Data catalog

The initial structured catalog is stored in SQLite so it can support both editorial work now and a website-backed data model later.

## Why SQLite

- portable and easy to inspect
- strong enough for structured querying
- simple to migrate into a future web application
- good fit for preserving source provenance and imported IDs

## Planned contents

- source files and file hashes
- canonical policy items with numeric IDs
- canonical policy position records with prefixed IDs
- per-source occurrences so duplicates and conflicts stay traceable

## Current schema

- `source_files`
- `legacy_policy_items` — old numeric checkpoint items (preserved for provenance; not the primary table)
- `legacy_policy_item_occurrences`
- `policy_items` — structured policy position records with prefixed IDs (e.g., `HLT-COV-003`); the canonical policy position table
- `rule_occurrences`
- `record_links` — legacy-to-structured ID conversions
- `record_link_occurrences`
- `prose_rule_mentions` — IDs identified in prose/context that are not yet promoted to canonical position rows
- `catalog_entries` view for unified browsing
- `deduped_catalog_entries` view for the canonical structured corpus after legacy-item conversion
- `unresolved_prose_rule_mentions` view for identified IDs that appear only in context/prose and are not yet canonical policy position rows

### policy_items status values

Each `policy_items` row carries a `status` field. Valid values:

| Status | Meaning |
|--------|---------|
| `INCLUDED` | Position is live on the site and confirmed in the DB |
| `MISSING` | In DB but not yet reflected in site HTML (pre-reconciliation: may actually be on the site under a different ID) |
| `PROPOSED` | Authored in DB but not yet reviewed or added to the site |
| `PARTIAL` | Partially implemented on the site; content incomplete |
| `UPDATED` | DB entry updated since last HTML regeneration |
| `UNDEVELOPED` | Placeholder ID; position text not yet written |

> **Note (Phase 1):** Status values were set during initial catalog construction and have not been fully reconciled with the current site HTML. `MISSING` does **not** reliably indicate a position is absent from the site. Do not use status fields as authoritative until after the 3-way reconciliation audit is complete.

## Reconciliation status

The catalog was last rebuilt from source logs in 2025. Since then, policy cards have been added directly to the site HTML. A full reconciliation audit (HTML ↔ DB ↔ source logs) is in progress. Until it completes:

- HTML additions must be backfilled into the DB in the same commit.
- DB additions should include a corresponding HTML card in the same commit.
- Treat both sources as valid; flag divergences for human review rather than auto-resolving them.

## Current import behavior

When the same ID appears multiple times, the database keeps every occurrence and promotes a deterministic canonical record:

1. prefer `main-branch.txt`
2. then prefer `brainstorm-branch.txt`
3. within a source, prefer the latest occurrence

## Dedupe behavior

- current numeric checkpoint items are converted to the structured ID system through `record_links`
- draft migration-map rows from the chats are preserved, but current numeric items are re-mapped against later canonical chat context where early mappings became stale
- prose-only ID mentions are preserved separately so provisional, superseded, or still-unresolved IDs are visible instead of silently dropped
