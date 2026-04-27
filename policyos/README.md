# PolicyOS Research

This directory contains non-canonical research outputs for refactoring the legacy
`SYS-*` rule set into a coherent "PolicyOS" layer.

Files:

- `policyos_legacy_system_rules.csv` — snapshot of the current canonical legacy
  `SYS-*` rules as exported from `data/policy_catalog.sqlite`
- `policyos_proposed_rules.csv` — proposed PolicyOS kernel and overlay rules,
  categorized into explicit `SYS` families so scope stays coherent
- `policyos_proposed_rules_v2.csv` — second-pass proposed canonical rules using
  the tighter `KERN / GEOG / FEDR / REGD / AIGV` structure
- `policyos_proposals_v2.md` — human-readable version of the second-pass
  proposal with introduction, rationale, and family-by-family layout
- `policyos_1_0_rules_proposal.csv` — current final-draft CSV proposal for
  PolicyOS 1.0
- `policyos_1_0_rules_proposal.md` — self-contained final-draft markdown
  proposal for PolicyOS 1.0
- `policyos_1_0_inheritance_matrix.csv` — canonicalization-oriented inheritance
  matrix mapping PolicyOS families to pillar slugs
- `policyos_authoring_os_v1.csv` — draft value-constrained authoring OS for how
  policy should be written, tested, scoped, enforced, and maintained
- `policyos_authoring_os_v1.md` — human-readable version of the PolicyOS
  authoring layer, including normative alignment requirements
- `policyos_platform_values_analysis.md` — analysis of the platform’s bedrock
  values, including environmental habitability and clean air / water as
  first-class commitments
- `policyos_platform_values_v1.md` — short canonical values layer intended to
  anchor the PolicyOS normative family
- `policyos_gap_analysis.md` — audit of what exists in the DB, what exists only
  in the source chats, and what should move out of the system-rule layer
- `policyos_plain_language.md` — distilled plain-language explanation of the
  current rule set, shared values, and the foundations underneath it
- `policyos_pillar_matrix.csv` — pillar-level inheritance map showing which
  PolicyOS families each live pillar should implement
- `policyos_taxonomy_v2.md` — second-pass taxonomy describing the final layered
  model: kernel, overlays, pillar rules, and prose
- `policyos_missing_items_review.md` — reviewed table of missing source-chat
  items with recommended final scope

Status:

- Research only
- Not yet imported into either SQLite catalog
- Intended to guide the next canonical rewrite of `system_rules.md` and any
  future DB import / migration work
