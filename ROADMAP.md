# Freedom and Dignity Project — Roadmap

*Last updated: 2026-04-27. Keep this file current as milestones shift.*

---

## Current state

- **25 policy pillars** across 5 foundations
- **3,810+ canonical positions** in `policy/catalog/policy_catalog_v2.sqlite` (source of truth)
- **PolicyOS** drafted and canonicalized: values locked (Layer 1), system rules under review (Layer 2), authoring OS under review (Layer 3)
- **Site** live at <https://alistardust.github.io/freedom-and-dignity-project/> — static HTML on GitHub Pages
- **PolicyOS pillar audit** complete (2026-04-27): inheritance declarations and whistleblower coverage added across all 25 pillars; critical gap remediation in progress

---

## Release milestones

```
Milestone 1: PolicyOS 1.0 + Site Prototype   ← current
Milestone 2: Full site launch                ← after prototype feedback
Milestone 3: Infrastructure                  ← plan now, execute after or parallel with M2
```

**Milestone 1 ships as a single coordinated release:** PolicyOS 1.0 finalized and published on site + a ground-up prototype of the redesigned site. These ship together because PolicyOS is a featured part of the new site.

---

## Milestone 1 — PolicyOS 1.0 + Site Prototype

### PolicyOS work (in progress)

- [x] Layer 1: Platform values (`policyos_platform_values_v1.md`) — locked
- [x] Layer 2: System principles (`policyos_1_0_rules_proposal.md`) — locked
- [x] Layer 3: Authoring OS (`policyos_authoring_os_v1.md`) — locked
- [x] Governance document (`policyos_governance_v1.md`) — locked
- [x] Full pillar audit against PolicyOS — complete (2026-04-27)
- [x] P1: Inheritance declarations + whistleblower coverage — complete
- [ ] P2: Critical gap remediation (CORT, SCIS, TERM, INFR, LEGL) — in progress
- [ ] P3: High-gap pillar reinforcement (CHKS, ELEC, FPOL, GUNS, HOUS, MDIA, RGHT)
- [ ] P4: Systemic overlay gap remediation (AIGV, THRV, ENFA sweeps)
- [ ] PolicyOS highlight page on site

### Site prototype — what ships

**Ground-up redesign:**
- `index.html` — tour entry point, values-first, re-anchored to New Bill of Rights
- `mission.html` — moral imperative framing, historical lineage, aspirational language
- `foundations.html` — each foundation with long-term vision + near-term entry points
- `get-involved.html` — culmination of the tour; the ask must feel earned
- `roadmap.html` — updated to reflect current phases
- `constitution.html`
- `classification.html`
- `adversarial-review.html`

**New pages:**
- The New Bill of Rights (name TBD — see blocking decisions below)
- PolicyOS 1.0 page

**Layout/tone updates only (no ground-up rewrite):**
- `about-ai.html`
- `about-us.html`
- `letter-from-the-founder.html`

**Deferred to Milestone 2:**
- Pillar page structural redesign (content stays; template/tour-flow update is a separate pass)
- `compare/` pages
- Search
- Infrastructure changes

### Blocking decisions

1. **Bill of Rights name** — must be decided before Phase 2 content writing begins. Candidates:
   - *A New Bill of Rights* — clean, historically neutral
   - *The People's Bill of Rights* — populist, strong
   - *The Freedom and Dignity Bill of Rights* — ties to project identity

   The three foundational rights documents (regardless of name):
   | Document | Scope |
   |---|---|
   | The New Bill of Rights | 10 amendments: civil, political, personal, environmental, material rights |
   | The New Bill of Workers' Rights | Fair wages, organizing, safe conditions, family leave, economic security |
   | The Declaration of Indigenous Rights | Sovereignty, treaty fulfillment, land rights, cultural survival, territorial self-determination |

---

## Milestone 1 — Design principles for the site prototype

### The site is a tour

Every page answers: *why does this matter?* and *what's next?* No page should feel like a dead end.

Proposed tour order:
```
index (who we are, why we exist)
  → mission (the case for change)
  → foundations (the five pillars of the vision)
  → [pillar pages] (the actual policy)
  → classification / PolicyOS (how it's built)
  → roadmap (what comes next)
  → about-us / letter-from-the-founder (the people)
  → get-involved (the ask)
```

Each page needs a clear "next" CTA that feels earned, not forced.

### Tone and inspirational framing

The site should channel:
- **Civil rights movement** — urgency, moral clarity, collective action, the sense that history is watching
- **FDR** — freedom without material security is not real freedom; economic rights as human rights
- **Obama 2008** — hope, possibility, optimism; politics as something that can make people's lives better
- **TR** — fighting concentrated power; government exists to serve people, not the other way around
- **JFK** — aspiration, the long game, service as something inspiring
- **Lincoln** — the moral weight of being on the right side of history

**What this is NOT:** heavy, bureaucratic, technocratic, exhausting. The gravity should make people want to act, not give up.

The tone guide:
- Lead with what is *possible*, not what is broken
- Make the vision feel achievable and worth being part of
- Frame participation as meaningful, not performative
- The platform is a moral imperative framed as an invitation, not a lecture
- Big scope = respect for the problems, not hubris

