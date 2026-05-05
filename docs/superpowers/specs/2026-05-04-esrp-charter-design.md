# ESRP Charter v0.1
## Economic Systems Research Project

**Date:** 2026-05-04
**Status:** v0.1 — working document, internal
**Author:** Alice Thomas

---

## Purpose of this document

This charter defines the Economic Systems Research Project (ESRP): what it is, what it is not,
how it relates to the Freedom and Dignity Project, what it will research, how it will do that
research, and what the first phase of work looks like.

This is a working document. It is written for Alice and future contributors, not for funders or
public audiences. Those versions come later. This version is for getting the project on solid
footing before it is explained to anyone else.

---

## 1. Mission and Purpose

The Economic Systems Research Project (ESRP) is a research sub-project of the Freedom and
Dignity Project. Its purpose is to design and validate economic system architectures that
fulfill the platform's core values: distributing the gains of technological change broadly,
preventing economic domination, and securing material well-being as a precondition of real
freedom.

ESRP is not a policy advocacy shop, a think tank, or a political organization. It is a research
program. It produces evidence, mechanism catalogs, system designs, and simulation-validated
proposals. The advocacy, the narrative, and the movement work belong to the main platform.
ESRP's job is to ensure the main platform's economic proposals have intellectual infrastructure
underneath them — the kind that makes demands defensible and transition pathways real.

---

## 2. Relationship to the Freedom and Dignity Project

ESRP is subordinate to the main platform but operationally distinct.

**The main platform provides:**
- Values framework (PolicyOS)
- Voice and theory of change
- Governance and citation standards
- Contributor community

**ESRP provides:**
- Rigorously researched economic mechanism catalog
- Techno-georgism as a new intellectual contribution
- Candidate system architectures evaluated against platform values
- Simulation-validated proposals

**ESRP outputs feed into:**
- Updates to existing pillars (Taxation & Wealth, Labor, Consumer Rights, Housing)
- New pillar proposals
- Supplements to the rights frameworks

ESRP does not maintain its own governance, recruit independently, or operate outside the
platform's standards. When the platform's contributor recruitment infrastructure (Roadmap
stages 03–04) activates, ESRP contributor roles are recruited through it, not in parallel.

**Repository structure:**
ESRP operates in a dedicated repository (`esrp`, under the same GitHub account as the main
platform). This is a requirement, not a preference. ESRP outputs — research memos, mechanism
catalog, adversarial review logs, eventually code and data — are research artifacts with
different lifecycle and structure than policy cards. This charter and the connection to PolicyOS
live in the main platform repository. All ESRP research outputs live in the ESRP repository.
The two repositories are explicit siblings: this charter links to the ESRP repo; the ESRP repo
README links back to the main platform and PolicyOS.

---

## 3. Scope and Boundaries

**In scope:**
- Economic mechanism research: what has worked, where, under what conditions, and why
- Techno-georgism: applying rent-capture logic to digital economies, AI training data, network
  effects, attention, spectrum, and platform infrastructure
- System design: synthesizing mechanisms into candidate architectures evaluated against platform
  values
- Transition pathway research: what changes can happen at city, state, and federal level vs.
  constitutional amendment
- Simulation of proposed architectures where resources allow

**Out of scope:**
- Near-term electoral or legislative strategy — that belongs to the main platform
- Macroeconomic forecasting
- International economic policy beyond what is needed for transition analysis
- Building a political or fundraising organization

---

## 4. Values Alignment

ESRP operates under the PolicyOS framework. The relevant overlays and values are not background
reading — they are active constraints that shape which research questions are worth asking and
which proposed mechanisms pass review.

**Primary PolicyOS overlays:**

`PLOS-ECON-0001–0004` (economic domination overlay) — the system-level constraints ESRP
research must satisfy. Any proposed mechanism or system architecture that would permit or
entrench the conditions ECON describes is a design failure, regardless of other merits.
ECON-0002 is especially operative: where a sector denies the practical ability to refuse,
negotiate, or exit, structural remedies are required — disclosure and transparency requirements
alone are not structural remedies.

`PLOS-THRV` (material security overlay) — the affirmative provision requirement. Research must
address not just how to prevent extraction but how to actively secure material well-being. A
duty declared without a funding mechanism and institutional structure is hollow.

**Platform values directly operative:**

- **Value 7 — Material security:** ESRP designs must specify how provisions are actually
  resourced, not just declared.
- **Value 2 — Equal standing:** Proposed systems must not create unequal classes or practical
  denial of equal access — including across geography, class, and credential.
