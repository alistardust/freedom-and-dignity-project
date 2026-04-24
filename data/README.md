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
- `policy_items`
- `policy_item_occurrences`
- `policy_items`  (structured ID records, formerly `rule_items`)
- `rule_occurrences`
- `record_links`
- `record_link_occurrences`
- `prose_rule_mentions`
- `catalog_entries` view for unified browsing
- `deduped_catalog_entries` view for the canonical structured corpus after legacy-item conversion
- `unresolved_prose_rule_mentions` view for identified IDs that appear only in context/prose and are not yet canonical policy position rows

## Current import behavior

When the same ID appears multiple times, the database keeps every occurrence and promotes a deterministic canonical record:

1. prefer `main-branch.txt`
2. then prefer `brainstorm-branch.txt`
3. within a source, prefer the latest occurrence

## Dedupe behavior

- current numeric checkpoint items are converted to the structured ID system through `record_links`
- draft migration-map rows from the chats are preserved, but current numeric items are re-mapped against later canonical chat context where early mappings became stale
- prose-only ID mentions are preserved separately so provisional, superseded, or still-unresolved IDs are visible instead of silently dropped
