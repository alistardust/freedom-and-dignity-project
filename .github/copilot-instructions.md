# Copilot Instructions

## Project context

This repository is an active U.S. policy platform in development. The live site is at https://alistardust.github.io/freedom-and-dignity-project/.

For current pillar counts, foundation structure, and corpus inventory, read `.github/current-state.md` before making structural changes. Do not hardcode counts from this file — verify them from the repository.

The policy corpus is primarily maintained in:

- `docs/pillars/*.html` — live policy card HTML
- `policy/catalog/policy_catalog_v2.sqlite` — structured policy position catalog (v2 ID format)
- `policy/foundations/<foundation>/<pillar>/` — narrative prose markdown (overview and policy sections per pillar)

The markdown under `policy/foundations/<foundation>/<pillar>/` may lag behind the site HTML.

For shared repository context, provenance notes, and maintenance expectations, also read `.github/ai-repo-context.md`.

---

## Source of truth

### Phase 1 — Current (pre-reconciliation)

The site HTML and the DB have both been edited since last reconciliation. Neither auto-overrides the other.

- **Site HTML** (`docs/pillars/*.html`) — the most recently edited content
- **DB** (`policy/catalog/policy_catalog_v2.sqlite`) — structured catalog; some entries not yet on site; some site cards not yet in DB
- **Divergences are flagged for human review.** Do not auto-resolve them.
- `MISSING` in the DB does not reliably mean the position is absent from the site.

**During Phase 1:** HTML edits are valid. Any new positions added to HTML must be backfilled into the DB in the same commit.

### Phase 2 — Post-reconciliation (target)

Once the reconciliation audit is complete:

- `policy/catalog/policy_catalog_v2.sqlite` is the **canonical source of truth** for all policy positions
- `policy/foundations/<foundation>/<pillar>/overview.md` and `policy/foundations/<foundation>/<pillar>/policy.md` are the source for narrative prose
- `docs/pillars/*.html` is **generated output** — do not hand-edit policy cards

Do **not** assume the current pillar files are complete.

---

## Working with IDs and the catalog

- Policy position IDs use the v2 format: `XXXX-XXXX-0000` (regex: `^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$`), e.g. `HLTH-COVR-0001`.
- The canonical position records live in the `positions` table in `policy/catalog/policy_catalog_v2.sqlite`.
- Domain codes (4 chars) and subdomain codes (4 chars) are defined in the `domains` and `subdomains` tables.
- Cross-pillar appearances are tracked in `position_pillar_appearances` — not in a separate position record.
- v1-to-v2 ID mappings live in `legacy_id_map` (`old_id` → `new_id`, with `source` = `db`/`html`/`both`).
- The old v1 DB (`policy/catalog/policy_catalog_v2.sqlite`) is retained for provenance only — do not query it for current data.

To rebuild the v2 catalog from source data:

```bash
scripts/build-catalog-v2.py
```

Do not hand-edit `policy/catalog/policy_catalog_v2.sqlite`.

---

## Known context-sensitive edge cases

- Some migration-map rows in the chats are stale relative to later canonical IDs.
- Some IDs appear only as future placeholders or optional variants and should not be promoted automatically.
- Some structured IDs were identified only in prose and had to be seeded into the catalog from context (`TAXN-TAXS-0001`, `ADMN-CHVS-0001`, `ADMN-AGYS-0001`, `HLTH-TRLS-0001`).
- Some unresolved prose-only IDs may represent future work rather than canon; check the surrounding chat context before formalizing them.

---

## Editing guidance

- Prefer updating import logic and source-backed docs over manual data patching.
- Preserve provenance. If you convert or reconcile IDs, keep the relationship visible through the database rather than deleting history.
- When updating policy content, check the current site HTML first, then the DB, then the source logs.
- Keep changes surgical: context and traceability matter as much as the final wording.

## Mandatory pre-drafting requirement for new policy (PAOS-AUTH-0010)

**Before writing any new policy rule, policy family, or policy section**, you must:

1. **Read the full PolicyOS framework** — all three layers in order:
   - `policy/policyos/policyos_platform_values_v1.md` — values that must not be violated
   - `policy/policyos/policyos_1_0_rules_proposal.md` — cross-platform design constraints; identify which KERN rules and overlays apply
   - `policy/policyos/policyos_authoring_os_v1.md` — structural requirements every rule must satisfy (NORM/AUTH/TEST/ENFC/PLAC/MAINT checklists)

2. **Conduct domain-specific research** into the policy area before drafting:
   - Applicable federal/state regulatory frameworks and statutes
   - Relevant industry standards and professional body guidelines
   - Known failure modes, enforcement gaps, and historical context
   - Empirical evidence and primary data sources

3. **Document what you consulted** — every new policy card must include a `rule-notes` field citing the PolicyOS rules applied and the primary sources reviewed.

Policy that skips this step is not eligible for adoption per PAOS-AUTH-0010. This applies equally to AI-assisted and human-authored drafts.

## Mandatory adversarial review for all policy work (PAOS-TEST-0008)

**Adversarial review is required for all policy writing, expansion, and rewriting.** The review must explicitly and separately address three named categories — **gaps, edge cases, and loopholes** — as distinct checks, not collapsed into a general note:

- **Gaps** — what the rule fails to cover; who it fails to protect; which scenarios fall outside its scope; which harms go unremedied
- **Edge cases** — boundary conditions, unusual fact patterns, and populations the rule treats inconsistently or leaves in an indeterminate state
- **Loopholes** — paths by which a regulated actor can satisfy the letter of the rule while defeating its purpose, including definitional workarounds, jurisdictional escape routes, and structural evasion

These three must be reviewed and documented separately. In addition, the review must also address: unintended consequences, foreseeable abuse paths, perverse incentives, and burden-shifting.

This applies to: new rules, additions to existing families, rewrites, scope expansions, and any change that substantively alters a right, duty, prohibition, or access condition.

**The review must be documented with findings for each of the three named categories.** A finding of "no issues" is valid only if it explains why. Skipping or collapsing the named categories is not compliant with PAOS-TEST-0008.

---

## PolicyOS

PolicyOS is the cross-platform system-rules layer being developed in parallel with the pillar policy content. All PolicyOS research and drafts live in:

```
policy/policyos/
```

The current hierarchy (as of April 2026):

1. **Platform values** — `policy/policyos/policyos_platform_values_v1.md` — the moral/political anchor for all rules. Uses a `floor + duty` model (what policy must not violate vs. what it must actively secure). **Locked.**
2. **System principles** — `policy/policyos/policyos_1_0_rules_proposal.md` — cross-platform design rules (11 families: KERN/GEOG/FEDR/REGD/ENFA/AIGV/ECOL/THRV/DEMO/PRIV/ECON). **Locked.**
3. **Authoring OS** — `policy/policyos/policyos_authoring_os_v1.md` — how policy must be written, tested, scoped, enforced, and maintained (NORM/AUTH/TEST/ENFC/PLAC/MAINT families). **Locked.**

For governance, amendment process, and pillar compliance review gate, see: `policy/policyos/policyos_governance_v1.md`.

PolicyOS rules use the ID prefix `PLOS-` and `PAOS-`. Do not conflate them with pillar policy positions (`XXXX-XXXX-0000`).

All three layers are now canonicalized. Amendments follow the process defined in `policyos_governance_v1.md` and the amendment protocol in the values document. Do not make casual changes to any of the three canonical documents.

---


## Documentation maintenance

Any commit that changes the following **must** update the relevant repo documentation in the same commit:

- Pillar count or structure → update `.github/current-state.md` pillar registry + `README.md`
- Policy card count or schema → update `policy/catalog/README.md` + `.github/current-state.md`
- DB schema changes → update `policy/catalog/README.md` + `system_rules.md`
- New architectural decisions → update `.github/copilot-instructions.md` + `.github/current-state.md`
- New scripts or tooling → update `README.md` "Scripts" section

"Repo documentation" means: `README.md`, `system_rules.md`, `.github/current-state.md`, `.github/ai-repo-context.md`, `policy/catalog/README.md`, `.github/copilot-instructions.md`.
"Docs" (without "repo") means the website in the `docs/` directory. Never confuse the two.