- **Value 3 — Real liberty:** Economic domination by private actors is a liberty violation,
  not just an inequality problem. This reframes the research scope.
- **Value 11 — Durability against capture:** Systems must resist bad actors, drift, and
  loophole exploitation from the design stage. This is an engineering requirement, not an
  afterthought.

---

## 5. Research Questions by Workstream

### Workstream A — Diagnostic Research

Document current system failures with evidence; map the structural mechanisms of economic
domination; identify pressure points and crisis vectors.

Initial questions:
- What mechanisms of economic domination are most structurally embedded in the current U.S.
  economy, and which are most amenable to disruption?
- How does AI-driven labor displacement interact with payroll-tax-funded social programs, and
  at what displacement rates do current systems become structurally insolvent?
- What are the specific mechanisms by which extreme wealth concentration translates into
  political and regulatory capture?

### Workstream B — Mechanism Research

Build a catalog of economic mechanisms: what has worked, where, under what institutional
conditions, and with what failure modes.

Initial questions:
- What mechanisms demonstrably reduce wealth concentration while preserving productive
  dynamism — and under what conditions?
- What are the necessary conditions for land value taxation to function at scale in urban and
  rural contexts?
- What mechanisms have been successfully tested at city or state level and are candidates for
  scaling?
- What are the failure modes of each mechanism when transplanted across institutional contexts?

### Workstream B (sub) — Techno-Georgism *(distinctive contribution)*

Classical Georgism holds that value created by the community — not by the individual who
happens to capture it — should be taxed back for collective benefit. This workstream extends
that logic to the digital economy, where the same dynamic recurs in new forms. This is ESRP's
most original intellectual contribution and a largely unoccupied research domain.

Categories under investigation:

| Category | Description |
|---|---|
| Data rent | Aggregated personal data generates value far exceeding individual contribution; the surplus is privately captured |
| Network effect rent | Platform value derives from network participation the platform did not create |
| AI training rent | Foundation model value derives from collectively-produced training data; a few actors capture it as private infrastructure |
| Attention rent | Human cognitive capacity is finite; platforms extract and sell it |
| Knowledge rent | Patents and copyright on publicly-funded research create artificial scarcity over commons |
| Computational infrastructure rent | Platform chokepoints built on public infrastructure extract rent from dependent participants |

Initial research questions:
- How should socially-produced value in digital economies be identified, measured, and captured
  for collective benefit?
- How do digital rents differ from classical land rent in ways that matter for mechanism design?
- What is the appropriate policy design for AI training data — one-time levy, ongoing usage
  tax, public option for foundation models, or combination?
- Can data be treated as labor (Weyl) vs. as commons (Lanier), and what follows for mechanism
  design in each case?
- How does digital capital mobility differ from physical capital mobility, and what does that
  mean for international coordination and evasion?

Key thinkers and works to engage: Henry George (*Progress and Poverty*); Glen Weyl and Eric
Posner (*Radical Markets*); Jaron Lanier (data dignity); Mariana Mazzucato (*The Value of
Everything*, *The Entrepreneurial State*); Yanis Varoufakis (*Technofeudalism*); Lincoln
Institute of Land Policy (LVT research).

### Workstream C — System Design

Synthesize mechanisms into candidate system architectures; evaluate against platform values;
identify incompatibilities and second-order effects.

Initial questions:
- What combinations of mechanisms produce candidate systems that satisfy all platform values
  simultaneously?
- What incompatibilities exist between mechanisms that work individually but conflict in
  combination?
- What are the second-order effects of proposed architectures on innovation, investment, and
  productive dynamism?

### Workstream D — Transition Strategy

How to get from here to there — at city, state, federal, and constitutional levels. The part
most utopian system designs neglect.

Initial questions:
- What transition pathways exist from current institutions to proposed architectures, and at
  what pace are they realistic?
- What changes can happen at city/state level vs. requiring federal legislation vs.
  constitutional amendment?
- What are the historical precedents for successful non-violent comprehensive economic
  restructuring, and what conditions enabled them?

### Workstream E — Platform Connection

Workstream E is not a research workstream. It is the connection point between ESRP's outputs
and the main platform's movement work. ESRP's contribution is producing intellectual
infrastructure specific and defensible enough to become political demands. The advocacy,
narrative, and organizing belong to the main platform. ESRP feeds it; ESRP does not do it.

---

## 6. Methodology

### The research pipeline

