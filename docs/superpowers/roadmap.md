# Freedom and Dignity Project — Work Tracker

_Last updated: 2026-05-10 (HTML build system brainstorm complete; spec review in progress). Update this file when epics open, close, or shift priority._
_GitHub Issues are the ticketing system. This doc is the human-readable summary layer._
_Issue links: https://github.com/alistardust/freedom-and-dignity-project/issues_

---

## How this works

Each epic below has a corresponding GitHub issue. This file tracks status at the epic level.
For task-level detail, follow the issue link or read the linked spec/plan file.

GitHub Issues: https://github.com/alistardust/freedom-and-dignity-project/issues

**Status key:** `active` | `blocked` | `not started` | `done` | `tabled`

---

## Epics

### 1. HTML Build System (Nunjucks)
**Status:** implementation complete — pending GH Pages source switch and visual baseline CI run
**GitHub issue:** [#1](https://github.com/alistardust/freedom-and-dignity-project/issues/1)
**Spec:** `docs/superpowers/specs/2026-05-08-html-build-system-design.md`
**Plan:** `docs/superpowers/plans/2026-05-10-html-build-system.md`

Migrated 47 hand-authored HTML pages to a Nunjucks base template with a canonical shell
(nav, head, footer). Phase 1 complete — pillar card content unchanged. CI workflow added.

**Remaining:** (1) Switch GH Pages source to GitHub Actions in repo settings. (2) Trigger
`workflow_dispatch` with `update_snapshots=true` to generate visual baselines; commit artifact.

---

### 2. Data Rights and Privacy Pillar
**Status:** active — spec done, plan not written
**GitHub issue:** [#2](https://github.com/alistardust/freedom-and-dignity-project/issues/2)
**Spec:** `docs/superpowers/specs/2026-05-08-data-rights-privacy-pillar-design.md`
**Research:** `policy/research/surveillance-capitalism/`, `policy/research/surveillance-pricing/`
**Plan:** not yet written

New pillar in the Real Freedom foundation. Domain code `PRIV`. Six policy families, 34
positions. Covers data broker regulation, ad-tech, behavioral manipulation, surveillance
pricing, biometric data, and children's data. Design approved by Ali.

**Next action:** Write implementation plan, then implement (DB inserts, HTML page, data.js).

---

### 3. ESRP Research Project — Phase 1
**Status:** active — tracking separately (likely moving to its own repository)
**GitHub issue:** n/a — will track in ESRP repo
**Spec:** `docs/superpowers/specs/2026-05-04-esrp-charter-design.md`
**Plan:** `docs/superpowers/plans/2026-05-05-esrp-phase-1.md`
**Handoff:** `policy/research/esrp/handoff-2026-05-08.md`

Economic Systems Research Project. Task 1 (workspace init: README, templates, directories)
is complete and committed. Tasks 2-6 are research outputs: values mapping, techno-georgism
memo, mechanism catalog entries.

**Next action:** Task 2 — write `policy/research/esrp/platform-values-mapping.md` (map
ESRP research questions to PolicyOS obligations; read PLOS-ECON-0001-0004 and Values 2, 3,
7, 11 first).

---

### 4. Policy Card Audit
**Status:** not started
**GitHub issue:** [#3](https://github.com/alistardust/freedom-and-dignity-project/issues/3)
**Plan:** `docs/superpowers/plans/2026-05-02-policy-audit-card-completion.md`

Promote all `status-missing` cards to `status-included` by adding `rule-notes` (research
basis, legal citations, adversarial review) to each card. Per PAOS-TEST-0008: every card
must document gaps, loopholes, unintended consequences, and abuse paths before promotion.

Priority order (P1 first, smallest gap pillars first within tier):

| Priority | Pillar | Missing |
|---|---|---|
| P1 | term-limits-and-fitness | 19 |
| P1 | gun-policy | 30 |
| P1 | science-technology-space | 38 |
| P1 | foreign-policy | 50 |
| P1 | equal-justice-and-policing | 143 |
| P1 | immigration | 225 |
| P1 | healthcare | 254 |
| P1 | technology-and-ai | 386 |
| P2 | anti-corruption, courts, media, infrastructure, checks-and-balances, rights, legislative-reform, elections | ~226 |
| P3 | admin-state, environment, executive-power, taxation, antitrust, consumer-rights, labor, housing, education | ~169 |

**Next action:** Start with term-limits-and-fitness (smallest P1 pillar, 19 cards).

---

### 5. Site Identity and Restructure
**Status:** not started (spec written; implementation unknown)
**GitHub issue:** [#4](https://github.com/alistardust/freedom-and-dignity-project/issues/4)
**Spec:** `docs/superpowers/specs/2026-05-01-site-identity-alignment-design.md`
**Strategic doc:** `ROADMAP.md`

Reframe the site from policy library to reform movement. North star: "I know exactly where
I fit in and what I can do." Five sub-projects: Identity & Voice (done), Movement Layer,
Site Restructure, Content Coherency, Accessibility.

**Next action:** Audit what (if anything) from the spec was actually implemented, then
write an implementation plan for the remaining sub-projects.

---

### 6. Human Review System
**Status:** concept — Ali designing the system
**GitHub issue:** [#5](https://github.com/alistardust/freedom-and-dignity-project/issues/5)

Design and build a system for tracking editorial flags that require human review. Covers
[VERIFY] markers (788 across 24 pillar files), orphan footnotes (9 files), and any other
flags left by audit agents.

Items currently awaiting the system (will migrate into it once built):

| Item | Location | Notes |
|---|---|---|
| [VERIFY] markers | 24 pillar HTML files (788 total) | Uncertain legal thresholds left by audit agents |
| Orphan footnotes | immigration, technology-and-ai, consumer-rights, courts, elections, environment, gun-policy, legislative-reform, term-limits | Footnotes defined but never cited inline |
| New Bill of Rights adversarial review | `policy/research/new-bill-of-rights-adversarial-review.md` | 15 issues, some critical (standing, enforcement, horizontal application) |
| Senate reform research verification | `policy/research/senate-reform-research.md` | Calculated figures flagged for primary source check |
| New Bill of Rights naming | — | Decision still open: *A New Bill of Rights* vs. *The People's Bill of Rights* vs. *The Freedom and Dignity Bill of Rights* |
| Policy card ID full audit | all pillar HTML files | No systematic duplicate/format check done yet |

**Next action:** Design session to define the system architecture and workflow.

---

### 7. Small Fixes and Loose Ends
**Status:** active
**GitHub issue:** [#6](https://github.com/alistardust/freedom-and-dignity-project/issues/6)

| Item | File | Notes |
|---|---|---|
| Push 7 unpushed commits | — | Commits `5c944f3`–`df41a15` ahead of origin/main |
| foreign-policy.html data.js TODO | `docs/pillars/foreign-policy.html` | `<!-- TODO: add to data.js -->` for foundation field |
| CONTRIBUTING.md expansion | `CONTRIBUTING.md` | PR workflow, branch naming, Discord link, non-technical onboarding |
| Compare pages missing foreign policy | `docs/compare/*.html` | Strengths/weaknesses sections don't discuss foreign policy |
| Related-pillar sections missing foreign policy | other pillar pages | Foreign policy not referenced in related pillars of other pillars |

---

## Tabled

| Item | File | Reason |
|---|---|---|
| "Why These Problems Persist" page | `tmp/why-problems-persist-page-plan.md` | Tabled 2026-05-01; revisit after Identity/Movement/Site Restructure |
| Site consistency audit | `tmp/site-consistency-audit-plan.md` | May be superseded by site restructure work |

---

## Completed (recent)

| Item | Commit(s) | Date |
|---|---|---|
| BNPL policy family (9 cards, CNSR-PDLS-0007 retired) | — | 2026-05 |
| PolicyOS site exposure (policyos.html, DB tables, data.js sentinels, overlay injection) | `9bdfe43`–`5c944f3` | 2026-05 |
| Surveillance capitalism + pricing research | `355531f`, `c7bc3eb` | 2026-05 |
| ESRP workspace initialized | `00f037c` | 2026-05-08 |
| HTML build system spec written and reviewed | `716c930`–`5af121d` | 2026-05-08 |
| Data Rights and Privacy spec written and reviewed | `beab87e`–`0aec947` | 2026-05-08 |
| PolicyOS canonicalization (3 layers locked) | — | 2026-04-27 |
| Full policy card audit + gap remediation (+179 positions) | — | 2026-04-27 |
