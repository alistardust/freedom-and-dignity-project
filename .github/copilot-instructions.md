# Copilot Instructions

## Project context

This repository is an active U.S. policy platform in development. It is organized around 25 policy pillars grouped into 5 foundations. The live site is at https://alistardust.github.io/freedom-and-dignity-project/.

The policy corpus is primarily maintained in:

- `docs/pillars/*.html` — live policy card HTML (2,935 `.policy-card` elements)
- `data/policy_catalog.sqlite` — structured policy position catalog (1,554 entries, pre-reconciliation)
- `pillars/` — narrative prose markdown (overview and policy sections per pillar)

The following files are historical source material, retained for provenance, and still referenced during catalog rebuilds:

- `sources/branch_branch_political_project_main.txt`
- `sources/branch_political_project_brainstorm.txt`

The markdown under `pillars/` may lag behind the site HTML. Read `overview/current-state.md` before making structural changes.

## Source of truth

### Phase 1 — Current (pre-reconciliation)

The site HTML and the DB have both been edited since last reconciliation. Neither auto-overrides the other.

- **Site HTML** (`docs/pillars/*.html`, 2,935 policy cards) — the most recently edited content
- **DB** (`data/policy_catalog.sqlite`, 1,554 `policy_items`) — structured catalog; some entries not yet on site; some site cards not yet in DB
- **Divergences are flagged for human review.** Do not auto-resolve them.
- `MISSING` in the DB does not reliably mean the position is absent from the site.

**During Phase 1:** HTML edits are valid. Any new positions added to HTML must be backfilled into the DB in the same commit.

### Phase 2 — Post-reconciliation (target)

Once the reconciliation audit is complete:

- `data/policy_catalog.sqlite` is the **canonical source of truth** for all policy positions
- `pillars/*/overview.md` and `pillars/*/policy.md` are the source for narrative prose
- `docs/pillars/*.html` is **generated output** — do not hand-edit policy cards
- New positions are authored in the DB first, then the site is regenerated at build time

Do **not** assume the current pillar files are complete.

## Working with IDs and the catalog

- The old numeric checkpoint items live in `legacy_policy_items`.
- The structured policy position records live in `policy_items` (prefixed IDs, e.g., `HLT-COV-003`).
- Legacy-to-structured conversions live in `record_links`.
- Prose/context-only IDs live in `prose_rule_mentions`.
- Use `deduped_catalog_entries` when you want the canonical structured corpus without the legacy numeric duplicates.
- Use `unresolved_prose_rule_mentions` when auditing IDs that were mentioned in context but not promoted into the canonical position corpus.

If chat-log sources change, rebuild the catalog with:

```bash
scripts/import_policy_catalog.py
```

Do not hand-edit `data/policy_catalog.sqlite`.

## Known context-sensitive edge cases

- Some migration-map rows in the chats are stale relative to later canonical IDs.
- Some IDs appear only as future placeholders or optional variants and should not be promoted automatically.
- Some structured IDs were identified only in prose and had to be seeded into the catalog from context (`ECO-TAX-001`, `ADM-CHV-001`, `ADM-AGY-001`, `HLT-TRL-001`).
- Some unresolved prose-only IDs may represent future work rather than canon; check the surrounding chat context before formalizing them.

## Editing guidance

- Prefer updating import logic and source-backed docs over manual data patching.
- Preserve provenance. If you convert or reconcile IDs, keep the relationship visible through the database rather than deleting history.
- When updating policy content, check the current site HTML first, then the DB, then the source logs.
- Keep changes surgical: context and traceability matter as much as the final wording.

---

## Documentation maintenance

Any commit that changes the following **must** update the relevant repo documentation in the same commit:

- Pillar count or structure → update `overview/current-state.md` pillar registry + `README.md`
- Policy card count or schema → update `data/README.md` + `overview/current-state.md`
- DB schema changes → update `data/README.md` + `system_rules.md` counts
- New architectural decisions → update `.github/copilot-instructions.md` + `overview/current-state.md`
- New scripts or tooling → update `README.md` "Scripts" section

"Repo documentation" means: `README.md`, `system_rules.md`, `overview/*.md`, `data/README.md`, `.github/copilot-instructions.md`.  
"Docs" (without "repo") means the website in the `docs/` directory.  
Never confuse the two.

---

## Citation standards

This project holds itself to the standard of a published policy document. Every factual claim, statistic, poll result, legal reference, and externally sourced assertion **must be cited**.

### Inline format

Use Wikipedia-style numbered annotations inline in HTML and Markdown:

```
Universal healthcare is associated with better population outcomes.[1]
```

The `[1]` links to (or corresponds to) the numbered entry in the References section at the bottom of the page or document. In HTML, render as:

```html
<sup><a href="#fn1" id="ref1">[1]</a></sup>
```

### Reference list format (APA 7th edition)

All reference lists use **APA 7th edition**. Key formats:

**News article:**
```
Author, A. A. (Year, Month Day). Title of article. *Publication Name*. https://url
```

**Government report / agency publication:**
```
Agency Name. (Year). *Title of report* (Report No. if applicable). https://url
```

**Academic journal article:**
```
Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, *Volume*(Issue), pages. https://doi.org/xxxxx
```

**Webpage with no author:**
```
Title of page. (Year, Month Day). *Organization Name*. https://url
```

**Federal statute (public domain):**
```
Name of Act, Pub. L. No. XXX-XX, § X, XX Stat. XXX (Year). https://url
```

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

This project is committed to originality, proper attribution, and full compliance with copyright law. These rules are non-negotiable.

### Core rules

**Never reproduce substantial verbatim text from copyrighted sources.** Quote sparingly — one or two sentences at most — and only when the exact wording matters. Always paraphrase and synthesize; always cite.

**Facts and statistics are not copyrightable.** The number itself (e.g., "the top 1% hold 30% of U.S. wealth") is a fact and can be stated freely with a citation to the source. The original presentation, analysis, and commentary by the author *is* copyrightable.

**Federal government works are in the public domain** (17 U.S.C. § 105). This includes federal statutes, federal regulations, federal court opinions, and documents produced by federal agencies in their official capacity. These may be quoted at length, but must still be cited.

**State government works** vary. Most state laws are public domain but confirm before reproducing at length.

**The "heart of the work" test:** Even a short quote can infringe if it captures the essential value of the original work (e.g., quoting the key finding of a paywalled study). When in doubt, paraphrase and cite.

### Plagiarism safeguards

- **Attribute every idea, framing, or argument that originated outside this project.** If a formulation was inspired by a source, cite it — even if the words are your own.
- **AI-synthesized text must be treated as a draft, not a final source.** AI can reproduce or closely paraphrase copyrighted material from its training data without flagging it. All AI output that incorporates external facts, quotes, or research must be reviewed and re-sourced from primary or original references.
- **Do not cite a source you have not verified.** AI frequently hallucinates citations — plausible-sounding but nonexistent articles, wrong authors, wrong dates, wrong page numbers, wrong URLs. Every citation added to this project must be verified: the source exists, the URL resolves, and it actually says what the citation claims it says.
- **Paraphrase actively.** Restating an idea in your own structure and words, then citing the source, is always preferred over quoting.

### Fair use: when in doubt, don't

Fair use in U.S. law (17 U.S.C. § 107) is assessed on four factors: purpose, nature of the work, amount used, and market effect. There is no safe word count. For this project:
- Political and policy commentary is a recognized fair use purpose.
- Brief quotation with attribution and analysis is lower risk than long reproduction.
- Using facts from a source (not its exact expression) is not infringement.
- When any doubt exists: paraphrase, add your own analysis, and cite.

---

## Quality and accuracy safeguards

This project is a public policy document. Errors damage credibility and, more importantly, mislead readers on matters of democratic governance. Quality is not optional.

### Before publishing any factual claim

1. **Verify the source exists.** Open the URL. Confirm the publication, date, and author match what is cited.
2. **Verify the claim is accurate.** Read the source. Confirm it actually supports the statement being made — not just something adjacent or vaguely related.
3. **Check the date.** Data goes stale. A 2018 study may be superseded by 2024 research. Prefer the most recent data; note the date in the citation.
4. **Check for context.** A statistic can be technically accurate and misleading. Ensure the framing reflects what the source actually demonstrates.

### Adversarial review requirement

Before finalizing any section that makes empirical claims, apply an **adversarial review**: actively try to disprove or find exceptions to the claims being made. If a counterargument or contradicting data exists:
- Acknowledge it honestly.
- Either explain why it does not change the conclusion, or revise the conclusion.
- Do not suppress contradicting evidence.

This is non-negotiable. Intellectual honesty is a core value of this platform.

### AI hallucination safeguards

AI language models can:
- Generate plausible-sounding but fabricated citations
- Misattribute quotes to real people
- Confuse similar statistics from different years or sources
- Present outdated data as current
- Produce confident-sounding claims that are simply wrong

**Every AI-generated factual claim in this project must be independently verified against a real, accessible source before it is published.** If a source cannot be found to support a claim, the claim must be removed or reframed as the project's own position (which does not require a citation).

### Language integrity

- Do not present the project's own policy positions as if they are established facts.
- Do not use weasel words ("many experts agree," "studies show") without citing specific experts and specific studies.
- Do not use emotional language in the research/sources sections; reserve advocacy framing for the mission and pillar narrative sections.
- Always distinguish between "this is what the research shows" and "this is what we believe should be done."

---

## Testing standards

### Stack
- **Unit tests:** Vitest — `tests/unit/data.test.js` — run with `npm run test:unit`
- **E2E tests:** Playwright (Firefox only) — `tests/e2e/site.spec.js` — run with `npm run test:e2e`
- Always run `npm run test:unit` before committing. Run `npm run test:e2e` after any HTML/JS/CSS change.