```
Diagnostic Research
       ↓
Mechanism Catalog  ←──────────────────┐
       ↓                              │
System Design                         │
       ↓                    Continuous adversarial
Simulation                   review loop at every
       ↓                         stage (below)
Validated Proposals
```

These stages overlap and feed each other. Nothing moves forward without adversarial review.

### Evidence standards

- Primary sources first: empirical research, natural experiments, historical record, government
  data
- Peer-reviewed academic research
- All factual claims cited to APA 7th edition, consistent with platform standards
- All proposed mechanisms must pass adversarial review before entering the catalog as validated
- Simulation outputs are hypotheses requiring real-world validation, not results

### Adversarial review — continuous loop

Adversarial review runs on every substantive output before that output is treated as a research
finding: mechanism catalog entries, research memos, system design proposals, simulation
assumptions.

**The review cycle:**

1. Draft produced
2. Submitted to multiple AI models with an explicit adversarial prompt: *identify the strongest
   objections from a mainstream economics perspective; identify the strongest objections from a
   free-market perspective; identify failure modes or unintended consequences the author may
   have missed; identify empirical claims requiring stronger evidence; identify logical gaps or
   inconsistencies*
3. Responses from each model collected, read, and synthesized
4. Revisions made — or objections documented with explicit reasoning for why they were not
   addressed
5. Review log updated: date, document reviewed, models used, objections raised, how each was
   addressed

The review log is the auditable record. "AI reviewed this" is not documentation. A log entry
that names the models, the prompt, the objections raised, and how each was handled — that is
documentation.

As human contributors join, they participate in the same cycle. Contributors with different
priors than the author are specifically valuable as reviewers. The multi-model AI review
simulates perspective diversity; human reviewers provide it for real.

### Mechanism catalog entry structure

Each validated catalog entry contains:

| Field | Description |
|---|---|
| Name | Mechanism name |
| Description | What it does |
| Values alignment | Which platform values it serves; which PolicyOS overlay rules it satisfies |
| Evidence | Where tried, outcomes, primary sources cited |
| Conditions | What institutional context is necessary |
| Failure modes | Documented failure cases and why they failed |
| Incompatibilities | Mechanisms it conflicts with in combination |
| Adversarial review log | Date, reviewers, objections raised, how addressed |
| Status | `draft` / `reviewed` / `validated` |

### Tools

| Purpose | Tool |
|---|---|
| Literature synthesis and adversarial review | Claude, GPT-4o (or equivalent), Gemini |
| Academic literature search | Elicit, Semantic Scholar |
| Citation management | Zotero |
| Knowledge management | Obsidian (local), GitHub (`esrp` repo) |
| Version control | Git / GitHub |
| Data analysis (Phase 2+) | Python (pandas, numpy), R |
| Agent-based simulation (Phase 4–5) | Mesa (Python) |
| System dynamics modeling (Phase 4–5) | Vensim or equivalent |

### Open methodology

All ESRP outputs are open-access. Data and code are published alongside findings. Working
papers are published before formal submission where feasible. Reproducibility and transparency
are what make ESRP outputs usable by the contributor community and credible to external
reviewers.

---

## 7. Phases

Phase 1 is the only phase with specifics. Phases 2–5 are planning horizons, not commitments.
They will be revised when Phase 1 completes and contributor capacity is clearer.

**Current team capacity:**
- Alice: director, 10–20 hrs/week
- First contributor: research and synthesis, 5–15 hrs/week
- Combined with AI assistance: 15–35 effective research hours/week

At this capacity, first meaningful outputs are achievable in 2–4 months. Phase 1 complete:
6–10 months.

| Phase | Focus | Rough horizon | Gate condition |
|---|---|---|---|
| 1 | Foundation — first outputs, research infrastructure | Months 1–10 | Current team, AI-assisted |
| 2 | Evidence base — comprehensive mechanism catalog, diagnostic research | Months 6–24 | Overlapping with Phase 1; requires 2–3 active contributors |
| 3 | Catalog complete — adversarial review finalized, peer engagement | Months 18–36 | Requires human reviewers with different priors |
| 4 | System design — candidate architectures | Months 24–48 | Requires domain expertise; likely first advisor |
| 5 | Simulation — validate and publish | Month 36+ | Requires computational resources and methodology expertise |

**What Phase 1 does not attempt:** governance structures, legal entity, formal funding
applications, formal recruitment beyond the first contributor. Attempting those now burns
capacity that should go to producing the first research outputs.

---

## 8. Team and Roles

### Current team

