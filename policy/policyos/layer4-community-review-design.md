# PolicyOS Layer 4: Community Review System
## Design Document for Review

**Status:** Pre-spec. Seeking design review before writing the formal specification.
**Last updated:** 2026-05-11
**Author:** Alisdair Calder (alistardust)
**Feedback welcome via:** GitHub issue, PR comment, or direct message

---

## Context: What Is This?

**The Freedom and Dignity Project** is an open-source U.S. policy platform. It publishes
detailed policy positions across 25 pillars (healthcare, housing, labor, criminal justice,
etc.) organized around five foundations. All content is on GitHub; anyone can read, comment,
or submit changes via pull request.

**PolicyOS** is the internal governance layer that defines how policy is written, structured,
and changed. It has four layers:

1. **Platform Values** -- the moral floor. Non-negotiable by any process.
2. **System Principles** -- cross-cutting design rules for all policy.
3. **Authoring OS** -- how individual policy rules must be written and tested.
4. **Community Review System** -- (this document) how community members evaluate
   and improve policy positions over time.

This document describes Layer 4. It is a design document, not an implementation plan.
Nothing here has been built. We are looking for feedback before writing the formal spec.

---

## The Problem

The project publishes policy positions and claims they reflect democratic values. That
claim requires a real mechanism for community members to scrutinize, challenge, and
improve those positions. Without one, the platform is a top-down publication dressed in
participatory language.

The review system is the mechanism that makes the legitimacy claim real. It gives U.S.
residents a structured, weighted voice in whether policy positions are:

- Technically sound and well-reasoned
- Supported by credible research and sources
- Accurately reflective of the experiences of affected people
- Clearly and accessibly written

Critically, the review system can **force policy changes** when community consensus
warrants it. This is by design, not an edge case.

---

## What This Is Not

- Not a voting system on political opinions ("do you support this policy?")
- Not a comment section
- Not an edit-anyone-can-make system (Wikipedia model)
- Not a top-down expert panel with a community rubber stamp

---

## Core Design Principles

1. **Community review can force policy changes.** When the community reaches consensus
   that a position is flawed, that finding results in a change -- not a suggestion. The
   platform maintainer's role shifts to anti-capture oversight, not content veto.

2. **Maintainer veto is narrow and public.** The maintainer can block a community-approved
   change only on Platform Values grounds (Layer 1). That block must be public, explained,
   and appealable. There is no other valid grounds for a veto.

3. **Weight dimensions, not people.** A reviewer's influence on any given review is
   determined by their demonstrated competence in that specific dimension (technical rigor,
   research quality, lived experience, accessibility) for that domain. No global reviewer
   score. No reputation economy.

4. **Sortition over self-selection.** Review assignments are partially random to prevent
   organized capture by any coordinated group.

5. **Transparency over secrecy.** All weighting decisions, aggregation outputs, and
   moderation actions are logged to an append-only audit log and are publishable as
   aggregate statistics.

6. **Probabilistic trust, not binary gates.** Authenticity enforcement uses risk scores and
   elevated scrutiny, not instant exclusions. VPNs alone are not penalized.

---

## Governance Authority Model

The community review system replaces the current maintainer-centric change model for
policy content.

```
AUTHORITY HIERARCHY

Community consensus (via review process)
    |
    v
Maintainer review
    |
    |-- Can APPROVE: always
    |-- Can IMPLEMENT: always
    |-- Can BLOCK: ONLY on Layer 1 Platform Values grounds
    |              Block must be public, reasoned, and appealable
    |-- CANNOT: content veto, delay indefinitely, unilateral revert
    |
    v
Change goes live

Platform Values (Layer 1) -- HARD FLOOR
    Cannot be overridden by community consensus
    Cannot be overridden by maintainer authority
    Amendment requires its own governance process
```

---

## System Architecture

The system has 12 components. They are described individually below.