### What to test
Every code change must be accompanied by tests that verify the **behavior changed**, not just the implementation.

**Always test:**
- Any new HTML page or section: title, key headings, critical elements present and visible
- Any new JS feature injected by `app.js`: element exists in DOM, correct href, correct behavior
- Any navigation path: link exists, href is correct, navigating to it loads the expected page
- Any count-sensitive assertion (pillars, nav links, cards): update the count when structure changes — stale counts are bugs
- Any fix for a visual bug: write a test that would have caught the bug (e.g., section has `.visible` class after scroll)
- Any link that could 404: navigate to the href and assert the page loads correctly

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

### Keeping tests current
- When you add a new pillar, update `SAMPLE_PILLARS` in `site.spec.js` and update any count assertions.
- When you add a new nav item, update nav count assertions across all describe blocks.
- When you add a new page, add a describe block covering: title, key heading, nav visible, footer visible.
- When you fix a rendering or path bug, add a regression test that would have caught it.
- Run the full test suite after every change. A passing test suite is a prerequisite for committing.

### Running tests
```bash
npm run test:unit          # Vitest — fast, run always
npm run test:e2e           # Playwright — full site, run after HTML/JS/CSS changes
npm run test:e2e -- --headed  # Run with browser visible for debugging
```
---

## Frontend architecture & professional coding standards

### The DRY rule — no copy-pasted structure

The single most important frontend rule: **never duplicate structural code across files.**

- **CSS** — All styles live in `docs/assets/css/style.css`. Never add `<style>` blocks to individual HTML pages. The only permitted inline style in a pillar page is the single-line accent color: `<style>:root { --accent-color: #...; }</style>`. Everything else belongs in the shared stylesheet under a named section comment.
- **JavaScript** — All sitewide logic lives in `docs/assets/js/app.js`. Use feature detection (`if (document.getElementById('pil-snav'))`) to scope page-specific behavior. Do not add `<script>` blocks to individual HTML pages except for page-specific inline data (rare and must be justified).
- **HTML structure** — Nav, footer, WIP banner, and injected nav links are all generated by `app.js`. Do not hard-code these in new pages beyond the minimal shell required for `app.js` to attach to.

### Dynamic values

Any number or count derived from `data.js` must be rendered dynamically, not hard-coded.

- Use `<span data-dynamic="pillar-count">23</span>` — the fallback is displayed when JS is disabled; `app.js` fills the live value.
- Use `data-dynamic="policy-count"` and `data-dynamic="family-count"` in pillar design sections — these are auto-computed from `.policy-card` elements on the page.
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

These scripts produce a correctly structured, minimal HTML scaffold. Add content inside the generated placeholders. The new-pillar script also prints the exact `data.js` update and test count changes required.

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

### Code quality rules

- **No magic numbers** — any count, ID, or value that appears in more than one place must be a variable, CSS custom property, or `data-dynamic` span.
- **No inline event handlers** — use `addEventListener` in JS files.
- **No `!important` except the `.visible` animation override** in `app.js`.
- **No `id` conflicts** — pillar section IDs (`#pil-intro`, `#pil-policy`, etc.) are standard across all pillar pages; do not introduce new IDs that collide with this scheme.
- **Accessibility** — all interactive elements need `aria-label` or visible label text; images need meaningful `alt` text.
- **Citations** — every factual claim, statistic, or externally sourced assertion in policy HTML must have an APA 7th edition footnote. See the Citation standards section of copilot-instructions.md.

---

## Build architecture

### Current state (Phase 1)

The site is hand-authored HTML. Policy position cards in `docs/pillars/*.html` are the most recently edited content. The DB (`data/policy_catalog.sqlite`) was built from source log parsing and has not been fully reconciled with the HTML.

**Until reconciliation is complete:**

- HTML edits are valid; backfill any new positions into the DB in the same commit
- Do not treat DB status fields as authoritative (many `MISSING` entries are actually on the site)
- Run `scripts/tag-policy-cards.py` after any HTML structural changes to normalize IDs

### Target state (Phase 2, post-reconciliation)

- `data/policy_catalog.sqlite` is the single source of truth for all policy positions
- `pillars/*/overview.md` and `pillars/*/policy.md` are the source for narrative prose
- `docs/pillars/*.html` is generated output — do not hand-edit policy cards
- A build script (`scripts/generate-site.py`, TBD) will render HTML from DB + markdown
- CSS lives in `docs/assets/css/style.css` — single source, applied consistently site-wide
- Any content change must be made in the source (DB or markdown), then the site regenerated

### Consistency rules (apply now and in Phase 2)

- All styles: `docs/assets/css/style.css` only. No inline styles except `--accent-color` per pillar.
- All sitewide JS: `docs/assets/js/app.js` only. No inline scripts in HTML.
- All policy positions: must have a SCOPE-FAM-NNN ID. Untagged cards are not canonical.
- All factual claims on the site: must have an APA 7th edition footnote.