**Alice Thomas — Director and Founder**
Part-time, 10–20 hrs/week. Systems and engineering background. Responsible for values
alignment, research direction, adversarial review synthesis, all commits, and quality
judgments. Will hand off the director role when a more qualified research director is
identified and recruited, while remaining involved in the project.

**First Contributor — Research and Synthesis**
Part-time, 5–15 hrs/week. Domain expertise in land use, regenerative agriculture, and
ecological economics. Primary focus: classical Georgism research, mechanism catalog entries
in land use and food systems economics, literature synthesis. Git-capable; no advanced
technical requirements for Phase 1.

### Contributor onboarding pathway

The first task for any new contributor is structured, achievable, connected to their existing
knowledge, and produces a real output:

1. Read the platform values document and this charter
2. Read the Taxation and Wealth pillar design logic for economic context
3. Produce a research memo on a specific mechanism drawn from the contributor's existing domain
   knowledge, following the mechanism catalog entry template
4. Submit for adversarial review cycle
5. Revise and commit

The first output goes directly into the mechanism catalog. Early wins matter for confidence
and for demonstrating that the project produces real outputs.

### Roles needed as project scales

| Role | Priority | Purpose |
|---|---|---|
| Senior research advisor | First when recruiting opens | Methodology guidance, legitimacy, recruitment support |
| Research methodologist | Second | Formal methodology design; quantitative/mixed-methods experience |
| Adversarial reviewer with different priors | Early | Built-in skepticism; ideally economist with different ideological starting point |
| Operations / PM | Later | Project management, recruitment coordination; Alice fills this initially |

Recruitment happens through the main platform's contributor infrastructure (Roadmap stages
03–04), not through a parallel ESRP process.

---

## 9. Honest Unknowns and Risks

This section exists because the project's credibility depends on being honest about what it
does not know. The discipline of being willing to be wrong is what separates a research
project from an ideological project.

### What we genuinely don't know

- Whether the techno-georgism research questions can be operationalized rigorously enough to
  produce defensible policy proposals — or whether they remain conceptually interesting but
  methodologically intractable
- Whether simulation is feasible at the resource levels ESRP will realistically reach, or
  whether the research stops at system design
- The timeline and scale of AI-driven labor displacement — the anchor crisis framing is
  calibrated to the direction being clear, not the timing
- Whether ESRP can recruit credentialed economists willing to engage seriously with a
  non-academic research project

### Risks

**Ideological capture** — the highest internal risk. The project starts with a hypothesis.
Research that confirms the hypothesis without seriously testing it is not research. Every
mechanism entry must include failure modes. Every system design must survive adversarial review
from perspectives the author disagrees with. If the evidence leads somewhere unexpected, the
project follows.

**Key-person dependency** — Alice is currently the only person who can commit, make quality
judgments, and maintain continuity. Mitigation: document everything; maintain the repo so a
future contributor can orient themselves from the record alone.

**Scope creep into advocacy** — ESRP is a research project. The advocacy, narrative, and
organizing belong to the main platform. This boundary must be maintained actively as the main
platform grows.

**Future donor capture** — not a current risk, but worth designing against now. Open-access
outputs, documented methodology, and public adversarial review logs make capture harder
regardless of who funds the project later.

**Burnout** — two part-time contributors working on a multi-year research project. Phase 1
scope is calibrated deliberately to produce real outputs before fatigue sets in.

---

## 10. First Deliverables (Phase 1, months 1–6)

These are the outputs that prove Phase 1 is real.

| Deliverable | Owner | Description |
|---|---|---|
| ESRP Charter v0.1 | Alice | This document |
| ESRP repository | Alice | `esrp` repo initialized; README with platform cross-reference; mechanism catalog template committed |
| Techno-georgism research memo | Alice | Literature review of key thinkers; identification of open research questions; proposed research agenda (~15–20 pages) |
| Mechanism catalog: land value tax implementations | First contributor | Research memo covering real-world LVT cases — where it worked, where it failed, what conditions mattered; first validated catalog entry |
| Mechanism catalog: 5–10 additional entries | Alice + contributor | Initial entries across workstreams A and B; each following the catalog template; each through the adversarial review loop |
| Platform values mapping | Alice | One-page document mapping ESRP research questions to PolicyOS obligations (ECON-0001–0004, THRV; Values 2, 3, 7, 11) |

The LVT mechanism catalog entry is specifically the first contributor's first task. It is
achievable, draws directly on her domain knowledge, follows a defined template, and produces
a real research artifact she can point to.

---

*ESRP Charter v0.1 — internal working document — 2026-05-04*
