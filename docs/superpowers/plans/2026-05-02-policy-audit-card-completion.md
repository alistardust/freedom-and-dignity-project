# Policy Audit — Card Completion Plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan.

**Goal:** Promote all `status-missing` policy cards to `status-included` by adding detailed, research-backed `rule-notes`, sharpening generic titles, and applying adversarial review to each card.

**Architecture:** Each missing card already has `rule-title`, `rule-plain`, and `rule-stmt`. The work is: (1) research legal/policy basis, (2) write `rule-notes`, (3) adversarial review (gaps, loopholes, failure modes), (4) sharpen title if generic, (5) change class and badge to `status-included`. Commit per pillar.

**Tech Stack:** HTML pillar files in `docs/pillars/`. PolicyOS framework in `policy/policyos/`. No build step — edit HTML directly.

---

## Card Format Reference

A complete `status-included` card looks like this:

```html
<div class="policy-card status-included" id="XXXX-YYYY-0000">
<div class="rule-header">
<code class="rule-id">XXXX-YYYY-0000</code>
<span class="rule-badge">Included</span>
</div>
<p class="rule-title">Specific, descriptive title in plain language</p>
<p class="rule-plain">1–3 sentences, ~8th grade reading level. What does this do and why does it matter?</p>
<p class="rule-stmt">Formal policy statement with precise language, thresholds, and enforcement detail.</p>
<p class="rule-notes">Research-backed rationale: legal basis (statutes, case law), empirical evidence, enforcement mechanisms, implementation notes, and adversarial review findings (gaps addressed, loopholes closed, failure modes considered).</p>
</div>
```

A `status-missing` card differs only in:
- `class="policy-card status-missing"` → change to `status-included`
- `<span class="rule-badge">Proposed</span>` → change to `Included`
- Missing `<p class="rule-notes">` → add it

---

## Adversarial Review Requirement (PAOS-TEST-0008)

For EVERY card, before marking included, document in `rule-notes`:
- **Gaps**: what the rule fails to cover
- **Loopholes**: how a bad-faith actor could comply technically while defeating the rule's purpose
- **Unintended consequences**: perverse incentives, burden-shifting, second-order harms
- **Abuse paths**: how government, employers, or institutions could exploit the rule

If no issues found, state that the review was conducted.

---

## Pillar Priority Order

Ranked by gap severity (missing / total):

| Priority | Pillar | Missing | Total | Gap% |
|---|---|---|---|---|
| P1 | term-limits-and-fitness | 19 | 23 | 83% |
| P1 | immigration | 225 | 268 | 84% |
| P1 | technology-and-ai | 386 | 502 | 77% |
| P1 | healthcare | 254 | 336 | 76% |
| P1 | gun-policy | 30 | 47 | 64% |
| P1 | science-technology-space | 38 | 62 | 61% |
| P1 | equal-justice-and-policing | 143 | 272 | 53% |
| P1 | foreign-policy | 50 | 99 | 51% |
| P2 | anti-corruption | 28 | 64 | 44% |
| P2 | courts-and-judicial-system | 26 | 62 | 42% |
| P2 | information-and-media | 22 | 58 | 38% |
| P2 | infrastructure-and-public-goods | 37 | 78 | 47% |
| P2 | checks-and-balances | 35 | 100 | 35% |
| P2 | rights-and-civil-liberties | 30 | 105 | 29% |
| P2 | legislative-reform | 16 | 62 | 26% |
| P2 | elections-and-representation | 22 | 65 | 34% |
| P3 | administrative-state | 20 | 88 | 23% |
| P3 | environment-and-agriculture | 28 | 176 | 16% |
| P3 | executive-power | 17 | 165 | 10% |
| P3 | taxation-and-wealth | 42 | 215 | 19% |
| P3 | antitrust-and-corporate-power | 11 | 150 | 7% |
| P3 | consumer-rights | 13 | 175 | 7% |
| P3 | labor-and-workers-rights | 18 | 237 | 8% |
| P3 | housing | 13 | 228 | 6% |
| P3 | education | 7 | 297 | 2% |

---

## Chunk 1: P1 Small Pillars — Term Limits & Gun Policy

### Task 1: term-limits-and-fitness.html (19 missing cards)

**Files:**
- Modify: `docs/pillars/term-limits-and-fitness.html`

- [ ] Read all `status-missing` cards in the file
- [ ] For each: add `<p class="rule-notes">` with research-backed rationale + adversarial review
- [ ] Sharpen any titles that are generic
- [ ] Change `status-missing` → `status-included`, `Proposed` → `Included` for each completed card
- [ ] Run: `npm run test:unit` — must pass
- [ ] Commit: `policy(term-limits): complete missing rule cards`

Key research areas for this pillar:
- Constitutional amendment requirements (Article V)
- Existing state-level term limit laws and their effectiveness
- Thornton v. Arkansas (1995) — SCOTUS holding on congressional term limits
- Historical entrenchment data: how long incumbents stay, electoral advantage data
- Fitness and cognitive standards: 25th Amendment analogy, existing federal fitness rules

### Task 2: gun-policy.html (30 missing cards)

**Files:**
- Modify: `docs/pillars/gun-policy.html`

- [ ] Read all `status-missing` cards in the file
- [ ] For each: add `<p class="rule-notes">` with research-backed rationale + adversarial review
- [ ] Change `status-missing` → `status-included`, `Proposed` → `Included`
- [ ] Run: `npm run test:unit` — must pass
- [ ] Commit: `policy(gun-policy): complete missing rule cards`

