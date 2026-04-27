# PolicyOS Authoring OS v1

Generated: 2026-04-26

## Purpose

This document defines the actual operating-system layer for writing policy in
this project.

The system-principles layer answers: what must be true across the platform?

The authoring OS answers: how should policy be written, tested, scoped,
enforced, and maintained so that the platform stays coherent, executable, and
faithful to the project’s values?

This layer is primarily procedural, but it is not value-neutral. It governs
policy-writing discipline in a way that is meant to carry equality, fairness,
liberty, dignity, accountability, anti-capture, and practical access into the
actual drafting process. It is meant to ensure that those values are not merely
aspirational background principles, but active drafting constraints that shape
what can be written, how it must be written, and what kinds of ambiguity are
acceptable.

## What this layer does

The Authoring OS is meant to ensure that:

- rules are driven by the platform’s core values rather than only by technical completeness
- rules are structurally complete rather than symbolic
- rights are made usable in practice rather than only declared
- enforcement is designed rather than assumed
- flexibility is preserved for future adaptation without allowing vague language to hollow out the rule
- scope placement is disciplined rather than arbitrary
- loopholes, burden-shifting, and abuse paths are checked before adoption
- maintenance and revision are built into the platform instead of deferred

## Families

This draft uses six authoring families:

- `NORM` — normative alignment requirements
- `AUTH` — rule construction requirements
- `TEST` — validation and adversarial review requirements
- `ENFC` — enforcement-design requirements
- `PLAC` — scope and placement rules
- `MAINT` — maintenance, revision, and deprecation rules

The `NORM` family should be read together with
[policyos_platform_values_v1.md](/home/alice/git/freedom-and-dignity-project/data/pillar_reports/by_mapping/policyos_research/policyos_platform_values_v1.md:1),
which serves as the current source text for the platform’s normative layer.

## `NORM` — normative alignment requirements

- `PAOS-NORM-0001` Every proposed rule must identify which named platform values from `policyos_platform_values_v1.md` it advances, protects, constrains, or places into tension.
- `PAOS-NORM-0002` No proposed rule may be accepted if it undermines human dignity, equal standing, real liberty, meaningful accountability, transparency, practical access, or enforceable fairness without an explicit, compelling, and reviewable justification.
- `PAOS-NORM-0003` Every proposed rule must be reviewed for whether it creates unequal classes of people, selective burdens, arbitrary exclusions, or second-class access in practice.
- `PAOS-NORM-0004` Every proposed rule involving enforcement, punishment, or state power must be reviewed for whether it preserves accountability, proportionality, due process, and meaningful review.
- `PAOS-NORM-0005` Every proposed rule must be reviewed for whether it creates capture opportunities, unreviewable discretion, hidden power, or conditions under which any actor becomes functionally above the law.
- `PAOS-NORM-0006` Every proposed rule affecting basic needs, essential services, or rights access must be reviewed for whether it preserves practical usability, not merely formal entitlement.
- `PAOS-NORM-0007` Every proposed rule with environmental, infrastructure, industrial, extractive, land-use, agricultural, health, or technological impact must be reviewed for whether it degrades ecological habitability, clean air, clean water, safe food systems, or the shared environmental conditions required for freedom and health.
- `PAOS-NORM-0008` Where core platform values come into tension within a proposed rule, the conflict must be surfaced explicitly, named against the values document, and resolved in the drafting rather than hidden inside vague language or implementation discretion.
- `PAOS-NORM-0009` Where a rule uses general standards, broad protective language, or open-textured terms to preserve future adaptability, that flexibility must be anchored to explicit baseline protections and stated purpose and may not be interpreted to dilute dignity, equality, liberty, transparency, accountability, enforceability, ecological protection, or the rule’s core protective intent.

## `AUTH` — rule construction requirements

- `PAOS-AUTH-0001` Every proposed policy rule must identify the actor being regulated, the conduct being required or prohibited, the trigger condition, and the intended outcome.
- `PAOS-AUTH-0002` Every proposed policy rule must specify the enforcement authority, enforcement mechanism, remedy or penalty, and review or appeal path where violations or denials are possible.
- `PAOS-AUTH-0003` Every proposed policy rule must be written in language that is clear enough to implement, review, and audit without relying on unstated assumptions.
- `PAOS-AUTH-0004` Every proposed policy rule must distinguish between the normative requirement, the implementation mechanism, and any optional examples or commentary.
- `PAOS-AUTH-0005` Every proposed policy rule must identify whether it creates a right, duty, prohibition, process requirement, design constraint, reporting obligation, funding obligation, or enforcement mechanism.
- `PAOS-AUTH-0006` Every proposed policy rule must identify the level at which it operates: constitutional, statutory, regulatory, administrative, institutional, contractual, or technical-system design.
- `PAOS-AUTH-0007` Every policy section must separate universal principle statements from operational rules and from explanatory prose.
- `PAOS-AUTH-0008` Where a policy requires discretion, the rule set must state the governing standards, documentation duties, and review mechanisms that constrain that discretion.
- `PAOS-AUTH-0009` Rules must balance explicit baseline commitments with bounded interpretive flexibility: the baseline must be specific enough to establish enforceable minimums and clear intent, while any open-textured language must not be interpretable in ways that defeat the rule’s purpose or protections.