---

## Citation standards

This project holds itself to the standard of a published policy document. Every factual claim, statistic, poll result, legal reference, and externally sourced assertion **must be cited**.

Use Wikipedia-style numbered inline annotations (e.g., `[1]`) and APA 7th edition reference lists. For HTML/Markdown formatting details and APA format examples, see `CODING_STANDARDS.md`.

### What must be cited

- Every statistic, poll result, or numerical claim
- Every reference to a study, report, or academic finding
- Every historical fact that is not common knowledge
- Every claim about what a law, court ruling, or official document says
- Every claim about what another political party or public figure has said or done

### What does not need a citation

- The project's own policy positions and arguments
- Common knowledge (e.g., "the U.S. Constitution was ratified in 1788")
- Internal cross-references to other pillars or documents in this project

### Source quality hierarchy

Prefer sources in this order:
1. Primary sources: federal statutes, court opinions, official government data (Census, BLS, CBO, GAO, CRS)
2. Peer-reviewed academic research
3. Established non-partisan research institutions (Pew, Brookings, EPI, KFF, Brennan Center)
4. Major news outlets with editorial standards (NYT, WaPo, Reuters, AP, NPR)
5. Advocacy or partisan sources — cite only for attribution ("Organization X claims..."), never as neutral fact

---

## Copyright and plagiarism safeguards

Core rules:
- Do not reproduce substantial verbatim text from copyrighted sources. Quote sparingly and only when the exact wording materially matters.
- Facts and statistics are not copyrightable — the number is free to use with a citation; the original expression is not.
- Federal government works (statutes, regulations, court opinions, agency reports) are in the public domain and may be quoted more freely, but must still be cited.
- AI-synthesized text must be treated as unverified draft material. All AI output incorporating external facts or research must be re-sourced against primary or original references before publication.
- Do not cite a source you have not verified. Confirm the source exists, the URL resolves, and it actually supports the claim.
- Attribute every idea, framing, or argument that originated outside this project.
- Prefer paraphrase, synthesis, and citation over quotation.
- When in doubt: paraphrase, add original analysis, and cite.

---

## Quality and accuracy safeguards

This project is a public policy document. Accuracy, verification, and intellectual honesty are mandatory.

### Before publishing any factual claim

1. **Verify the source exists.** Confirm the publication, date, and author match what is cited.
2. **Verify the claim is accurate.** Confirm the source actually supports the statement — not just something adjacent.
3. **Check the date.** Data goes stale. Prefer the most recent data; note the date in the citation.
4. **Check for context.** A statistic can be technically accurate and misleading. Ensure the framing reflects what the source actually demonstrates.

### Adversarial review requirement

Before finalizing any section that makes empirical claims, actively try to disprove or find exceptions to the claims. If counterevidence or contradicting data exists:
- Acknowledge it honestly.
- Either explain why it does not change the conclusion, or revise the conclusion.
- Do not suppress contradicting evidence. This is non-negotiable.

Treat AI-generated factual material as unverified draft text until checked against real, accessible sources. If a source cannot be verified, remove the claim or reframe it as the project's own position.

### Language integrity

- Do not present the project's own policy positions as if they are established facts.
- Do not use weasel words ("many experts agree," "studies show") without citing specific experts and specific studies.
- Do not use emotional language in research/sources sections; reserve advocacy framing for mission and pillar narrative sections.
- Always distinguish between "this is what the research shows" and "this is what we believe should be done."

---

## Testing standards

Current test entry points:
- **Unit tests:** Vitest — `tests/unit/data.test.js` — run with `npm run test:unit`
- **E2E tests:** Playwright (Firefox only) — `tests/e2e/site.spec.js` — run with `npm run test:e2e`

Always run `npm run test:unit` before committing. Run `npm run test:e2e` after any HTML/JS/CSS change.

Every code change must be accompanied by tests that verify the **behavior changed**, not just the implementation. Test behavior, not incidental implementation details. Update stale count-based assertions when structure changes.

