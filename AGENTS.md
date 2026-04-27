# Repo Instructions

## Project context

This repository is an active U.S. policy platform in development.

For shared repository context, source-of-truth guidance, provenance notes, and maintenance expectations, read:
- `.github/ai-repo-context.md`
- `.github/current-state.md`

Do not hardcode volatile counts from repo documentation into agent instructions. Verify current counts from the repository when they matter.

## Source of truth

The repository is currently in a pre-reconciliation state.

Until reconciliation is complete:
- site HTML and structured catalog data may both contain meaningful edits
- do not auto-resolve conflicts between HTML and database content
- treat divergences as review items
- preserve provenance

When auditing or editing policy content, use this general order:
1. `.github/current-state.md`
2. `docs/pillars/`
3. `policy/catalog/policy_catalog_v2.sqlite`
4. `policy/foundations/pillars/`

Shared repository context belongs in `.github/ai-repo-context.md`. Do not duplicate volatile repo facts, counts, or inventories in this instruction file. When shared repository context changes, update `.github/ai-repo-context.md` in the same change.

## Working with IDs and the catalog

- Policy position IDs use the v2 format: `XXXX-XXXX-0000` (regex: `^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$`), e.g. `HLTH-COVR-0001`.
- The canonical active position records live in the `positions` table in `policy/catalog/policy_catalog_v2.sqlite`.
- Domain codes (4 chars) and subdomain codes (4 chars) are defined in the `domains` and `subdomains` tables.
- Cross-pillar appearances are tracked in `position_pillar_appearances` rather than separate position records.
- v1-to-v2 ID mappings live in `legacy_id_map` (`old_id` → `new_id`, with `source` = `db`/`html`/`both`).
- `policy/catalog/policy_catalog_v2.sqlite` is historical. Use it for provenance, audit, and reconstruction tasks, but do not treat it as the canonical current source of active policy positions.

To rebuild the v2 catalog from source data:

```bash
scripts/build-catalog-v2.py
```

Do not hand-edit `policy/catalog/policy_catalog_v2.sqlite` unless the task is explicitly about an approved manual repair.

## Known context-sensitive edge cases

Catalog, migration, and provenance edge cases in this repo are context-sensitive and may change over time.

When they matter, check:
- `.github/current-state.md`
- `.github/ai-repo-context.md`
- the current catalog data in `data/`

## Editing guidance

- Prefer updating import logic and source-backed docs over manual data patching.
- Preserve provenance. If you convert or reconcile IDs, keep the relationship visible through the database rather than deleting history.
- When updating policy content, check the current site HTML first, then the DB, then the source logs.
- Keep changes surgical: context and traceability matter as much as the final wording.

---

## PolicyOS

PolicyOS is the cross-platform system-rules layer being developed in parallel with the pillar policy content. All PolicyOS research and drafts live in:

```
policy/policyos/
```

The current hierarchy (as of April 2026):

1. **Platform values** — `policy/policyos/policyos_platform_values_v1.md` — the moral/political anchor for all rules. Uses a `floor + duty` model (what policy must not violate vs. what it must actively secure). **Locked.**
2. **System principles** — `policy/policyos/policyos_1_0_rules_proposal.md` — cross-platform design rules (KERN/GEOG/FEDR/REGD/ENFA/AIGV families). Under review.
3. **Authoring OS** — `policy/policyos/policyos_authoring_os_v1.md` — how policy must be written, tested, scoped, enforced, and maintained (NORM/AUTH/TEST/ENFC/PLAC/MAINT families). Under review.

For the most current status and next steps, read the handoff file: `policy/policyos/copilot_handoff_2026-04-26.md`.

PolicyOS rules use the ID prefix `PLOS-` and `PAOS-`. Do not conflate them with pillar policy positions (`XXXX-XXXX-0000`).

Do not canonicalize PolicyOS rules into `system_rules.md` or the DB until the structural review is complete and approved.

---


## Documentation maintenance

Any change that affects repository behavior, workflow, build steps, architecture, testing expectations, documentation, or user-facing functionality must update the relevant documentation in the same change.

This includes, when applicable:
- `README.md`
- `.github/current-state.md`
- `.github/ai-repo-context.md`
- `system_rules.md`
- `policy/catalog/README.md`
- other affected repo documentation

"Repo documentation" means repository documentation files such as `README.md`, `.github/current-state.md`, `.github/ai-repo-context.md`, `system_rules.md`, `policy/catalog/README.md`, and related project documentation files.

