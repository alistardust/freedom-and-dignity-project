# Copilot Instructions

## Project context

This repository is an active U.S. policy platform in development. It is organized around 25 policy pillars grouped into 5 foundations. The live site is at https://alistardust.github.io/freedom-and-dignity-project/.

The policy corpus is primarily maintained in:

- `docs/pillars/*.html` — live policy card HTML (2,935 `.policy-card` elements)
- `data/policy_catalog_v2.sqlite` — structured policy position catalog (2,783 positions, v2 ID format)
- `pillars/` — narrative prose markdown (overview and policy sections per pillar)

The following files are historical source material, retained for provenance, and still referenced during catalog rebuilds:

- `sources/branch_branch_political_project_main.txt`
- `sources/branch_political_project_brainstorm.txt`

The markdown under `pillars/` may lag behind the site HTML. Read `overview/current-state.md` before making structural changes.

## Source of truth

### Phase 1 — Current (pre-reconciliation)

The site HTML and the DB have both been edited since last reconciliation. Neither auto-overrides the other.

- **Site HTML** (`docs/pillars/*.html`, 2,935 policy cards) — the most recently edited content
- **DB** (`data/policy_catalog_v2.sqlite`, 2,783 `positions`) — structured catalog; some entries not yet on site; some site cards not yet in DB
- **Divergences are flagged for human review.** Do not auto-resolve them.
- `MISSING` in the DB does not reliably mean the position is absent from the site.

**During Phase 1:** HTML edits are valid. Any new positions added to HTML must be backfilled into the DB in the same commit.

### Phase 2 — Post-reconciliation (target)

Once the reconciliation audit is complete:

- `data/policy_catalog_v2.sqlite` is the **canonical source of truth** for all policy positions
- `pillars/*/overview.md` and `pillars/*/policy.md` are the source for narrative prose
- `docs/pillars/*.html` is **generated output** — do not hand-edit policy cards
- New positions are authored in the DB first, then the site is regenerated at build time

Do **not** assume the current pillar files are complete.

## Working with IDs and the catalog

- Policy position IDs use the v2 format: `XXXX-XXXX-0000` (regex: `^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$`), e.g. `HLTH-COVR-0001`.
- The canonical position records live in the `positions` table in `data/policy_catalog_v2.sqlite`.
- Domain codes (4 chars) and subdomain codes (4 chars) are defined in the `domains` and `subdomains` tables.
- Cross-pillar appearances are tracked in `position_pillar_appearances` — not in a separate position record.
- v1-to-v2 ID mappings live in `legacy_id_map` (`old_id` → `new_id`, with `source` = `db`/`html`/`both`).
- The old v1 DB (`data/policy_catalog.sqlite`) is retained for provenance only — do not query it for current data.

To rebuild the v2 catalog from source data:

```bash
scripts/build-catalog-v2.py
```

Do not hand-edit `data/policy_catalog_v2.sqlite`.

## Known context-sensitive edge cases

- Some migration-map rows in the chats are stale relative to later canonical IDs.
- Some IDs appear only as future placeholders or optional variants and should not be promoted automatically.
- Some structured IDs were identified only in prose and had to be seeded into the catalog from context (`TAXN-TAXS-0001`, `ADMN-CHVS-0001`, `ADMN-AGYS-0001`, `HLTH-TRLS-0001`).
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

## General coding standards

The full coding standards document lives at `CODING_STANDARDS.md` in the repo root. It is the authoritative reference. The rules below are the non-negotiable subset enforced in every commit.

### Naming — the first and most important rule

Variable, function, and class names must describe **what the thing is**, not what content it relates to or what project it belongs to.

| ✓ Good | ✗ Bad | Why |
|---|---|---|
| `const siteData = {...}` | `const ARP = {...}` | `ARP` is a project acronym, not a description |
| `user_count` | `n` | Single letters reveal nothing |
| `is_active` | `flag` | Vague; a flag for what? |
| `get_user()` | `doThing()` | Functions are verb phrases |
| `MAX_RETRIES` | `3` | No magic numbers |
| `PaymentProcessor` | `Processor` | Noun phrases, as specific as possible |

**Never:**
- Single-letter names except `i`/`j` loop counters
- Shadow built-ins (`list`, `id`, `type`, `input`, `filter`)
- Invent new abbreviations — only well-known ones (`id`, `url`, `db`)
- Negative booleans (`is_not_valid`) — use `is_invalid` or flip the logic

### Error handling

- **Fail fast and loudly.** A crash immediately is better than silent data corruption.
- **Never swallow exceptions silently.** A bare `except: pass` or `catch (e) {}` is almost always a bug. If you must suppress, log and document *why*.
- **Always chain exceptions** in Python: `raise AppError("context") from original_error`. Bare re-raise loses context.
- Handle errors at the layer that can meaningfully respond — don't catch what you can't handle.