Key research areas:
- Heller (2008), McDonald (2010), Bruen (2022) — current Second Amendment doctrine
- Background check system gaps (NICS, private sales, gun show loophole)
- Red flag law effectiveness data
- Safe storage laws and their impact on accidents and theft
- Assault weapons definition challenges post-Bruen

---

## Chunk 2: P1 Medium Pillars — Science, Foreign Policy

### Task 3: science-technology-space.html (38 missing cards)

**Files:**
- Modify: `docs/pillars/science-technology-space.html`

- [ ] Read all `status-missing` cards
- [ ] Add `rule-notes` for each (legal basis, research, adversarial review)
- [ ] Promote to `status-included`
- [ ] Run tests, commit: `policy(science-tech): complete missing rule cards`

### Task 4: foreign-policy.html (50 missing cards)

**Files:**
- Modify: `docs/pillars/foreign-policy.html`

- [ ] Read all `status-missing` cards
- [ ] Add `rule-notes` — particularly important for: war powers, treaty obligations, arms sales, foreign aid conditionality
- [ ] Adversarial review emphasis: sovereignty conflicts, executive overreach paths, enforcement gaps in international agreements
- [ ] Promote to `status-included`
- [ ] Run tests, commit: `policy(foreign-policy): complete missing rule cards`

---

## Chunk 3: P1 Large Pillars — Equal Justice, Immigration

### Task 5: equal-justice-and-policing.html (143 missing cards)

**Files:**
- Modify: `docs/pillars/equal-justice-and-policing.html`

- [ ] Read all `status-missing` cards — scan for families first to understand structure
- [ ] Add `rule-notes` with: case law references, empirical evidence on policing disparities, enforcement mechanisms, accountability structures
- [ ] Adversarial review emphasis: qualified immunity workarounds, union contract barriers, civil liability caps
- [ ] Promote to `status-included`
- [ ] Run tests, commit per family: `policy(equal-justice): complete [FAMILY] cards`

Key research areas:
- Qualified immunity doctrine and reform proposals
- Pattern-or-practice investigations (DOJ authority)
- Consent decree effectiveness
- Body camera requirements and footage access
- Use-of-force standards (Graham v. Connor → community-safety standard)
- Civilian oversight board legal authority

### Task 6: immigration.html (225 missing cards)

**Files:**
- Modify: `docs/pillars/immigration.html`

- [ ] Read all `status-missing` cards by family
- [ ] ICE Abolition family (Task 3 from ICE audit): flesh out all cards with full rule-notes including: what replaces ICE, statutory authority, transition structure, accountability mechanisms
- [ ] For all families: add rule-notes with legal basis (INA, IIRIRA, DACA litigation, Plyler v. Doe)
- [ ] Adversarial review emphasis: enforcement gap during transition, due process in expedited removal, asylum clock manipulation
- [ ] Promote to `status-included`
- [ ] Commit per family: `policy(immigration): complete [FAMILY] cards`

---

## Chunk 4: P1 Massive Pillars — Healthcare, Tech/AI

### Task 7: healthcare.html (254 missing cards)

**Files:**
- Modify: `docs/pillars/healthcare.html`

- [ ] Scan by family — identify which families have the most missing cards
- [ ] Priority families: coverage, cost, pharmaceutical pricing, mental health parity, nursing staffing ratios
- [ ] For nursing/staffing cards specifically: safe staffing ratio research, California model data, evidence on patient outcomes
- [ ] Rule-notes must reference: ACA, Medicare Act, ERISA preemption issues, state action doctrine
- [ ] Adversarial review emphasis: ERISA preemption blocking state mandates, provider shortage as unintended consequence of mandates, cost-shift dynamics
- [ ] Promote to `status-included`
- [ ] Commit per family

### Task 8: technology-and-ai.html (386 missing cards)

**Files:**
- Modify: `docs/pillars/technology-and-ai.html`

- [ ] Scan by family — this is the largest single pillar
- [ ] Priority families given recent work: FACE (just rewritten), PUBL (removed), remaining surveillance/data/labor families
- [ ] Rule-notes must reference: GDPR as comparison, proposed US federal privacy legislation, FTC Act Section 5, CCPA, biometric laws (BIPA)
- [ ] Adversarial review emphasis: preemption conflicts, First Amendment challenges to content moderation rules, enforcement jurisdiction gaps
- [ ] Promote to `status-included`
- [ ] Commit per family

---

## Chunk 5: P2 Pillars

Work through P2 pillars using the same process:

- [ ] anti-corruption.html (28 missing)
- [ ] courts-and-judicial-system.html (26 missing)
- [ ] information-and-media.html (22 missing)
- [ ] infrastructure-and-public-goods.html (37 missing)
- [ ] checks-and-balances.html (35 missing)
- [ ] rights-and-civil-liberties.html (30 missing)
- [ ] legislative-reform.html (16 missing)
- [ ] elections-and-representation.html (22 missing)

Commit per pillar: `policy([pillar]): complete missing rule cards`

---

## Chunk 6: P3 Pillars

- [ ] administrative-state.html (20 missing)
- [ ] environment-and-agriculture.html (28 missing)
- [ ] executive-power.html (17 missing)
- [ ] taxation-and-wealth.html (42 missing)
- [ ] antitrust-and-corporate-power.html (11 missing)
- [ ] consumer-rights.html (13 missing)
- [ ] labor-and-workers-rights.html (18 missing)
- [ ] housing.html (13 missing)
- [ ] education.html (7 missing)

---

## Testing

Run after every pillar:
```bash
npm run test:unit   # must pass — 42 tests
```

Run after all HTML changes are complete:
```bash
npm run test:e2e    # Playwright/Firefox full site check
```
