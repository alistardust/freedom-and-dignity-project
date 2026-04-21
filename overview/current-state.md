# Current State

## Source-of-truth order

1. `sources/chat-logs/main-branch.txt`
2. `sources/chat-logs/brainstorm-branch.txt`
3. `data/policy_catalog.sqlite`
4. legacy markdown under `pillars/` as working scaffolding only

The pillar files may be outdated. Use the chat logs and the catalog before assuming a pillar file is complete.

## Catalog state

The current importer reconstructs four layers from the main and brainstorm chats:

1. **Canonical numeric checkpoint items** in `policy_items`
2. **Canonical structured rules** in `rule_items`
3. **Legacy-to-structured conversions** in `record_links`
4. **Contextual/prose-only ID mentions** in `prose_rule_mentions`

### Current totals

- 101 `policy_items`
- 1,051 `rule_items`
- 138 `record_links`
- 888 `prose_rule_mentions`

### Recent actions

- The importer was updated to include `brainstorm-branch1part2.txt` and re-run to capture recently added structured rows.
- A dedupe audit was performed and a JSON report saved to `data/dedupe_report.json`.
- Many-to-one record links were reviewed and 43 mappings were explicitly approved by Alice; approval notes are stored in `record_links.notes` and `record_link_occurrences.notes`.
- A full DB dump and an intent report were saved to `data/full_db_dump.json` and `data/intent_report.json` respectively.

### What is fully converted

All current numeric checkpoint items (`192`-`292`) now have structured-ID conversions recorded in `record_links`.

### What was promoted from context

These structured IDs were identified in the chats but had been missed by the first importer because they never appeared as canonical pipe-delimited rows:

- `ECO-TAX-001`
- `ADM-CHV-001`
- `ADM-AGY-001`
- `HLT-TRL-001`

### Why contextual mentions matter

Some IDs appear only in prose or summary sections. Context shows they are not all equally authoritative:

- some are **future split placeholders** like `ADM-CON-001A` / `ADM-CON-001B`
- some are **optional/procedural variants** like `ADM-OVR-001`
- some are **older families later replaced or reframed** like `SYS-STR-*` or `HLT-DRG-*`
- some may be **real but still-unformalized candidates** such as `RGT-LAB-001`, `ECO-WRK-001`, `JUS-CRJ-001`, `JUS-CRJ-002`, and `RGT-DET-003`

Those are intentionally preserved in `unresolved_prose_rule_mentions` instead of being silently promoted into the canonical rule corpus.

## Important context from the chats

- The migration map embedded in the chats is useful, but not always final. Later summary blocks and later formal rule rows sometimes supersede earlier ID assignments.
- The main and brainstorm branches currently contain the same structured corpus, but the brainstorm branch includes important contextual explanations about duplication, provisional IDs, and when not to split an item yet.
- Some policy areas are much more developed in the database than in the pillar markdown, especially healthcare governance, AI/system rules, justice/drug policy, and media/journalist protections.