## `TEST` — validation and adversarial review requirements

- `PAOS-TEST-0001` Every proposed rule must be tested for loopholes, exploit paths, burden-shifting, selective enforcement risk, and foreseeable abuse patterns before acceptance.
- `PAOS-TEST-0002` Every proposed rule affecting rights, access, or eligibility must be tested against practical barriers including cost, distance, disability, language, timing, digital access, and paperwork burden.
- `PAOS-TEST-0003` Every proposed rule must be checked for conflict with existing rules in the same pillar, overlapping pillars, and applicable system overlays.
- `PAOS-TEST-0004` Every proposed rule must be reviewed for whether it creates perverse incentives, hidden rationing, delay incentives, denial incentives, or extraction incentives.
- `PAOS-TEST-0005` Every high-risk rule must be evaluated against bad-actor behavior, edge cases, noncompliance patterns, and likely institutional workarounds.
- `PAOS-TEST-0006` Every rights-limiting or coercive rule must identify the least-abusive alternative considered and explain why the chosen design is justified.
- `PAOS-TEST-0007` Every proposed rule set must define what successful implementation, implementation failure, non-enforcement, and systemic breakdown would look like in practice.

## `ENFC` — enforcement-design requirements

- `PAOS-ENFC-0001` No rule should be accepted as complete unless it defines who enforces it, how enforcement begins, what evidence is needed, and what happens when enforcement fails.
- `PAOS-ENFC-0002` Where violations are likely to recur or be concealed, the rule set must specify monitoring, audit, reporting, inspection, or detection mechanisms appropriate to the risk.
- `PAOS-ENFC-0003` Where the platform proposes penalties, it must specify escalation logic and the threshold for moving from ordinary enforcement to structural intervention or individual liability.
- `PAOS-ENFC-0004` Where a rule depends on reporting, the rule set must specify reporting format, cadence, auditability, and consequences for false, missing, or manipulated reporting.
- `PAOS-ENFC-0005` Where a rule creates appeal, challenge, or review rights, the rule set must identify timelines, access standards, record access, and decision authority for that review.

## `PLAC` — scope and placement rules

- `PAOS-PLAC-0001` Every proposed rule must be placed at the narrowest scope that still preserves consistency: kernel, overlay, pillar, cross-pillar coordination rule, foundation prose, or strategy prose.
- `PAOS-PLAC-0002` A rule belongs in the universal system layer only if it applies across multiple pillars as a design invariant rather than as a domain-specific policy preference.
- `PAOS-PLAC-0003` A rule belongs in an overlay when it is cross-domain but conditional, meaning it applies only to pillars with a recurring design problem such as geography, federalism, regulation, enforcement architecture, or AI.
- `PAOS-PLAC-0004` A rule belongs in a pillar when its implementation details, metrics, institutions, or harms are domain-specific enough that universal treatment would reduce clarity or accuracy.
- `PAOS-PLAC-0005` A statement belongs in prose rather than canon when it expresses values, narrative framing, project identity, strategy, or history without creating a design invariant or enforceable policy requirement.

## `MAINT` — maintenance, revision, and deprecation rules

- `PAOS-MAINT-0001` Every major policy section must identify which rules are core, which are implementation-dependent, and which are expected to require future revision as conditions change.
- `PAOS-MAINT-0002` When a rule is revised, the revision must state whether the change closes a loophole, updates a condition, resolves a conflict, improves enforceability, or narrows overbreadth.
- `PAOS-MAINT-0003` Deprecated rules should be superseded with visible traceability rather than silently removed when provenance or interpretation history matters.
- `PAOS-MAINT-0004` Every pillar must periodically review for missing policy areas, stale assumptions, under-enforced rules, and newly visible system vulnerabilities.
- `PAOS-MAINT-0005` Where a system overlay applies to a pillar, the pillar should explicitly state how that overlay is implemented locally rather than assuming the inheritance is obvious.

## How this relates to the principles layer

The current PolicyOS principles draft says what the platform must protect
against and what a just, auditable, enforceable system should look like.

This Authoring OS says how new policy should be written so that those principles
are actually carried into the platform consistently.

In short:

- the principles layer defines the platform’s design constraints
- the authoring layer defines the workflow, value checks, and structural requirements for writing policy under those constraints
