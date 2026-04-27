# PolicyOS Proposals v2

Generated: 2026-04-26

## What this is

This document is a human-readable proposal for turning the project’s legacy
`SYS-*` rules into a coherent PolicyOS.

PolicyOS is the operating system for the platform. It is not a policy pillar.
It is the rule layer that says how laws, institutions, enforcement systems, and
technical systems should be designed so that the whole platform stays coherent,
rights-preserving, enforceable, and resistant to abuse.

## Why this rewrite is needed

The current legacy `SYS-*` layer captures only part of the idea. Right now it
mixes together:

- real operating rules
- values language
- strategy language
- history and origin language
- geography constraints
- election-specific federalism rules
- early AI rules

The source chats later developed a much stronger and more complete conception of
PolicyOS, but most of that later work was never promoted into the canonical
rule layer.

This proposal turns that later conception into a clearer structure.

## The idea behind PolicyOS

PolicyOS starts from a simple premise:

- policy should behave like a well-designed system
- rights should be real in practice, not only formal on paper
- power should always be attributable, reviewable, and constrained
- systems should fail well rather than collapse into hidden abuse
- enforcement must be real, proportionate, and capable of correction
- no one should lose access to rights because of geography, opacity,
  administrative burden, or concentrated power

In plain terms, PolicyOS is the shared design logic that every pillar should
inherit.

## What PolicyOS is for

PolicyOS is meant to:

1. keep the platform internally consistent across pillars
2. provide shared design rules for laws, institutions, and enforcement
3. ensure that rights and access are usable in the real world
4. prevent hidden power, black-box decisions, and unreviewable harm
5. require systems to be stress-tested, repairable, and accountable
6. provide cross-domain overlays for issues that cut across multiple pillars,
   especially geography, federalism, regulatory design, and AI governance

## Relationship to the five foundations

### Accountable Power

PolicyOS gets from this foundation:

- no one beyond the law
- attributable authority
- review, removal, and correction
- anti-centralization and anti-capture logic

### Clean Democracy

PolicyOS gets from this foundation:

- anti-corruption and anti-capture design
- public-interest regulation
- resistance to concentrated private power
- anti-extraction incentives

### Equal Justice

PolicyOS gets from this foundation:

- equal treatment
- challenge and appeal rights
- no second-class treatment by geography or burden
- human accountability for consequential decisions

### Real Freedom

PolicyOS gets from this foundation:

- no hidden rules or black boxes
- explicit and usable rights
- explainability and auditability
- consequential AI and surveillance limits

### Freedom to Thrive

PolicyOS gets from this foundation:

- practical rather than merely formal access
- material conditions as prerequisites for freedom
- anti-deprivation and anti-precarity design
- regulatory rules that protect health, habitability, and public welfare

## Proposed structure

This proposal uses five canonical families.

### 1. `KERN` — universal kernel

This is the smallest mandatory rule layer. It applies to every pillar.

It covers:

- accountability
- attributable authority
- no hidden rules
- meaningful review and challenge
- anti-bias and anti-asymmetry
- no coercion or deprivation as control
- anti-extraction incentives
- clear enforceable law design
- adaptive review and repair
- stress-testing and anti-gaming

### 2. `GEOG` — geography overlay

This covers cross-jurisdiction equality of access.

It covers:

- rights may not vary by geography
- national baselines where systems are decentralized
- practical access cannot be defeated by distance, burden, or local failure
- cross-jurisdiction fallback and travel support where necessary

### 3. `FEDR` — federalism overlay

This covers anti-centralization and distributed oversight.

It covers:

- no single-point centralization in high-risk systems
- multiple independent oversight layers
- safeguards against both state abuse and federal abuse
- federal baselines without unnecessary direct operational control where
  distributed administration is itself a safeguard

### 4. `REGD` — regulatory-design overlay

This covers how regulation itself should be built and reviewed.

It covers:

- regulation must protect public interest
- distinguish real protections from fake gatekeeping or scarcity
- weakening safeguards must be evidence-based
- anti-capture rulemaking and enforcement
- symbolic under-enforced regulation counts as failure
- periodic regulatory review

### 5. `AIGV` — AI-governance overlay

This covers consequential AI use across the platform.

It covers:

- provenance, auditability, and incident review
- disclosure and labeling
- human-accountability floors
- third-party auditability
- scaled obligations by capability and autonomy
- safety overrides and misuse prevention
- procurement obligations
- adaptive and enforceable AI regulatory authority

## Mandatory and conditional inheritance

Only `KERN` should be mandatory for every pillar.

The overlays should be inherited only where relevant:

- `GEOG`
- `FEDR`
- `REGD`
- `AIGV`

That is the main structural simplification. Instead of pretending every
cross-cutting issue is part of one flat universal system layer, the platform can
use one mandatory kernel and then apply overlays where the design area actually
requires them.

## What should not remain in canonical PolicyOS

Not everything currently in the legacy `SYS-*` layer belongs in the canonical
system-rule layer.

### Move to foundation prose

These belong in the five-foundation layer:

- broad value commitments
- constitutional or social project goals
- equality, dignity, freedom, and anti-extraction statements at the level of
  values

### Move to strategy or project prose

These belong in mission, movement, or history documents:

- "not left vs right"
- coalition / communication strategy
- not-a-party identity language
- historical origin language

### Move to pillar rules

These belong mainly in domain pillars:

- elections remain state/local administered
- federal standards but not direct election control
- domain-specific environmental audit mechanics
- EPA-specific infrastructure
- corporation-specific liability mechanics

