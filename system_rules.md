# System Rules

This file documents the project's cross-domain "system rules": constraints and guarantees that apply across pillars to avoid contradictions, loopholes, and structural drift. It records how rules are tracked, edited, and reviewed so contributors preserve provenance and consistency.

Last updated: 2026-04-21T19:17:48-04:00 (user session)

Current catalog counts (authoritative source: data/policy_catalog.sqlite):

- rule_items: 1,051
- policy_items: 101
- record_links: 138
- prose_rule_mentions: 888

Paths to key artifacts
- Database (canonical): data/policy_catalog.sqlite
- Human reports and exports: data/human_report.md, data/full_db_dump.json
- Per-pillar exports (mapping-based): data/pillar_reports/by_mapping/
- Prose mentions export (full): data/pillar_reports/by_mapping/prose_rule_mentions_full.csv
- Unresolved prose mentions (if present): data/pillar_reports/by_mapping/unresolved_prose_rule_mentions.csv

Rule families and core intents
- Foundational rules: mission, architecture, baseline civic values.
- Geographic equality: avoid service/rights fragmentation by location.
- Federalism & balance: design mechanisms to defend against both fragmentation and capture.
- AI & algorithmic governance: require human accountability, prevent denial bias and hidden harms.
- Domain obligations: every pillar must implement the shared cross-domain constraints.

Editorial and provenance rules (must follow)
1. Source of truth: the catalog DB (data/policy_catalog.sqlite). Do not hand-edit the DB unless you know the migration provenance.
2. Preferred edits: update source chat logs / importer inputs and re-run scripts/import_policy_catalog.py so provenance is recorded.
3. Small corrections: prefer adding a record_link or record_link_occurrence with explicit notes rather than changing canonical statements directly.
4. Approvals & notes: when approving mappings, append "Approved by <Name>" and a date to record_links.notes or record_link_occurrences.notes so human approvals remain auditable.
5. Do not delete historical rows; use status fields (eg. status='deprecated' or notes) to indicate changes.

Review workflow for prose mentions
- Export for review: data/pillar_reports/by_mapping/prose_rule_mentions_full.csv (full table) and unresolved_prose_rule_mentions.csv (filtered unresolved set).
- Reviewer actions: tag rows with a proposed target_rule_id, suggest new rule_ids (seed), or mark as false-positive. Collect changes in a review CSV and submit for import via scripts/import_policy_catalog.py or the maintenance script used by the project.

Next steps (recommended priorities)
- Review prose_rule_mentions_full.csv to identify candidates for promotion to rule_items.
- Produce per-pillar mapping corrections (if scope_code→pillar mapping needs adjustment).
- Create a small review board (2–3 reviewers) to approve promotions — approvals recorded in record_links.notes.

Contacts & operational notes
- Importer script: scripts/import_policy_catalog.py — controls parsing, canonical choice, and manual seed application. Re-run this to pick up source fixes.
- If unsure, open an issue or add a short note in overview/current-state.md describing the change request and rationale.

This file is intentionally procedural: changes to policy modeling must preserve provenance and be reproducible via the importer workflow.