**Do not:**
- Test CSS styles or visual appearance directly (fragile, wrong layer)
- Use `toBeVisible()` alone to test opacity — Playwright considers `opacity:0` elements as "visible" in the DOM. Use `.toHaveClass(/visible/)` for IntersectionObserver-driven reveals instead.
- Write tests that only check element existence when behavior is what matters

### GitHub Pages path handling

The site runs on GitHub Pages at `/freedom-and-dignity-project/`. Path logic in `app.js` must account for the repo base path being a path segment. Use named subdir checks (`/\/(pillars|compare)\//.test(location.pathname)`) rather than segment counting, which breaks at the root level.

### Test patterns to follow

**Structural count assertions** — always comment the expected value with context:
```js
// 22 pillars + 1 shared rights card = 23
await expect(page.locator('a.pi-fv-pill')).toHaveCount(23);
```

**Link validity** — don't just check `href` exists; navigate and assert the target loads:
```js
const href = await page.locator('a.about-ai-link').getAttribute('href');
await page.goto(href);
await expect(page).toHaveTitle(/AI/i);
```

**IntersectionObserver-driven visibility** — scroll into view, then check for the `.visible` class:
```js
await page.locator('#pil-policy').scrollIntoViewIfNeeded();
await expect(page.locator('#pil-policy')).toHaveClass(/visible/, { timeout: 3000 });
```

**Injected elements** — test both existence and correct path resolution across page types:
```js
// Test on a root page AND a subdir page — path logic must be correct for both
for (const url of ['/', '/pillars/healthcare.html', '/compare/republican-party.html']) {
  await page.goto(url);
  const link = page.locator('.nav-links a[href*="about-ai"]');
  await expect(link).toBeAttached();
}
```

**Negative assertions** — test that prohibited patterns are absent:
```js
// The core quote must never appear in quotation marks
const text = await page.locator('.hero-statement').textContent();
expect(text).not.toMatch(/^["""]/);
```

```bash
npm run test:unit          # Vitest — fast, run always
npm run test:e2e           # Playwright — full site, run after HTML/JS/CSS changes
npm run test:e2e -- --headed  # Run with browser visible for debugging
```

---

## Frontend architecture

### The DRY rule — no copy-pasted structure

The single most important frontend rule: **never duplicate structural code across files.**

- **CSS** — All styles live in `docs/assets/css/style.css`. Never add `<style>` blocks to individual HTML pages. The only permitted inline style in a pillar page is the single-line accent color: `<style>:root { --accent-color: #...; }</style>`. Everything else belongs in the shared stylesheet.
- **JavaScript** — All sitewide logic lives in `docs/assets/js/app.js`. Use feature detection (`if (document.getElementById('pil-snav'))`) to scope page-specific behavior. Do not add `<script>` blocks to individual HTML pages except for page-specific inline data (rare and must be justified).
- **HTML structure** — Nav, footer, WIP banner, and injected nav links are all generated by `app.js`. Do not hard-code these in new pages beyond the minimal shell required for `app.js` to attach to.

### Dynamic values

Any number or count derived from `data.js` must be rendered dynamically, not hard-coded.

- Use `<span data-dynamic="pillar-count">23</span>` — the fallback is displayed when JS is disabled; `app.js` fills the live value.
- Use `data-dynamic="policy-count"` and `data-dynamic="family-count"` in pillar design sections.
- Use `data-dynamic="foundation-count"` for any reference to the number of foundations.
- **Never write "we have X pillars" with a literal number.** It will go stale.

### Generating new pages — never copy-paste

**Do not copy an existing HTML file to create a new one.** Use the generator scripts:

```bash
# New pillar page:
node scripts/new-pillar.js --id my-pillar --title "My Pillar" --foundation freedom-to-thrive --color "#1a6b8a" --prefix "MPL"

# New compare page:
node scripts/new-compare.js --id my-party --party "Party Name" --color "#336699" --tagline "One-sentence description of this platform."
```

The new-pillar script also prints the exact `data.js` update and test count changes required.

### Adding a new pillar — complete checklist

