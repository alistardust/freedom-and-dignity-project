# Roadmap — American Renewal Project

> Where we are, what comes next, and the work still ahead — across policy development,
> organization, outreach, and technical infrastructure.

*Status as of April 2026.*

---

## Overview

The American Renewal Project is a living platform — built in the open, subject to revision,
and committed to intellectual honesty. This roadmap tracks six parallel work streams:
policy content, organizational formation, outreach, fundraising, branding, and technical
infrastructure.

---

## Track 1: Policy Development — 🟡 In Progress

### Overall status

| Item | Status |
|------|--------|
| 22 policy pillar HTML pages published | ✓ Done |
| Mission and Constitution pages complete | ✓ Done |
| Referendum & Recall policy added to Elections pillar | ✓ Done |
| Compare pages for major parties published | ✓ Done |
| 5 new pillars (Education, Labor, Housing, Consumer Rights, Legislative Reform) — markdown complete; DB reimport pending | ○ Pending |
| APA citations required across all policy pages | ○ Ongoing |
| Adversarial gap audit — systematic review of all 22 pillars by external reviewers | ◆ Planned |
| Constitutional amendment classification for all rules | ◆ Planned |

To reimport the catalog after source changes:
```bash
python scripts/import_policy_catalog.py
```

### Pillar completion status

Status key: **High** = 50+ rules · **Medium** = 10–49 rules · **Low** = <10 rules · **DB Rebuild** = 0 in DB, markdown pending import

| # | Pillar | Rules (DB) | Status | Notes |
|---|--------|-----------|--------|-------|
| 1 | Executive Power | 13 | Medium | GOV in DB; EXE rules in markdown pending reimport |
| 2 | Elections & Representation | 22 | Medium | Well-developed; referendum & recall added |
| 3 | Anti-Corruption | 15 | Medium | |
| 4 | Equal Justice & Policing | 136 | **High** | Very developed — JUS scope |
| 5 | Rights & Civil Liberties | 26 | Medium | |
| 6 | Courts & Judicial System | 8 | Low | Needs expansion |
| 7 | Checks & Balances | 52 | **High** | SYS + OVR scope codes |
| 8 | Taxation & Wealth | 10 | Medium | ECO in DB; TAX rules in markdown pending reimport |
| 9 | Healthcare | 184 | **High** | Very developed — HLT scope |
| 10 | Antitrust & Corporate Power | 4+ | Low | Cross-scope (COR-FIN, MED); needs expansion |
| 11 | Information & Media | 20 | Medium | MED + INF scope codes |
| 12 | Gun Policy | 2+ | Low | No GUN- scope yet; cross-scope JUS-POL rules only; needs expansion |
| 13 | Term Limits & Fitness | 8 | Low | TRM scope |
| 14 | Administrative State | 3 | Low | ADM scope; needs expansion |
| 15 | Technology & AI | 361 | **High** | Very developed — TEC scope; PAT rules in markdown pending reimport |
| 16 | Immigration | 222 | **High** | Very developed — IMM scope |
| 17 | Environment & Agriculture | 10 | Medium | ENV + AGR in DB; EWT pending reimport |
| 18 | Education | 2 | Low | DB pre-expansion; markdown has significantly more, pending reimport |
| 19 | Labor & Workers' Rights | 3 | Low | DB pre-expansion; markdown has significantly more, pending reimport |
| 20 | Housing | 0 | **DB Rebuild** | Markdown content complete; DB reimport pending |
| 21 | Consumer Rights | 0 | **DB Rebuild** | Markdown content complete; DB reimport pending |
| 22 | Legislative Reform | 0 | **DB Rebuild** | Markdown content complete; DB reimport pending |

**Total (DB, pre-expansion state):** 1,095 rules across 20 scope codes.

---

## Track 2: Organization — ⚪ Not Started

- ○ Formal legal establishment — 501(c)(4) or similar nonprofit structure
- ○ Board structure and bylaws
- ○ Engage legal counsel
- ○ File for tax-exempt status
- ○ Establish fiscal sponsorship as interim structure if needed

---

## Track 3: Outreach & Advocacy — ⚪ Not Started

- ○ Platform packaging: 1-pager, 5-pager, FAQ, video script, social media versions
- ○ Coalition building: identify and approach aligned organizations
- ○ Speaker and presentation strategy
- ○ Social media presence — handle registration and content calendar
- ○ Press kit
- ○ Petition drives — especially for referendum/recall constitutional amendment advocacy

---

## Track 4: Fundraising — ⚪ Not Started

- ○ Small-dollar online fundraising infrastructure — ActBlue or equivalent
- ○ Grant research — progressive foundations: NEO Philanthropy, Democracy Fund, and others
- ○ Major donor outreach strategy
- ○ Crowdfunding for specific projects

---

## Track 5: Content & Branding — 🟡 In Progress

- ○ Replace AI-generated branding assets with human-designed equivalents — logo, color system, typography
- ○ Human review and rewrite of all policy language — ongoing
- ○ Professional copyediting of all pages
- ○ Accessibility audit — WCAG 2.1 AA compliance
- ◆ Video explainer series (planned)

---

## Track 6: Technical — 🟡 In Progress

- ✓ Version control and provenance tracking in place
- ○ Complete E2E test suite — Playwright + Vitest — ongoing
- ○ Regular adversarial review cycles
- ○ Regular policy catalog rebuilds from source (`scripts/import_policy_catalog.py`)
- ○ DB reimport for 5 new pillars — pending
- ○ Mobile/responsive QA — ongoing

---

*Legend: ✓ Done · ○ Pending/Ongoing · ◆ Planned*
