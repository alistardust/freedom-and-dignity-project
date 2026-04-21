# System Rules

Purpose and intent

The "system rules" are the minimal, foundational constraints that the entire project uses to evaluate, align, and integrate policy proposals. They are not policy prescriptions for a single domain; they are normative design constraints that govern how domain rules, governance architectures, and technical controls must behave so the whole corpus is coherent, auditable, and rights-preserving.

Key design goals
- Preserve human dignity and equal treatment across jurisdiction and technology.
- Make algorithmic systems auditable, accountable, and secondary to independent human judgment for high-stakes decisions.
- Prevent fragmentation of core rights by geography or administrative boundary.
- Distribute risk: avoid single-point centralization in high-risk systems and require layered oversight.
- Maintain provenance: every canonical rule must be traceable to source artifacts (chat logs, imports, and explicit approvals).

Authoritative sources and counts
- Canonical DB: data/policy_catalog.sqlite
- Current counts (snapshot): rule_items=1,051; policy_items=101; record_links=138; prose_rule_mentions=888
- Human reports: data/human_report.md, data/full_db_dump.json
- Per-pillar exports and mapping: data/pillar_reports/by_mapping/

How system rules are used
- As constraints during rule import and deduplication: importer uses these concepts to prefer canonical phrasings and avoid contradictory rule sets.
- As QA checks: new domain rules should be validated against system rules for conflicts or scope violations.
- As governance primitives: approvals, deprecation, and promotion workflows reference system rules to preserve cross-pillar consistency.

Editorial & provenance obligations (non-negotiable)
1. The catalog DB is authoritative; record provenance and avoid direct DB edits.
2. Make source edits at the exported/log level and re-run scripts/import_policy_catalog.py to preserve history.
3. Record human approvals explicitly in record_links.notes ("Approved by <Name> — YYYY-MM-DD").
4. Use status fields to deprecate rather than delete.
5. Prefer many-to-one mappings when consolidating duplicate language; document decisions.

System rules dump
A machine-readable extraction of system-level rules is available: data/pillar_reports/by_mapping/system_rules_dump.csv and a human-readable version at data/pillar_reports/by_mapping/system_rules_dump.md. These represent the set of SYS-* canonical rule_items the project treats as foundational. Review and suggest edits by tagging entries in the prose export or filing a small proposal describing intended change and provenance.

Representative system rules (selected highlights)
- SYS-AI-002: Human judgment required for materially harmful decisions; AI absence cannot justify denial.
- SYS-AI-003: Lack of an AI recommendation must not be used as evidence of unfitness.
- SYS-FED-001: High-risk systems must not be fully centralized; distribute oversight.
- SYS-FND-004: Guarantee universal equal rights (baseline national standard).
- SYS-GEO-001: Geography must not determine access to rights or care.

Next actions
- Review the system_rules_dump.md and flag items for refinement.
- Nominate up to 20 prose mentions for promotion; use the CSV review pattern and submit as a batch for importer ingestion.

(For operational details, see scripts/import_policy_catalog.py and overview/current-state.md.)