```
SYSTEM OVERVIEW

[1] Reviewer Profiles
    |
    v
[2] Training + Credentialing
    |
    v                          [12] Signal Integrity Layer
[3] Weighting Engine <-------- (trust scores feed here)
    |
    v
[4] Assignment / Routing (Sortition + Profile Match)
    |
    v
[5] Review Interface + Criteria Engine
    |
    v
[6] Aggregation + Change Pipeline
    |
    v
[7] Moderation
    |
    v
[8] Appeals
    |
    v
[9] Governance / Review Board
    |
    v
[10] Anti-Capture Mechanisms
    |
    v
[11] Audit Logging (immutable, cross-cutting)
```

---

## Component Designs

### Component 1: Reviewer Profiles

Each reviewer has a profile storing:

- Training completions per policy domain and review dimension
- Calibration scores per dimension (derived from comparison to a ground-truth corpus)
- Voluntarily disclosed demographic data (see privacy note below)
- Trust score (produced by the Signal Integrity Layer; see Component 12)
- Current scrutiny level (normal, elevated, or queued for human review)
- Review history (anonymized for weighting purposes; not publicly linked to identity)

**Privacy floor:** Demographic data is always voluntary. It is encrypted at rest, stored
separately from review activity data, and subject to right-to-erasure. It is used only to
determine which review dimensions a reviewer can contribute to. It is never published
individually or used to identify a reviewer.

---

### Component 2: Training and Credentialing

Reviewers complete training modules to unlock specific review dimensions:

| Dimension | Training required |
|---|---|
| Policy rigor | Policy process, legal framework, evidence standards |
| Research quality | Source evaluation, data literacy |
| Lived experience | Accessible self-attestation (no formal assessment) |
| Clarity and accessibility | Plain language standards, WCAG awareness |

**Lived-experience pathway:** Training friction must not systematically exclude time-poor,
lower-formal-education, or disability-affected reviewers. The lived-experience dimension
unlocks via accessible self-attestation (specific domain + affirmation), not a formal
module. This is intentional and reflects a core equity commitment.

**Bot detection integration:** Training modules enforce minimum realistic completion times.
Copy-paste patterns in written assessments are flagged as a bot signal.

---

### Component 3: Weighting Engine

Review contributions are weighted per dimension, not by global reviewer reputation.

```
WEIGHT CALCULATION (per dimension, per review)

reviewer_dimension_weight =
    base_weight (calibration score for this dimension)
  * domain_factor (calibration score specific to this policy domain)
  * trust_score (from Signal Integrity Layer, 0.0 - 1.0)
  * recency_decay (weight decreases if reviewer has been inactive)

aggregate_score (per dimension) =
    sum(review_score * reviewer_dimension_weight)
  / sum(reviewer_dimension_weight)
```

**Fraud detection metrics (not weighting inputs):**
Global acceptance rate and total review count are tracked for fraud and bot detection
purposes only. They do not factor into review weighting. The "weight dimensions, not
people" principle is not violated by operational monitoring.

**Open design question:** The specific initialization values, increment and decay rates,
and aggregation thresholds are not decided here. This is the primary pre-spec requirement
blocking the formal schema design.

---

### Component 4: Assignment and Routing

Review assignments use a hybrid of sortition (randomness) and profile matching.

```
ASSIGNMENT FLOW

New review task created for policy position P
    |
    v
Eligible reviewer pool =
    (has relevant training) AND (trust score >= threshold) AND
    (has not previously reviewed P) AND (no conflict of interest)
    |
    v
Split:
    ~60-70% profile-matched (highest dimension weight for P's domain)
    ~30-40% sortition (random draw from eligible pool)
    |
    v
Assignment queue
```

The sortition percentage is a design parameter to be decided during Stage 1 scoping.
The exact split affects capture resistance versus review quality and needs calibration.

---

### Component 5: Review Criteria Engine

Each review evaluates a policy position on dimensions appropriate to its type.