## Proposed rules

### `KERN`

- `PLOS-KERN-0001` Platform must remain complete, internally consistent, and auditable.
- `PLOS-KERN-0002` No one beyond law or accountability.
- `PLOS-KERN-0003` Fundamental rights attach to all persons under U.S. jurisdiction.
- `PLOS-KERN-0004` No unchecked concentration of power.
- `PLOS-KERN-0005` All authority must be attributable, auditable, and reviewable.
- `PLOS-KERN-0006` No delegation that reduces accountability or rights protection.
- `PLOS-KERN-0007` Consequential systems must be transparent and explainable.
- `PLOS-KERN-0008` No hidden rules or black-box consequential systems.
- `PLOS-KERN-0009` Public decisions must use verifiable evidence and defined standards.
- `PLOS-KERN-0010` No adverse rights decisions without human accountability.
- `PLOS-KERN-0011` Systems may assist but not replace accountable judgment.
- `PLOS-KERN-0012` Prevent bias amplification and asymmetrical process design.
- `PLOS-KERN-0013` Require challenge, appeal, correction, and independent review.
- `PLOS-KERN-0014` Rights cannot be defeated by burden, delay, opacity, or complexity.
- `PLOS-KERN-0015` Prevent foreseeable abuse before harm occurs.
- `PLOS-KERN-0016` No coercion, deprivation, fear, or precarity as control.
- `PLOS-KERN-0017` Incentives may not reward denial, extraction, or concealment.
- `PLOS-KERN-0018` Laws must be clear and enforceable.
- `PLOS-KERN-0019` Laws need plain-language summaries.
- `PLOS-KERN-0020` Pre-enactment review for loopholes and exploit paths.
- `PLOS-KERN-0021` Periodic review for obsolescence and under-enforcement.
- `PLOS-KERN-0022` Systems must adapt to technological and social change.
- `PLOS-KERN-0023` No known broken systems left in place by inertia.
- `PLOS-KERN-0024` Stress-test against bad actors, misuse, edge cases, and failures.
- `PLOS-KERN-0025` Guard against gaming and strategic exploitation.
- `PLOS-KERN-0026` Systemic failure patterns must trigger corrective action.

### `GEOG`

- `PLOS-GEOG-0001` Rights and essential services may not vary by geography.
- `PLOS-GEOG-0002` Decentralized systems need national equality baselines.
- `PLOS-GEOG-0003` Practical access cannot be defeated by distance, burden, or local failure.
- `PLOS-GEOG-0004` Cross-jurisdiction fallback and travel support when needed.

### `FEDR`

- `PLOS-FEDR-0001` High-risk systems should not create single-point centralization.
- `PLOS-FEDR-0002` Federal baselines without unnecessary direct operational control where decentralization is itself a safeguard.
- `PLOS-FEDR-0003` Multiple independent oversight layers and anti-abuse safeguards.
- `PLOS-FEDR-0004` Balance anti-centralization with enforceable national equality baselines.

### `REGD`

- `PLOS-REGD-0001` Regulation must protect safety, fairness, durability, and public interest.
- `PLOS-REGD-0002` Distinguish real protections from fake gatekeeping and scarcity.
- `PLOS-REGD-0003` Weakening safeguards must be evidence-based.
- `PLOS-REGD-0004` Regulatory process may not become opaque arbitrary gatekeeping.
- `PLOS-REGD-0005` Anti-capture safeguards in rulemaking and enforcement.
- `PLOS-REGD-0006` Symbolic or under-enforced regulation counts as failure.
- `PLOS-REGD-0007` Periodic review to remove bad rules and strengthen good ones.

### `AIGV`

- `PLOS-AIGV-0001` Provenance records for rights-impacting AI.
- `PLOS-AIGV-0002` Label consequential AI-generated or AI-modified content.
- `PLOS-AIGV-0003` No silent replacement of legally required human judgment.
- `PLOS-AIGV-0004` Pre-deployment assessment, monitoring, incident reporting.
- `PLOS-AIGV-0005` Third-party auditability, not self-attestation only.
- `PLOS-AIGV-0006` Scale obligations by capability, autonomy, and misuse risk.
- `PLOS-AIGV-0007` No deployment where catastrophic or systemic risk cannot be mitigated.
- `PLOS-AIGV-0008` Rights-impacting AI must remain reviewable by people, regulators, and courts.
- `PLOS-AIGV-0009` Distinguish assistive, advisory, and delegated AI use.
- `PLOS-AIGV-0010` Public procurement AI review obligations.
- `PLOS-AIGV-0011` Release of high-capability models must consider misuse risk.
- `PLOS-AIGV-0012` No harmful AI impersonation.
- `PLOS-AIGV-0013` Accessibility-support AI allowed only where rights remain protected.
- `PLOS-AIGV-0014` Non-optional safety, security, and misuse-prevention controls.
- `PLOS-AIGV-0015` Narrow override cases with federal approval, scope limits, and disclosure.
- `PLOS-AIGV-0016` Developers must actively prevent misuse by bad actors.
- `PLOS-AIGV-0017` Constitutionally established AI regulator with adaptive and aggressive enforcement powers.

## Closing summary

This proposal treats PolicyOS as the actual operating system for the platform:

- one universal kernel
- four targeted overlays
- pillar rules for domain implementation
- foundation and strategy prose for values and identity

That structure is much closer to the underlying idea from the source chats than
the current flat legacy `SYS-*` layer.