1. `node scripts/new-pillar.js ...` — generates `docs/pillars/<id>.html`
2. Add entry to `ARP.pillars` in `docs/assets/js/data.js`
3. Add pillar ID to the relevant foundation's `.pillars` array in `data.js`
4. Increment `PILLAR_COUNT` in `tests/unit/data.test.js` and `tests/e2e/site.spec.js`
5. Add pillar to `SAMPLE_PILLARS` in `tests/e2e/site.spec.js`
6. `npm run test:unit && npm run test:e2e` — must pass before committing
7. No other files need manual updating — nav, footer, counts, and WIP banner are all injected by `app.js`

### CSS variable conventions

| Variable | Purpose |
|---|---|
| `--accent-color` | Per-pillar accent; set inline per page; defaults to `var(--red)` |
| `--navy` `#1a2a4a` | Primary dark color for nav, hero backgrounds |
| `--red` `#bf0a30` | Brand red — action, urgency, Foundation I |
| `--gold` `#c9952a` | Secondary accent, WIP banner |
| `--sky` `#1a6b8a` | Foundation V / infrastructure accent |
| `--cream` `#faf6ef` | Page background |
| `--ink` | Body text |
| `--rule` | Border / divider color |

---

## Accessibility — Non-Negotiable

Accessibility operates on two equal dimensions: **disability access** and **content democratization**. Neither overrides the other, and neither justifies weakening the project's policy positions or directness.

### Disability accessibility (WCAG 2.1 AA)

These are requirements. Violations are treated the same as security failures — fix before merging.

**Structure and semantics**
- Every page must have `<html lang="en">`.
- Every page must have a single `<h1>`; heading levels descend without skipping (`h1 → h2 → h3`, never `h1 → h3`).
- Use semantic HTML first: `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<button>`, `<label>`. ARIA is for when native semantics are insufficient — incorrect ARIA is worse than no ARIA.
- Every page must begin with a skip link (injected by `app.js`): `<a href="#main-content" class="skip-link sr-only focusable">Skip to main content</a>`. The first main content section must have `id="main-content"`.

**Images and media**
- All `<img>` must have meaningful `alt` text. Decorative images get `alt=""`.
- Informational icons must have an `aria-label` or visible adjacent label — never convey meaning through icon alone.
- Video and audio content requires captions and a text transcript.

**Color and contrast**
- Normal text: ≥ 4.5:1 contrast ratio against its background.
- Large text (≥ 18pt / 14pt bold): ≥ 3:1.
- UI components (buttons, inputs, focus indicators): ≥ 3:1.
- Color must never be the **only** way information is conveyed — always pair with text, pattern, or icon.

**Keyboard and interaction**
- All functionality must be operable via keyboard alone (Tab, Shift+Tab, Enter, Space, Escape, arrow keys).
- Focus indicator must always be visible — never use `outline: none` or `outline: 0` without replacing it with an equally visible alternative.
- Interactive elements must have a descriptive accessible name: visible label text, `aria-label`, or `aria-labelledby`. Never use `title` attribute alone.
- Collapsible sections: use `<details>/<summary>` (accessible by default) or `aria-expanded` + `aria-controls` on custom accordions.
- Modal dialogs must trap focus and return focus to the trigger on close.

**Motion and animation**
- Every CSS animation and transition must have an override under `@media (prefers-reduced-motion: reduce)`. The global override in `style.css` handles this — do not add `!important` transitions that escape it.
- Never auto-play video or audio.

**Forms**
- Every `<input>`, `<select>`, and `<textarea>` must have an associated `<label>`. `placeholder` alone is not a label.
- Error messages must identify the field and explain what is wrong. Never use color alone to signal an error.

Required CSS utilities (`.sr-only`, `.focusable`, `:focus-visible`, `prefers-reduced-motion`) are defined in `docs/assets/css/style.css` — do not redefine elsewhere. See `CODING_STANDARDS.md` for the canonical definitions.

### Content accessibility (democratization)

Content accessibility means the site's policy content is usable by people of varying educational backgrounds. It does **not** mean weakening positions or shifting policy toward the center.