**Core dimensions:**
- **Policy rigor:** Is the rule technically sound? Does it achieve its stated goal?
- **Research quality:** Are claims supported by the cited sources? Are sources current and credible?
- **Lived experience alignment:** Does this position reflect the reality of affected people?
- **Clarity and accessibility:** Is the plain-language version accurate? Is the formal rule understandable?
- **Scope accuracy:** Does the position do what it says -- no more and no less?

Dimension availability for a given reviewer depends on their completed training
(see Component 2).

---

### Component 6: Aggregation and Change Pipeline

```
PROCESSING FLOW

Reviews accumulate for position P
    |
    v
Coverage check:
    (minimum reviewer count met?) AND (minimum aggregate weight threshold met?)
    |
    NO  -> continue accumulating
    YES -> trigger aggregation run
    |
    v
Weighted score computed per dimension
    |
    v
Change recommendation generated:
    AFFIRM / REVISE (with specific feedback) / ESCALATE / WITHDRAW
    |
    v
Maintainer review
    |
    v
Implementation  OR  Layer-1 block (public, reasoned, appealable)
```

Processing thresholds (minimum reviewer count, minimum aggregate weight) are
pre-spec design parameters.

---

### Component 7: Moderation

The moderation system handles:

- Review content moderation (e.g., abusive or bad-faith submissions)
- Signal Integrity escalations (accounts queued for human review)
- Conflict of interest disclosures
- Coordinated bad-faith patterns (bulk organized rating, submission flooding)

Moderation decisions are logged to the audit log. Accounts are never silently downgraded.
Any action that affects an account's review weight is disclosed to the account owner.
The specific reason is not always disclosed if doing so would compromise anti-gaming
security, but the fact of the change is always communicated.

---

### Component 8: Appeals

Any account whose trust score is reduced, or whose submitted review is moderated,
may appeal. Appeals are reviewed by the Review Board (Component 9) or a designated
moderation panel. Appeal outcomes are logged to the audit log.

Appeal response SLAs are a pre-spec design parameter.

---

### Component 9: Governance / Review Board

The Review Board:

- Reviews escalated change recommendations (cases where the maintainer invokes a
  Layer-1 block)
- Reviews appeals from moderation decisions
- Periodically audits the weighting algorithm for systematic bias
- Oversees calibration corpus quality

Board composition, size, term length, and selection process are pre-spec design
parameters.

---

### Component 10: Anti-Capture Mechanisms

The system must resist organized actors attempting to dominate review outcomes.

| Mechanism | What it prevents |
|---|---|
| Sortition in assignment | Organized reviewer bloc controlling outcomes |
| Weighting recency decay | Capturing influence through training + dormancy |
| Subnet clustering detection | One organization running many accounts |
| Review submission velocity limits | Flooding a position with coordinated reviews |
| Calibration corpus comparison | Reviewers who systematically diverge from ground truth |
| Review Board rotation | Capture of the Review Board itself |

---

### Component 11: Audit Log

An immutable, append-only event log covering all materially significant system events:

- Every weighting decision (reviewer weight assigned to a review)
- Every aggregation run and its output
- Every change recommendation generated
- Every maintainer approval or Layer-1 block (with stated reason)
- Every trust score change (triggering signal category logged; identifying details not logged)
- Every moderation action
- Every appeal outcome

The audit log is queryable for aggregate statistics and will be published in aggregate
form as a platform transparency commitment. A data retention policy is a pre-spec
design parameter.

---

### Component 12: Signal Integrity Layer

Ensures review contributions reflect genuine U.S.-resident human judgment. Uses
probabilistic trust scoring, not binary geographic gates. No government ID or biometric
verification is used or planned.

**Account trust model:**

Each account starts with:
- `base_trust_score = 1.0`
- `scrutiny_level = normal`

**Signal taxonomy:**