"Docs" without "repo" means the website content in the `docs/` directory.

Do not update instruction files solely because repo facts or counts changed. Update instruction files when agent-behavior guidance changes.

---

## Citation standards

This project holds itself to the standard of a published policy document. Every factual claim, statistic, poll result, legal reference, and externally sourced assertion must be verified and cited.

Use concise inline citations in policy and documentation content, and use APA 7th edition in reference lists where reference lists are present.

For evolving citation patterns, formatting details, and repo-specific examples, follow the relevant project documentation rather than expanding this instruction file with long examples.

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

This project is committed to originality, proper attribution, and copyright compliance.

Core rules:
- Do not reproduce substantial verbatim text from copyrighted sources.
- Quote sparingly and only when exact wording materially matters.
- Prefer paraphrase, synthesis, and citation.
- Treat AI-generated research text as draft material that must be verified against real sources.
- Do not cite sources you have not verified.
- Attribute external ideas, framing, and arguments when they are materially derived from outside sources.
- When in doubt, use less quoted text, more original synthesis, and clearer citation.

Federal government materials may be quoted more freely where legally appropriate, but they must still be cited.

For evolving legal or formatting detail, follow relevant project documentation rather than expanding this instruction file with long copyright discussion.

---

## Quality and accuracy safeguards

This project is a public policy document. Accuracy, verification, and intellectual honesty are mandatory.

Before publishing any factual claim:
1. verify the source exists
2. verify the source actually supports the claim
3. check whether the source is current enough for the use
4. check whether the framing preserves the source's real context

Apply adversarial review to empirical claims. If meaningful counterevidence, uncertainty, or exceptions exist, acknowledge them honestly and revise the claim or framing as needed.

Treat AI-generated factual material as unverified draft text until it has been checked against real, accessible sources. If a source cannot be verified, remove the claim or clearly reframe it as the project's own position rather than a factual assertion.

### Language integrity

- Do not present the project's own policy positions as if they are established facts.
- Do not use weasel words ("many experts agree," "studies show") without citing specific experts and specific studies.
- Do not use emotional language in the research/sources sections; reserve advocacy framing for the mission and pillar narrative sections.
- Always distinguish between "this is what the research shows" and "this is what we believe should be done."

---

## Testing standards

Use the repo's current test tooling and commands.

Current test entry points:
- unit tests: `npm run test:unit`
- e2e tests: `npm run test:e2e`

Requirements:
- all new code must receive tests appropriate to the change
- relevant tests must be run before committing or pushing
- newly added or updated tests must pass
- failing tests must be fixed or explicitly discussed with the user before proceeding
- test behavior, not incidental implementation details
- update stale count-based assertions when structure changes
- write tests for the behavior a fix or feature is meant to enforce

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

## Repo-specific implementation constraints

Follow `CODING_STANDARDS.md` for detailed implementation standards. Keep this instruction file focused on durable repo-specific behavior.

Core rules for this repo:
- centralize shared CSS in `docs/assets/css/style.css`
- centralize sitewide JS in `docs/assets/js/app.js`
- prefer repo generators and scripts over copy-paste scaffolding when they exist
- avoid duplicating shared structural code across pages
- use structured IDs for policy positions where required by the current repo workflow
- keep factual claims verified and cited
- preserve provenance when reconciling content, IDs, or source material

Accessibility and content requirements are non-negotiable:
- maintain disability accessibility and content accessibility together
- keep content understandable to non-expert readers without weakening policy meaning
- keep contribution paths understandable to non-technical contributors
- ensure layouts remain usable under zoom and other accessibility constraints

For changing implementation detail, frontend conventions, accessibility specifics, and content-pattern guidance, follow:
- `CODING_STANDARDS.md`
- `.github/ai-repo-context.md`
- `.github/current-state.md`



## Build architecture

For current build and source-of-truth context, follow:
- `.github/ai-repo-context.md`
- `.github/current-state.md`

Current working rules:
- treat the repo as pre-reconciliation unless current repo documentation says otherwise
- make content changes in the appropriate source, not by bypassing the repo workflow
- keep styles centralized in `docs/assets/css/style.css`
- keep sitewide JS centralized in `docs/assets/js/app.js`
- ensure policy positions use structured IDs where required by the current repo workflow
- ensure factual claims on the site are verified and cited

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
