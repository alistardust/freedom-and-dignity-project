# PolicyOS Taxonomy v2

Generated: 2026-04-26

This is the tightened second-pass taxonomy for canonicalizing PolicyOS.

## Design Goal

The canonical system layer should stop treating every cross-cutting idea as the
same kind of rule. PolicyOS should instead distinguish:

1. a small universal kernel
2. named cross-domain overlays
3. pillar implementation rules
4. foundation and strategy prose

That split preserves rigor and keeps the system layer from becoming a grab-bag
of values, history, and domain specifics.

## Layer Model

### 1. `SYS kernel`

The smallest universal rule layer. These rules apply to every pillar and every
institutional design area.

Kernel topics:

- accountability
- attributable authority
- no hidden rules
- meaningful review and challenge
- anti-bias and anti-asymmetry
- no coercion / deprivation as control
- anti-extraction incentives
- clear enforceable law design
- adaptive review and repair
- stress-testing and anti-gaming

Source basis:

- primarily `SYS-RUL-002` through `SYS-RUL-030`
- selected parts of the current `SYS-GEO-*` logic

### 2. `SYS geography overlay`

Cross-domain overlay for practical equality of access across jurisdictions.

Overlay topics:

- rights may not vary by geography
- decentralized systems need national minimums
- practical access cannot be defeated by distance, burden, or local failure
- cross-jurisdiction fallback and travel support where needed

Source basis:

- current `SYS-GEO-001` through `SYS-GEO-005`
- `SYS-RUL-015` through `SYS-RUL-017`

### 3. `SYS federalism overlay`

Cross-domain overlay for anti-centralization, distributed control, and
multi-layer oversight where design must balance federal standards with local
administration.

Overlay topics:

- high-risk systems should not create single-point centralization
- multiple oversight layers
- safeguards against abuse at both state and federal levels
- federal standards without unnecessary direct operational control in areas
  where distributed administration is itself a safeguard

Source basis:

- current `SYS-FED-001`, `SYS-FED-004`, `SYS-FED-005`
- current `SYS-FED-002` and `SYS-FED-003` only as elections-specific pillar rules
- `SYS-RUL-004` and `SYS-RUL-016`

### 4. `SYS regulatory-design overlay`

Cross-domain overlay for designing, revising, and enforcing regulation without
capture, fake efficiency arguments, or symbolic enforcement.

Overlay topics:

- regulation must protect public interest
- distinguish real safeguards from artificial scarcity / gatekeeping
- weakening protections must be evidence-based
- anti-capture rulemaking and enforcement
- symbolic under-enforced regulation counts as system failure
- periodic review of regulatory frameworks

Source basis:

- `SYS-REG-001` through `SYS-REG-008`
- `SYS-RUL-007`

### 5. `SYS AI-governance overlay`

Cross-domain overlay for consequential AI use across all pillars.

Overlay topics:

- provenance, logging, and incident review
- labeling and disclosure
- human-accountability floor in high-stakes domains
- third-party auditability
- scaled obligations by capability and autonomy
- override-control governance
- misuse prevention
- procurement review
- adaptive constitutional AI regulatory authority

Source basis:

- current `SYS-AI-001` through `SYS-AI-007`
- source-chat `SYS-AI-008` through `SYS-AI-034`

## What does *not* belong in canonical PolicyOS

### Foundation prose

These belong in the five-foundation layer rather than in the canonical system
rule layer:

- broad value commitments
- constitutional or social project goals
- statements of equality, dignity, freedom, anti-extraction, and material security
  at the level of values rather than operational design

Examples:

- `SYS-FND-004`
- `SYS-FND-005`
- `SYS-FND-016`
- `SYS-FND-018`

### Strategy / project prose

These belong in mission, movement, or history documents rather than in the
canonical system layer:

- not-left-vs-right framing
- coalition / communication strategy
- organizational identity statements
- historical origin statements

Examples:

- `SYS-FND-008`
- `SYS-FND-010`
- `SYS-FND-011`
- `SYS-FND-012`

### Pillar rules

Some source-chat rules are too domain-specific to remain in the system layer.

Examples:

- elections remain state/local administered
- federal sets election standards without direct control
- anti-impersonation rules that also need consumer / civil-rights implementation
- environmental audit mechanics and EPA-specific infrastructure
- corporate liability specifics that should also live under antitrust / environment / labor

## Recommended Canonical Family Map

| Canonical family | Type | Mandatory for all pillars | Primary source blocks |
|---|---|---:|---|
| `KERN` | universal kernel | Yes | `SYS-RUL-002` to `SYS-RUL-030` |
| `GEOG` | system overlay | No | `SYS-GEO-*`, `SYS-RUL-015` to `017` |
| `FEDR` | system overlay | No | `SYS-FED-*`, `SYS-RUL-004`, `016` |
| `REGD` | system overlay | No | `SYS-REG-*`, `SYS-RUL-007` |
| `AIGV` | system overlay | No | `SYS-AI-*` |

## Mandatory vs Conditional Inheritance

### Mandatory

Every pillar should inherit:

- `KERN`

### Conditional

Pillars should inherit overlays only where the design area requires them:

- `GEOG`
- `FEDR`
- `REGD`
- `AIGV`

This is the key simplification. The current research bundle treated several
families as if they were universally inherited. The stronger model is:

- one mandatory kernel
- optional overlays by pillar

## Canonical Rewrite Implications

If we adopt this taxonomy, the next rewrite should:

1. replace the current multi-family universal model with `KERN` as the only
   universal mandatory family
2. move geography rules into a dedicated `GEOG` overlay
3. add a dedicated `FEDR` overlay
4. move anti-capture / regulatory design rules out of kernel language
5. keep AI governance explicitly as an overlay rather than pretending it is part
   of the smallest universal kernel