*Geographic signals (U.S. residency inference):*
- IP geolocation (MaxMind GeoIP2 or equivalent commercial database)
- Browser timezone and locale (corroborating signal only; easily spoofed)
- Session activity time patterns (checks for U.S. timezone consistency over time)
- ASN type classification (residential vs. datacenter or VPN ASN)

*Anonymization detection:*
- Known VPN, proxy, and datacenter ASN lists
- Tor exit node lists
- IP reputation scoring (commercial provider)

*Multi-account / Sybil resistance:*
- Device fingerprint collisions across accounts
- IP and subnet clustering (multiple accounts sharing a /24)
- Throwaway email domain detection at registration

*Bot and automation detection:*
- Training completion too fast (minimum realistic time enforced per module)
- Review submission velocity above human-plausible rate
- Copy-paste similarity across accounts on the same position
- Absence of mouse and scroll events during training or review sessions

**Decision model:**

```
SCRUTINY STATE MACHINE

On account creation:
    VPN / datacenter / Tor signal present?
        YES -> scrutiny_level = elevated  (NO score change)
        NO  -> scrutiny_level = normal

On ongoing activity:
    elevated account + additional corroborating signals?
        YES -> review_queue (human moderator reviews)
        NO  -> stays elevated, score unchanged

    normal account accumulates additional signals?
        YES -> elevated -> same path as above

review_queue:
    human moderator confirms concern -> trust_score reduced, logged
    human moderator clears account   -> scrutiny_level = normal, logged
```

**Key design decisions:**

- **VPN alone carries zero score penalty.** VPN flags elevated scrutiny only.
  A score reduction requires multiple corroborating signals AND human confirmation.
  This protects users with legitimate privacy reasons for using VPNs.
- Flagged-but-not-actioned accounts are not notified of elevated status
  (telling users they are being watched enables gaming the system).
- Accounts whose weight is reduced are told their weight changed; specific
  trigger signals are not disclosed.

**Privacy commitment:** Device fingerprinting is scoped to fraud detection within the
review system only. It is never used for advertising, cross-site tracking, or any
purpose other than detecting multi-account fraud and bot activity. This will be stated
explicitly in the platform privacy policy.

**Pending:** Fingerprinting library selection requires a privacy policy review before
implementation. This is flagged as an R&D item.

---

## What Needs to Be Decided Before We Can Write the Spec

The following items must be resolved in design sessions before a formal specification
can be written. None are implementation tasks -- they are design decisions.

| # | What needs deciding | Why it's blocking |
|---|---|---|
| 1 | **Stage 1 scope** -- what ships first, what is deferred? | Drives all other sequencing. Nothing else can be properly designed without this. |
| 2 | **Sections data model** -- how are positions grouped into reviewable sections? | DB schema depends on this. Section is the unit of review, not individual positions. |
| 3 | **Weighting algorithm v1** -- concrete initialization values, increment and decay rates, aggregation thresholds | Needed to design the reviewer profile schema. |
| 4 | **PII architecture** -- storage model for demographic data, encryption, deletion and right-to-erasure flow | Required before any storage schema can be written. |
| 5 | **Cold-start strategy** -- which sections get reviews first, what are the bootstrapping rules, what is the minimum viable reviewer count? | The system cannot operate at launch without this. |
| 6 | **Signal integrity thresholds** -- which signals trigger elevated scrutiny? What is the multi-signal convergence rule for review_queue? | Needed to implement Component 12. |
| 7 | **Launch-day calibration corpus** -- who produces it, how many items per dimension and domain, how are items marked as ground truth? | Without a calibration corpus, the weighting engine cannot initialize. |
| 8 | **Lived-experience training pathway** -- accessible format for training materials, accessible alternative to formal assessment | Equity commitment requires this to be designed before the system goes live. |
| 9 | **Governance v1 amendment** -- formal text to amend or supersede the current maintainer-centric change process | The current governance document does not reflect the community-primary model described here. |

---

## Open Questions for Review Feedback

