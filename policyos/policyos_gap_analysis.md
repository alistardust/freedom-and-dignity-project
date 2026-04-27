# PolicyOS Gap Analysis

Generated: 2026-04-26

## Scope Audit

The current canonical `SYS-*` layer in `data/policy_catalog.sqlite` is underscoped
and internally mixed:

- 36 total legacy `SYS-*` rules
- 7 `SYS-AI-*` rules
- 18 `SYS-FND-*` rules
- 5 `SYS-FED-*` rules
- 5 `SYS-GEO-*` rules
- 1 `SYS-RUL-*` rule
- 0 canonical `SYS-REG-*` rules

This does not match the source-chat design. In
`sources/political_project_brainstorm.txt`, the later PolicyOS logic expands into:

- `SYS-RUL-002` through `SYS-RUL-030`
- `SYS-REG-001` through `SYS-REG-008`
- `SYS-AI-008` through `SYS-AI-034`

In other words, the database currently preserves the earliest shell of system
rules, but not the later operating-system layer that actually explains how policy
should be designed, enforced, stress-tested, and adapted.

## Main Findings

### 1. The current canonical layer mixes rule types that should not share one bucket

The legacy `SYS-*` set currently mixes:

- true operating rules
- geography constraints
- election/federalism design constraints
- foundation beliefs
- project-branding and movement-framing statements
- one historical-origin statement

That mixture is why the current layer feels incoherent. A policy operating system
needs design invariants, not a merged list of values, strategy, and history.

### 2. Several legacy `SYS-FND-*` entries are mis-scoped

These are important statements, but many are not kernel operating rules:

- `SYS-FND-008` — "Movement is not left vs right"
- `SYS-FND-010` — "Includes communication and coalition strategy"
- `SYS-FND-011` — "Not a political party"
- `SYS-FND-012` — "Origin tied to post-Trump instability concerns"

They belong in foundation prose, strategy documents, or project history rather
than the PolicyOS kernel.

### 3. The later source-chat rules are closer to the real PolicyOS concept

The later `SYS-RUL-*`, `SYS-REG-*`, and expanded `SYS-AI-*` blocks capture the
actual design logic described in the handoff and in the user’s direction:

- completeness and conflict checking
- anti-centralization and anti-capture
- enforceability with teeth
- proportionality and escalation
- fail-well design
- challenge, appeal, and correction
- no hidden rules or black boxes
- geography equality
- practical usability of rights
- anti-coercion / anti-extraction incentives
- periodic review and adaptive governance

### 4. The current canonical set leaves major operational gaps

The DB-preserved `SYS-*` layer does not yet canonically express:

- pre-enactment loophole review
- plain-language requirement for laws
- system stress-testing
- anti-gaming and anti-exploitation design
- mandatory corrective action on repeated failure
- regulatory-design principles
- scaled AI obligations by capability and use mode
- AI override controls and approval criteria
- constitutional AI-regulator concept
- aggressive baseline enforcement language

## Correct Scope Recommendation

To keep the system coherent, PolicyOS should use `scope_code = SYS` only for
true cross-platform design rules, then split by family:

- `CORE` — invariant system architecture rules
- `SAFE` — fail-well, review, transparency, and abuse-prevention rules
- `GEOG` — geography equality and practical-access rules
- `ENFC` — enforceability, penalties, audits, and corrective-action rules
- `ADPT` — periodic review and adaptive-governance rules
- `REGD` — regulatory-design rules
- `THRV` — minimum material-security requirements that every pillar must respect
- `AIGV` — cross-domain AI governance rules

Legacy families should be treated as follows:

- Keep `SYS-AI-*` as system scope, but expand and modernize it
- Keep `SYS-GEO-*` as system scope, but fold into a broader geography family
- Keep `SYS-FED-*` as system scope only where the rule is truly cross-domain;
  otherwise treat it as a checks/elections overlay
- Move many `SYS-FND-*` statements out of the PolicyOS kernel into foundation or
  strategy prose
- Replace the one-line `SYS-RUL-001` shell with a real `CORE` + `SAFE` + `ENFC`
  + `ADPT` structure

## Gap Categories

### Kernel gaps

- No canonical anti-hidden-rule rule
- No canonical appeal / correction rule
- No canonical anti-coercion / anti-precarity rule
- No canonical anti-gaming / stress-test rule
- No canonical mandatory-correction rule

### Enforcement gaps

- No canonical plain-language requirement
- No canonical pre-enactment loophole review
- No canonical proportional-penalty rule
- No canonical symbolic-rule failure standard
- No canonical audit-log requirement for high-risk systems

### Regulatory-design gaps

- No canonical anti-capture regulatory family
- No canonical distinction between real safeguards and fake gatekeeping
- No canonical evidence standard for weakening protections

### AI-governance gaps

- No canonical provenance / incident / labeling rules after `SYS-AI-007`
- No canonical capability-tiered governance
- No canonical safety-override approval framework
- No canonical constitutional AI regulator

### Material-conditions gaps

- The current system layer implies material security through the foundations, but
  does not operationalize minimum baseline security across all pillars.

## Recommended Next Canonicalization Order

1. Replace the legacy one-bucket system-rule concept with the scoped PolicyOS
   families in `policyos_proposed_rules.csv`
2. Move non-operating `SYS-FND-*` statements into foundation or strategy prose
3. Preserve geography rules as system scope
4. Preserve only truly cross-domain federalism rules as system scope
5. Canonicalize the expanded AI-governance family
6. Add pillar-specific overlays that inherit the PolicyOS kernel rather than
   rewriting it separately inside each pillar