### Faith and values framing

The platform's values — dignity, equality, care for the vulnerable, stewardship of the earth, accountability, fairness — are consistent with the core teachings of Christianity, Judaism, Islam, Buddhism, and secular humanism. This framing is not a religious appeal — it is a recognition that the moral foundations of the platform are shared across traditions. The site should feel welcoming to people of faith without requiring faith.

### "Not all or nothing" — aspirational + incremental

The platform holds two things at once:
1. **Big and aspirational** — a genuine long-term vision; the size signals seriousness
2. **Incremental and fallback-aware** — every major position should have an ideal goal *and* a realistic first step

The tone: "Here is the picture of what life could look like. Here is where we start."

---

## Milestone 2 — Full site launch

After prototype feedback. Includes:
- Full pillar page structural redesign (template/tour-flow update)
- `compare/` pages redesigned
- New Bill of Rights page (full floor+duty treatment for all 10 amendments)
- Search (SQLite WASM client-side, no server required)
- Mailing list integration (Buttondown recommended — simple, privacy-respecting)
- Social media launch (Twitter/X, Bluesky, Instagram; content calendar needed separately)

---

## Milestone 3 — Infrastructure

Plan now, execute after or in parallel with Milestone 2.

### Hosting

GitHub Pages is appropriate for now but not the long-term home (no server-side logic, no auth, tied to GitHub account).

Options under evaluation:
- **Netlify / Vercel** — static hosting + serverless functions; easy migration; good for search + light auth; free tiers generous
- **Self-hosted VPS** (DigitalOcean, Hetzner) — full control; requires devops; good for the internal review platform
- **Hybrid** — public site on Netlify/Vercel, internal tool on VPS

Decision not needed until Milestone 2 content work is done.

### Policy database search

Full-text search across the policy catalog from the site. Preferred path for Milestone 2: **SQLite WASM** — load the DB in-browser; no server needed; works on static hosting. Upgrade to serverless function if performance is insufficient.

### Internal review platform

A browser-based tool for human reviewers that does not require GitHub:
- Role model: **Owner** (final authority) → **Maintainers** (can approve) → **Contributors** (can propose + comment) → **Readers** (approved content only)
- Per-position review threads: comments, suggested edits, flags, status states
- Structured consensus signal (not a vote — owner is tiebreaker; tool surfaces agreement/disagreement)
- Most complex Phase 3 item — design the data model and governance rules first, then choose the tech

### Social media

Accounts needed: Twitter/X, Bluesky, Instagram, YouTube. Possibly TikTok, Threads. Needs a content calendar, not just account creation. Natural content formats: "imagine" cards, one-sentence pillar stories, PolicyOS explainers, Bill of Rights as shareable format.

---

## The New Bill of Rights — structure (finalized)

10 amendments — a deliberate parallel to the original Bill of Rights.

| # | Amendment | One-line |
|---|---|---|
| 1 | Right to Vote | Your voice in who governs you is sacred — and may not be denied, suppressed, or made practically impossible. |
| 2 | Right to Self-Governance | You have the right to shape the institutions and systems that shape your life. |
| 3 | Right to Organize | You have the right to join together — with coworkers, neighbors, or fellow citizens — to demand better. |
| 4 | Right to Bodily Autonomy | Your body is yours — including your reproductive choices, your medical decisions, and your right to age and die with dignity. |
| 5 | Right to Privacy | Your personal life, your data, and your communications belong to you — not to corporations or government agencies. |
| 6 | Right to Indigenous Sovereignty | The nations that were here first have rights that predate this government — and this government has obligations it has not kept. |
| 7 | Right to a Healthy Environment | Clean air, clean water, healthy waterways and ecosystems, and a stable climate are not luxuries — they are the shared conditions of life. |
| 8 | Right to Equal Justice | The law applies equally to everyone, and every person has the right to participate fully in public life. |
| 9 | Right to Cultural Identity | Every person has the right to their language, their faith, their heritage, and their cultural life. |
| 10 | Right to Basic Necessities | Healthcare, housing, food, a living income, education, childcare, elder care, economic security, and rest are not privileges — they are the floor of a free society. |

### Sub-rights (confirmed)

**Amendment 4 — Bodily Autonomy:** reproductive rights (contraception, abortion), gender-affirming care, end-of-life decisions, freedom from physical coercion

**Amendment 5 — Privacy:** Freedom from Surveillance · Digital Privacy · Medical Privacy · Financial Privacy · Search and Seizure Limits

**Amendment 7 — Healthy Environment:** Clean Air · Clean Water (all waterways) · Climate Stability

**Amendment 8 — Equal Justice:** Equal Protection · Due Process · Full Participation · Accessibility · Family Integrity · Right to Form a Family

**Amendment 9 — Cultural Identity:** Religious Freedom · Linguistic Identity · Cultural Participation · Artistic Expression · Cultural Heritage · Native Hawaiian and Pacific Islander cultural rights

**Amendment 10 — Basic Necessities:** Healthcare · Housing · Food · Living Income · Clean Water (shared with A7) · Education · Childcare · Elder Care · Economic Security · Rest