**Plain language and the two-field requirement**
- Every policy pillar and major policy family must have a 1–2 sentence plain-language summary (~8th-grade reading level) appearing alongside the full technical position.
- **Every individual policy position (card) must have both a `rule-plain` field and a `rule-stmt` field:**
  - `rule-plain` — 1–3 sentences in plain language (~8th grade). What does this position do, and why does it matter? No jargon.
  - `rule-stmt` — The full technical/legal policy statement with precise language, thresholds, enforcement mechanisms, and regulatory detail.
  - Both fields are required. `rule-plain` is not a summary of `rule-stmt` — it is an independent, accessible explanation. When they conflict, escalate for review; do not silently resolve.
  - In HTML: `<p class="rule-plain">` appears immediately after `<p class="rule-title">`, before `<p class="rule-stmt">`.
  - In the DB: `plain_language TEXT` column on the `positions` table — to be added post-migration.
- Legal or technical jargon must be defined on first use with a tooltip, glossary link, or parenthetical.
- Policy card titles must be understandable without prior domain knowledge.

**Language and inclusion**
- Use gender-neutral language throughout: "persons" not "men"; singular "they/them"; avoid gendered role titles unless quoting a named law.
- Do not write in a voice that implies the reader is already politically aligned.

**Contribution pathways**
- The Get Involved page must always prominently list all active contribution channels: GitHub (technical), Discord (community), and any active non-technical workflow.
- CONTRIBUTING.md and issue templates must be written for someone who has never used GitHub.
- Every policy proposal must have a clear path for non-technical review.

**Zoom and responsive layout**
- All content must be readable and fully operable at 200% browser zoom without horizontal scrolling.
- No fixed pixel heights that clip text when font size increases. Use `min-height` or `auto` height where needed.

---

## Build architecture

### Current state (Phase 1)

The site is hand-authored HTML. Policy position cards in `docs/pillars/*.html` are the most recently edited content. The DB was built from the v1 catalog and all tagged HTML cards and has not been fully reconciled with the current HTML.

Until reconciliation is complete:
- HTML edits are valid; backfill any new positions into the DB in the same commit
- Run `scripts/tag-policy-cards.py` after any HTML structural changes to normalize IDs

### Target state (Phase 2, post-reconciliation)

- `policy/catalog/policy_catalog_v2.sqlite` is the single source of truth for all policy positions
- `policy/foundations/<foundation>/<pillar>/overview.md` and `policy/foundations/<foundation>/<pillar>/policy.md` are the source for narrative prose
- `docs/pillars/*.html` is generated output — do not hand-edit policy cards
- A build script (`scripts/generate-site.py`, TBD) will render HTML from DB + markdown
- Any content change must be made in the source (DB or markdown), then the site regenerated

### Consistency rules (apply now and in Phase 2)

- All styles: `docs/assets/css/style.css` only. No inline styles except `--accent-color` per pillar.
- All sitewide JS: `docs/assets/js/app.js` only. No inline scripts in HTML.
- All policy positions: must have a `XXXX-XXXX-0000` ID. Untagged cards are not canonical.
- All factual claims on the site: must have an APA 7th edition footnote.

---

## General coding standards

See `CODING_STANDARDS.md` for the full reference. See the global Copilot instructions (`~/.copilot/copilot-instructions.md`) for the universal subset covering naming, error handling, logging, security, function design, architecture, testing, git, Python, and JavaScript.

---

## Explicit Approval

When a task requires user approval, the agent must ask directly and wait for an unambiguous affirmative confirmation before acting.

Valid approval includes clear affirmative confirmations such as:
- `Yes`
- `Approve`
- `Approved`
- `Affirmative`
- `Confirmed`

The following do not count as approval:
- `Go ahead`
- `Go ahead and do this`
- `Proceed`
- `Sounds good`
- implied intent
- contextual inference
- language that could reasonably be interpreted in more than one way

If approval is required and has not been given, the agent may prepare work, explain the next step, or show a proposed patch, but must not apply the change.

Review and approval requests must be presented one at a time.

When proposing edits for approval:
- Show only one approval request before waiting for a reply.
- Each approval request must contain one complete logical change set.
- Do not split a coherent edit into smaller fragments solely to reduce size.
- Do not combine unrelated edits into one approval request.
- If a file contains multiple unrelated edits, present them as separate approval requests.
- Prefer smaller diffs when possible, but preserve logical completeness.