### Security — absolute blockers (CI failures)

These are never acceptable under any circumstances:

- ❌ `eval()`, `exec()`, or equivalent with any external/user input
- ❌ `subprocess(..., shell=True)` with any variable content — always pass argument lists
- ❌ SQL built by string concatenation — always use parameterized queries
- ❌ `pickle.loads()` / `pickle.load()` on any external data — it is arbitrary code execution
- ❌ `yaml.load()` — always `yaml.safe_load()`
- ❌ Hardcoded API keys, passwords, tokens, or credentials anywhere in source
- ❌ Secrets in `.env` files committed to the repo (`.env` in `.gitignore`; `.env.example` with placeholders is allowed)
- ❌ PII, passwords, or tokens logged at any log level
- ❌ `random` module for security purposes — use `secrets` (Python) or `crypto.randomBytes` (Node)
- ❌ MD5 or SHA-1 for any security purpose — use SHA-256+
- ❌ `innerHTML` with any unsanitized content in JavaScript

### Logging

- Use structured logging (JSON/key-value). Do not build log strings with f-strings in production code.
- **Never log** passwords, tokens, secrets, or PII at any level.
- Log levels have strict meaning: `DEBUG` (development only), `INFO` (normal ops), `WARNING` (unexpected but handled), `ERROR` (request failed), `CRITICAL` (service impaired).
- Every log line in a request context must include a correlation/request ID.

### Functions and design

- One function does one thing. If you can't see the whole function at once (target ≤40 lines), it's likely doing too much.
- Max 3–4 arguments; group related args into a config/data object beyond that.
- Prefer pure functions (same input → same output, no external mutation) where possible.
- Command–Query Separation: a function either returns a value OR changes state. Functions that do both are the hardest to reason about. Violations must be documented.

### Architecture

- Business logic never lives in API handlers or DB queries — it lives in a service/domain layer.
- DB queries never live in business logic — use a repository pattern.
- Import direction flows inward only: presentation → service → domain → infrastructure. Inner layers must not import outer layers.
- Fail-secure defaults: new features/endpoints default to off/denied, not on/public.
- YAGNI: don't build abstractions for requirements you don't have yet. Add generality when the second case arrives.

### Python-specific

- Formatter: **Black** (line-length=88). Non-negotiable. Run in pre-commit and CI.
- Linter: **Ruff** with `E/W/F/I/N/B/C4/UP/S/ANN/D` rulesets. Run in pre-commit and CI.
- Type checking: **mypy --strict**. All public functions/methods/class attributes must have type annotations.
- Testing: **pytest**. Test names must be sentences: `test_create_user_with_duplicate_email_raises_conflict_error`.
- Dependency management: **uv**. Pin versions in lockfiles. Run `pip-audit` in CI.
- Use `secrets` module for any cryptographic randomness. Use `pathlib.Path`, not `os.path`. Use f-strings, not `%`-formatting or `.format()`.
- See `CODING_STANDARDS.md` §2 for the full Python reference.

### Git

- Commit messages follow **Conventional Commits** format: `<type>[scope]: <description>` (imperative mood, ≤72 chars)
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`, `revert`
- Every commit must be atomic (one logical change) and must pass tests independently.
- Never force-push to `main` or shared branches.
- PRs target ≤400 lines changed. Larger PRs must be split.

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
- **Citations** — every factual claim, statistic, or externally sourced assertion in policy HTML must have an APA 7th edition footnote. See the Citation standards section of copilot-instructions.md.

---

## Accessibility — Non-Negotiable

Accessibility operates on two equal dimensions: **disability access** and **content democratization**. Neither overrides the other, and neither justifies weakening the project's policy positions or directness.

---

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
- Focus indicator must always be visible — never use `outline: none` or `outline: 0` without replacing it with an equally visible alternative. The site uses `:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }`.
- Interactive elements (links, buttons, controls) must have a descriptive accessible name: visible label text, `aria-label`, or `aria-labelledby`. Never use `title` attribute alone.
- Collapsible sections: use `<details>/<summary>` (accessible by default) or `aria-expanded` + `aria-controls` on custom accordions.
- Modal dialogs must trap focus and return focus to the trigger on close.

**Motion and animation**
- Every CSS animation and transition must be wrapped in or have an override under `@media (prefers-reduced-motion: reduce)` that stops or reduces motion to near-zero. The global override in `style.css` handles this — do not add `!important` transitions that escape it.
- Never auto-play video or audio. User must initiate.

**Forms**
- Every `<input>`, `<select>`, and `<textarea>` must have an associated `<label>` (via `for`/`id` or wrapping). `placeholder` alone is not a label.
- Error messages must identify the field and explain specifically what is wrong. Never use color alone to signal an error.

**Required CSS utilities (defined in `style.css` — do not redefine elsewhere)**
```css
/* Screen-reader-only — visually hidden, accessible to assistive tech */
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }

/* Visible when focused */
.sr-only.focusable:focus, .sr-only.focusable:focus-visible {
  position: static; width: auto; height: auto;
  margin: 0; overflow: visible; clip: auto; white-space: normal; }

/* Focus indicator */
:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important; } }
```

---

### Content accessibility (democratization)

Content accessibility means the site's policy content and contribution pathways are usable by people of varying educational backgrounds, technical expertise, and lived experience. It does **not** mean weakening positions, moderating language, or shifting policy toward the political center.

**Plain language**
- Every policy pillar and every major policy family must have a 1–2 sentence plain-language summary at approximately an 8th-grade reading level. This appears **alongside** the full technical position — not instead of it.
- **Every individual policy position (card) must have both a `rule-plain` field and a `rule-stmt` field:**
  - `rule-plain` — 1–3 sentences in plain language (~8th grade). What does this position do, and why does it matter? No jargon. Any person, regardless of education or background, must be able to read this and understand what the position says.
  - `rule-stmt` — The full technical/legal policy statement. This is where precise legal language, specific thresholds, enforcement mechanisms, and regulatory detail live.
  - Both fields are required on every card. `rule-plain` is not a summary of `rule-stmt` — it is an independent, accessible explanation written for a general audience. When they conflict, escalate for review; do not silently resolve.
  - In HTML: `<p class="rule-plain">` appears immediately after `<p class="rule-title">`, before `<p class="rule-stmt">`.
  - In the DB: `plain_language TEXT` column on the `positions` table — **to be added post-migration**. A null value is a data gap, not acceptable for canonical positions.
- Legal or technical jargon must be defined on first use with a tooltip, glossary link, or parenthetical.
- Policy card titles must be understandable without prior domain knowledge.
- Do not use weasel words or insider language in titles. "Big Tech Platforms Must Not Use Dark Patterns to Manipulate Users" is accessible; "Platform Interface Regulation Under Market Power Conditions" is not.

**Language and inclusion**
- Use gender-neutral language throughout: "persons" not "men"; singular "they/them"; avoid gendered role titles unless quoting a named law.
- Do not write in a voice that implies the reader is already politically aligned. Write as if a persuadable, politically independent person is reading for the first time.

**Contribution pathways**
- The Get Involved page must always prominently list all active contribution channels: GitHub (technical), Discord (community), and any active non-technical workflow (Google Docs, Notion, etc.).
- CONTRIBUTING.md and issue templates must be written for someone who has never used GitHub. Do not assume technical knowledge.
- Every policy proposal must have a clear path for non-technical review — the two-reviewer requirement applies regardless of whether the reviewer uses GitHub directly.

**Zoom and responsive layout**
- All content must be readable and fully operable at 200% browser zoom without horizontal scrolling.
- No fixed pixel heights that clip text when font size increases. Use `min-height` or `auto` height where needed.



## Build architecture

### Current state (Phase 1)

The site is hand-authored HTML. Policy position cards in `docs/pillars/*.html` are the most recently edited content. The DB (`data/policy_catalog_v2.sqlite`) was built from the v1 catalog and all tagged HTML cards and has not been fully reconciled with the current HTML.

**Until reconciliation is complete:**

- HTML edits are valid; backfill any new positions into the DB in the same commit
- Run `scripts/tag-policy-cards.py` after any HTML structural changes to normalize IDs

### Target state (Phase 2, post-reconciliation)

- `data/policy_catalog_v2.sqlite` is the single source of truth for all policy positions
- `pillars/*/overview.md` and `pillars/*/policy.md` are the source for narrative prose
- `docs/pillars/*.html` is generated output — do not hand-edit policy cards
- A build script (`scripts/generate-site.py`, TBD) will render HTML from DB + markdown
- CSS lives in `docs/assets/css/style.css` — single source, applied consistently site-wide
- Any content change must be made in the source (DB or markdown), then the site regenerated

### Consistency rules (apply now and in Phase 2)

- All styles: `docs/assets/css/style.css` only. No inline styles except `--accent-color` per pillar.
- All sitewide JS: `docs/assets/js/app.js` only. No inline scripts in HTML.
- All policy positions: must have a `XXXX-XXXX-0000` ID. Untagged cards are not canonical.
- All factual claims on the site: must have an APA 7th edition footnote.