The following questions are genuinely unresolved. Input from reviewers is welcome.

- **Stage 1 scope:** What is the minimum viable version of this system? Which subsystems
  are essential from day one and which can be deferred?

- **Review Board:** How large should it be? How should members be selected? What term
  lengths prevent capture while maintaining continuity?

- **Sortition percentage:** What is the right balance between profile-matched assignments
  (expertise match) and sortition (capture resistance)? The 60/40 split above is a
  placeholder.

- **Weight decay function:** Should weight decay be linear, exponential, or a step
  function? How long before a dormant reviewer's weight resets?

- **Weighting calibration corpus:** How do we define "high quality" reviews for use as
  calibration ground truth? Who produces the initial corpus?

- **Non-U.S. residents:** The system targets U.S. residents for voting weight. Should
  non-U.S. participants be allowed to submit reviews with reduced or no weight, or
  excluded entirely?

- **Minor corrections exemption:** Should citation updates, typo fixes, and other
  non-substantive changes bypass the review process?

- **Meta-review:** Should reviewers be able to flag low-quality reviews for secondary
  review? (Noted as a partial anonymity problem -- deferred but worth discussion.)

---

## What Is Out of Scope

| Item | Reason |
|---|---|
| Government ID or biometric verification | Explicitly excluded by design |
| Voting on political opinions | This is a research and writing quality review, not a preference poll |
| Anonymous editing (Wikipedia model) | Requires accountability mechanisms the wiki model lacks |
| Relevance mapping (knowledge types to policy domains) | R&D item; not blocking Stage 1 |
| Portfolio or prior work submission for dimension test-out | Creates anonymity-breaking problem; deferred to R&D |
| Stage 2 and 3 architecture | Depends on Stage 1 definition and launch learnings |
| Per-subsystem implementation plans | Come after the spec is written and approved |

---

## Failure Modes to Address in the Spec

| Risk area | Failure | Current status |
|---|---|---|
| Weighting aggregation | Silent bug produces incorrect weights | No test, no handler -- critical gap |
| Sortition assignment | Non-random distribution due to bad RNG | No test, no handler |
| Launch-day calibration | No calibration corpus exists at launch | Unmitigated |
| Appeals | Reviewer cannot reconstruct what led to a trust score change | Partially covered by audit log; needs explicit decision |
| Coordinated capture | Organized actor pre-loads the reviewer pool before sortition | Anti-capture mechanisms partially cover this; thresholds needed |

---

## Relationship to Existing Infrastructure

| Existing asset | Role in this system |
|---|---|
| PolicyOS Platform Values (Layer 1) | Non-overridable floor; community consensus cannot breach it |
| PolicyOS Governance v1 | Must be amended or superseded; current model is maintainer-primary |
| `policy/catalog/policy_catalog_v2.sqlite` | The entities being reviewed; needs a `sections` table added |
| PolicyOS Authoring OS checklists | The quality criteria reviewers evaluate against |

---

## How to Give Feedback

This document is a design proposal, not a final spec. All sections are open for discussion.
The most valuable feedback addresses:

1. **The governance model** -- does the authority hierarchy make sense? Is the maintainer
   veto too narrow? Too broad?
2. **The weighting approach** -- is weighting by dimension (not by global reputation) the
   right model? What are the failure modes you see?
3. **Signal integrity** -- is the VPN-as-elevated-scrutiny (not penalty) decision sound?
   What signals are missing? What signals are too invasive?
4. **The pre-spec requirements table** -- are there items missing? Are any of the nine
   blockers actually solvable in a different order?
5. **The open questions** -- any of these are fair game for substantive input.

GitHub issues and pull request comments are the preferred channels.
Direct feedback to the author via GitHub: [@alistardust](https://github.com/alistardust)

---

*This is a design document. Nothing here has been implemented. The formal specification
(RVEW rule family) will be written after the pre-spec requirements above are resolved and
this design has been reviewed.*
