# PolicyOS Handoff — 2026-04-26

## Current state

PolicyOS work has now split into three distinct layers:

1. `policyos_platform_values_v1.md`
   The platform values layer above PolicyOS itself.

2. `policyos_1_0_rules_proposal.md` and `.csv`
   The system-principles layer: cross-platform rules and overlays.

3. `policyos_authoring_os_v1.md` and `.csv`
   The policy-writing OS layer: how rules must be written, tested, scoped,
   enforced, and maintained.

This was an important correction. Earlier drafts were leaning too heavily
toward high-level principles without a real authoring layer, and too heavily
toward procedural authoring rules without a clear values anchor.

## Most important current conclusion

The values layer is now the upstream foundation for everything else.

The current working hierarchy is:

1. `Platform values`
2. `PolicyOS principles`
3. `PolicyOS authoring OS`
4. `Pillar rules`

## Values layer status

Primary file:
- `policyos_platform_values_v1.md`

This document now explicitly uses a `floor + duty` model.

That means each value has:
- a `floor`: what policy must not violate, erode, or fall beneath
- a `duty`: what policy must actively secure, preserve, build, or advance

This is deliberate. The values layer should not operate only as a negative
screen against bad policy. It should also require affirmative policy design.

Current values in the draft:
- human dignity
- equal standing
- real liberty
- democratic self-government
- accountable power
- transparency
- material security
- ecological habitability
- truthfulness and legibility
- enforceable fairness
- durability against capture and neglect

Important addition:
- environmental protection is treated as foundational
- clean air and clean water are treated as baseline conditions of freedom,
  health, and dignity

## Authoring OS status

Primary files:
- `policyos_authoring_os_v1.md`
- `policyos_authoring_os_v1.csv`

Current authoring families:
- `NORM`
- `AUTH`
- `TEST`
- `ENFC`
- `PLAC`
- `MAINT`

Important recent change:
- `NORM` is now explicitly anchored to `policyos_platform_values_v1.md`
- environmental habitability and transparency are first-class normative review
  concerns
- the bounded-flexibility rule is preserved, but now tied to the values layer

Key idea:
- a rule is not enough if it is procedurally complete
- it must also satisfy the relevant platform values

## Principles layer status

Primary files:
- `policyos_1_0_rules_proposal.md`
- `policyos_1_0_rules_proposal.csv`
- `policyos_1_0_inheritance_matrix.csv`

Current family structure:
- `KERN`
- `GEOG`
- `FEDR`
- `REGD`
- `ENFA`
- `AIGV`

This layer is useful, but it may still need later refinement after the values
and authoring layers stabilize.

## Likely next steps

Best next review order:

1. Review `policyos_platform_values_v1.md`
   Main open question:
   Are the values complete, correctly named, and strong enough as both floors
   and duties?

2. Revisit `policyos_authoring_os_v1.md`
   Main open question:
   Do the `NORM` rules cleanly and fully operationalize the values document?

3. Revisit `policyos_1_0_rules_proposal.md`
   Main open question:
   Once values and authoring logic are stable, do the system-principles rules
   still have the right scope and wording?

## Context for future sessions

The user explicitly wants PolicyOS to be more than a list of high-level policy
principles.

PolicyOS is being developed as an operating system for writing coherent policy
across the platform.

That means it must do at least three things:
- define the values being protected
- define the system-level design constraints
- define the writing and review discipline that every pillar must follow

One especially important user correction in this session:
- values and rules must not be framed only as prohibitions
- they must also include affirmative obligations

That is why the `floor + duty` model now matters so much.
