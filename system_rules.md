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
- Canonical DB: policy/catalog/policy_catalog_v2.sqlite
- Current counts (snapshot): positions=2,783; domains=26; subdomains=506; legacy_id_map=2,783
- Human reports: data/human_report.md, data/full_db_dump.json
- Per-pillar exports and mapping: data/pillar_reports/by_mapping/

Source-of-truth model (phased)
- Phase 1 (current, pre-reconciliation): The site HTML (docs/pillars/*.html, 2,935 policy cards) and the DB (policy/catalog/policy_catalog_v2.sqlite, 2,783 positions) have both been edited since last reconciliation. Neither blindly overrides the other. Divergences are flagged for human review. A full reconciliation audit is in progress.
- Phase 2 (post-reconciliation): policy/catalog/policy_catalog_v2.sqlite becomes the single canonical source of truth. Site HTML is generated output. All new positions are authored in the DB first.

How system rules are used
- As constraints during rule import and deduplication: importer uses these concepts to prefer canonical phrasings and avoid contradictory rule sets.
- As QA checks: new domain rules should be validated against system rules for conflicts or scope violations.
- As governance primitives: approvals, deprecation, and promotion workflows reference system rules to preserve cross-pillar consistency.

Editorial & provenance obligations (non-negotiable)
1. During Phase 1, HTML and the DB are both valid sources; backfill any HTML additions into the DB in the same commit.
2. In Phase 2, the catalog DB is authoritative; record provenance and avoid direct DB edits.
3. Make source edits at the exported/log level and re-run scripts/import_policy_catalog.py to preserve history.
4. Record human approvals explicitly in record_links.notes ("Approved by <Name> — YYYY-MM-DD").
5. Use status fields to deprecate rather than delete.
6. Prefer many-to-one mappings when consolidating duplicate language; document decisions.

System rules dump
A machine-readable extraction of system-level rules is available: data/pillar_reports/by_mapping/system_rules_dump.csv and a human-readable version at data/pillar_reports/by_mapping/system_rules_dump.md. These represent the set of SYS-* canonical policy_items the project treats as foundational. Review and suggest edits by tagging entries in the prose export or filing a small proposal describing intended change and provenance.

Representative system rules (selected highlights)
- CHKS-AINL-0002: Human judgment required for materially harmful decisions; AI absence cannot justify denial.
- CHKS-AINL-0003: Lack of an AI recommendation must not be used as evidence of unfitness.
- CHKS-FEDS-0005: High-risk systems must not be fully centralized; distribute oversight.
- CHKS-FNDS-0009: Guarantee universal equal rights (baseline national standard).
- CHKS-GEOS-0001: Geography must not determine access to rights or care.

(For operational details, see scripts/import_policy_catalog.py and .github/current-state.md.)
