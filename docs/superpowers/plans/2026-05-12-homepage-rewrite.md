# Homepage Rewrite Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `src/pages/index.njk` per the approved design: remove Problem and Approach sections, add a History bridge section, update the hero, move the FDR block, update the foundations grid values callouts, update the nav, and replace the closing CTA block.

**Architecture:** Nav update first, then tests updated before running (TDD), then index.njk rewritten section-by-section, then build and full test suite. All edits to `.njk` source files only -- never to built `docs/` HTML. The approved design is in `~/.gstack/projects/alistardust-freedom-and-dignity-project/alice-main-eng-review-home-page-20260511-162717.md` and the companion design doc at `~/.gstack/projects/alistardust-freedom-and-dignity-project/alice-feature-7-policy-card-completion-design-20260511-153000.md`.

**Tech Stack:** Nunjucks templates in `src/pages/`, built with `node scripts/build-site.js`, tested with `npm run test:unit` (Vitest) and `npm run test:e2e` (Playwright/Firefox). Nav data in `src/data/nav.json`.

---

## Chunk 1: Nav and test scaffolding

### Task 1: Update nav.json -- replace Problem with Rights

**Files:**
- Modify: `src/data/nav.json`

- [ ] Open `src/data/nav.json`. Replace the Problem entry:

**Current:**
```json
{ "href": "problem.html", "label": "Problem" }
```

**New:**
```json
{ "href": "rights.html", "label": "Rights" }
```

Final `nav.json` must be:
```json
[
  { "href": "index.html",        "label": "Home" },
  { "href": "rights.html",       "label": "Rights" },
  { "href": "plan.html",         "label": "The Plan" },
  { "href": "get-involved.html", "label": "Get Involved" }
]
```

- [ ] Verify: `cat src/data/nav.json` -- confirm 4 entries, second is Rights.

---

### Task 2: Update 6 existing tests in site.spec.js

**Files:**
- Modify: `tests/e2e/site.spec.js`

These tests reference `problem` in the nav and must be updated BEFORE running the build. Make each replacement exactly as specified.

- [ ] **Update 1 -- nav label test.** Find the test that starts with `'nav has 4 links (Home, Problem...'`. Replace the entire test body:

```js
test('nav has 4 links (Home, Rights, The Plan, Get Involved)', async ({ page }) => {
  // Baked-in nav: Home, Rights, The Plan, Get Involved = 4
  await expect(page.locator('.nav-links a')).toHaveCount(4);
  await expect(page.locator('.nav-links a').nth(1)).toHaveText('Rights');
  await expect(page.locator('.nav-links a').nth(2)).toHaveText('The Plan');
});
```

- [ ] **Update 2 -- aria-current test.** Find the test `'nav item has aria-current="page" on nav-destination page'`. Replace:

```js
test('nav item has aria-current="page" on nav-destination page', async ({ page }) => {
  await page.goto('/rights.html');
  // Rights is a nav item -- its link should have aria-current="page" set at build time
  await expect(
    page.locator('.nav-links a[aria-current="page"][href*="rights"]')
  ).toBeAttached();
});
```

- [ ] **Update 3 -- Mission/Problem nav link describe block.** Find `test.describe('Mission nav link from all page types', ...)`. Replace the entire describe block:

```js
test.describe('Rights nav link from all page types', () => {
  const pages = [
    { url: '/',                               label: 'Homepage' },
    { url: '/policy-library.html',            label: 'Proposals' },
    { url: '/pillars/index.html',             label: 'Pillars index' },
    { url: '/pillars/healthcare.html',        label: 'Pillar page' },
    { url: '/compare/index.html',             label: 'Compare index' },
  ];

  for (const { url, label } of pages) {
    test(`${label} has Rights in nav`, async ({ page }) => {
      await page.goto(url);
      const link = page.locator('.nav-links a[href*="rights"]');
      await expect(link).toBeAttached();
      const href = await link.getAttribute('href');
      await page.goto(href.startsWith('http') ? href : new URL(href, page.url()).toString());
      await expect(page).toHaveTitle(/Rights.*Freedom and Dignity/i);
    });
  }
});
```

- [ ] **Update 4 -- problem.html nav tests.** Find the two tests `'nav Problem link is present'` and `'nav Problem link is marked active on problem page'` (they are in the problem.html describe block). Replace both:

```js
test('nav does not have a Problem nav link (problem page is not in main nav)', async ({ page }) => {
  await expect(page.locator('.nav-links a[href*="problem"]')).toHaveCount(0);
});
test('nav has Rights link visible on problem page', async ({ page }) => {
  await expect(page.locator('.nav-links a[href*="rights"]')).toBeAttached();
});
```

- [ ] **Update 5 -- roadmap page nav test.** Find the test `'nav has a Problem link'` (in the plan/roadmap describe block). Replace:

```js
test('nav has a Rights link', async ({ page }) => {
  await expect(page.locator('.nav-links a[href*="rights"]')).toBeAttached();
});
```

- [ ] **Update 6 -- Letter from the Founder nav tests.** Find two tests referencing `[href*="problem"]` in the Letter from the Founder describe block (`'nav has problem link visible'` and the `'nav and footer are injected'` test). Replace `[href*="problem"]` with `[href*="rights"]` in both tests.

- [ ] Verify no remaining `href*="problem"` in nav-assertion context: `grep -n 'href\*="problem"' tests/e2e/site.spec.js` -- should return 0 results (the problem.html describe block tests itself, not the nav).

---

### Task 3: Add 6 new tests to Homepage describe block

**Files:**
- Modify: `tests/e2e/site.spec.js`

Find the `test.describe('Homepage', ...)` block. Add these 6 tests inside it, after the existing homepage tests:

- [ ] Add all 6 tests:

```js
test('rights section appears before foundations section', async ({ page }) => {
  // Use DOM index rather than boundingBox -- boundingBox() returns null for off-screen elements
  const order = await page.evaluate(() => {
    const ids = Array.from(document.querySelectorAll('[id]')).map(el => el.id);
    return { rights: ids.indexOf('rights-heading'), building: ids.indexOf('building-heading') };
  });
  expect(order.rights).toBeGreaterThanOrEqual(0);
  expect(order.building).toBeGreaterThanOrEqual(0);
  expect(order.rights).toBeLessThan(order.building);
});

test('"Pillars" does not appear in authored page content', async ({ page }) => {
  // Scope to sections and page-hero only -- body includes injected nav/footer which
  // may contain "pillars" links (e.g. Pillars index in footer)
  const texts = await page.locator('section, .page-hero, .tour-section, .page-nav-cta').allTextContents();
  expect(texts.join(' ')).not.toMatch(/\bpillars?\b/i);
});

test('hero h1 contains the new promise statement', async ({ page }) => {
  const h1 = await page.locator('h1.hero-title').textContent();
  expect(h1).toMatch(/promise.*never kept|never kept.*promise/i);
});

test('history section is present with correct heading', async ({ page }) => {
  await expect(page.locator('#history-heading')).toBeAttached();
  await expect(page.locator('section[aria-labelledby="history-heading"]')).toBeAttached();
});

test('rights nav link is present on home page', async ({ page }) => {
  await expect(page.locator('.nav-links a[href*="rights"]')).toBeAttached();
});

test('problem section heading is absent from home page', async ({ page }) => {
  await expect(page.locator('#problem-heading')).toHaveCount(0);
});
```

- [ ] Verify no syntax errors: `npx playwright test --list 2>&1 | tail -5` -- should list tests without parse errors.

---

## Chunk 2: index.njk rewrite

### Task 4: Update page metadata and hero

**Files:**
- Modify: `src/pages/index.njk`

- [ ] **Update set description (line 2).** Replace:
```
{% set description = "Five structural foundations..." %}
```
with:
```
{% set description = "The promise America never kept, and the plan to keep it. An open-source policy platform built on rights, evidence, and public accountability." %}
```

- [ ] **Update twitter_description (line 5).** Replace the block content with:
```
{% block twitter_description %}The promise America never kept, and the plan to keep it. An open-source policy platform built on rights, evidence, and public accountability.{% endblock %}
```

- [ ] **Update page title (line 3).** Replace:
```
{% block title %}Freedom and Dignity Project — A New New Deal for Everyone{% endblock %}
```
with:
```
{% block title %}Freedom and Dignity Project — The promise America never kept, and the plan to keep it.{% endblock %}
```

- [ ] **Update og_description (line 4).** Replace:
```
{% block og_description %}An open project to rebuild America's rights, institutions, and economy for everyone.{% endblock %}
```
with:
```
{% block og_description %}The promise America never kept, and the plan to keep it. An open-source policy platform built on rights, evidence, and public accountability.{% endblock %}
```

- [ ] **Replace the entire `<div class="page-hero">` block.** The current block spans from `<div class="page-hero">` to its closing `</div>` (includes the large SVG btn-pin). Replace the entire block with:

```html
<!-- HERO -->
<div class="page-hero">
  <div class="hero-logo-wrap">
    <img src="assets/img/logo.svg" alt="Freedom and Dignity Project seal" width="148" height="148">
  </div>
  <div class="hero-eyebrow">The Next Chapter</div>
  <h1 class="hero-title">The promise America never kept, and the plan to keep it.</h1>
  <div class="hero-divider"><span>★ ★ ★ ★ ★</span></div>
  <p class="hero-mission">America has always spoken in the language of freedom. This project is about building the public systems that make freedom real: rights people can rely on, institutions people can trust, and a democracy strong enough to serve everyone.</p>
  <div class="hero-ctas">
    <a href="policy-library.html" class="btn-primary">See What We're Building</a>
    <a href="get-involved.html" class="btn-outline">Get Involved</a>
  </div>
</div>
```

---

### Task 5: Remove Problem and Approach sections

**Files:**
- Modify: `src/pages/index.njk`

- [ ] **Remove the Problem section entirely.** Find and delete the entire block from the comment `<!-- THE PROBLEM (brief) -->` through the closing `</section>` tag (the section with `aria-labelledby="problem-heading"`). This includes the `<section>`, `<div class="wrap">`, eyebrow, h2, paragraph, and link.

- [ ] **Remove the Approach section entirely.** Find and delete the entire block from `<!-- THE APPROACH -->` through its closing `</section>` (the section with `aria-labelledby="approach-heading"`).

- [ ] Verify: `grep -c "problem-heading\|approach-heading" src/pages/index.njk` -- must return 0.

---

### Task 6: Update the Rights section

**Files:**
- Modify: `src/pages/index.njk`

The existing Rights section has the right structure but needs updated copy, a class change, and em-dash removal.

- [ ] **Update the opening tag and eyebrow.** Find:
```html
<section class="bg-parchment ruled" aria-labelledby="rights-heading">
<div class="wrap">
  <div class="eyebrow" style="color:var(--mid)">The Foundation</div>
  <h2 id="rights-heading">Three Documents. One Foundation.</h2>
  <p style="max-width:640px;margin-bottom:2rem">Before policy comes rights. Three co-equal foundational documents define what this movement will not compromise on, the floor beneath everything else we build.</p>
```

Replace with:
```html
<section class="bg-cream ruled" aria-labelledby="rights-heading">
<div class="wrap">
  <div class="eyebrow">The Foundation</div>
  <h2 id="rights-heading">Rights come first.</h2>
  <p style="max-width:640px;margin-bottom:2rem">Before policy, there are rights. Franklin Roosevelt proposed a Second Bill of Rights in 1944 that would make freedom real for ordinary Americans. Congress never passed it. This project finishes that work, and goes further. Three co-equal documents define what this movement will not compromise on: the floor beneath everything else we build.</p>
```

- [ ] **Add "Read all three documents" link.** After the closing `</div>` of the `rights-doc-grid`, before the section's closing `</div></section>`, add:
```html
<p style="margin-top:1.5rem"><a href="rights.html" style="font-family:'Libre Franklin',sans-serif;font-weight:600;font-size:.9rem;color:var(--navy)">Read all three documents →</a></p>
```

- [ ] Verify no em-dashes remain in this section: `grep -n "\-\-\|—" src/pages/index.njk` and check the Rights section lines.

---

### Task 7: Add History bridge section

**Files:**
- Modify: `src/pages/index.njk`

Insert a new dark section immediately after the closing `</section>` of the Rights section, before the existing "WHAT WE'RE BUILDING" section comment.

- [ ] **Insert the History section.** The `fdr-block` (Roosevelt quote) moves here from the Platform section per locked decision D3 -- it stays in the DOM so the existing test at `site.spec.js` line 29-30 continues to pass. Insert the full block:

```html
<!-- THE SECOND NEW DEAL ARC -->
<section class="bg-dark on-dark ruled" aria-labelledby="history-heading">
<div class="wrap">
  <div class="eyebrow">How We Got Here</div>
  <h2 id="history-heading">Unfinished work.</h2>
  <p style="color:rgba(255,255,255,.85);max-width:640px;margin-bottom:1.25rem">Roosevelt proposed it. Congress refused it. King demanded it. Johnson advanced it and left it incomplete. Each generation inherited the gap between what was promised and what was delivered. This generation can close it. Not by hoping for leadership that comes from above, but by building the coalition that makes leadership impossible to ignore.</p>
  <!-- [VERIFY] citations needed: FDR Economic Bill of Rights 1944, MLK demands, LBJ Great Society legislation -- pre-ship task, not a blocker -->
  <div class="fdr-block" style="margin-top:2rem">
    <div class="fdr-label">Franklin D. Roosevelt, January 11, 1944</div>
    <blockquote>"True individual freedom cannot exist without economic security and independence. Necessitous men are not free men."</blockquote>
    <p class="fdr-note">He proposed eight new rights. Congress never passed them. This project finishes them, and goes further.<sup><a href="#fn1">[1]</a></sup></p>
  </div>
</div>
</section>
```

Note: The `[VERIFY]` comment is intentional -- the design doc flags the narrative claims as accurate but uncited, and marks them as a pre-ship task. The `fdr-block` moves here from the Platform section; its footnote ref is renumbered to fn1 (see Task 12).

- [ ] Verify: `grep -n "history-heading" src/pages/index.njk` -- should show exactly one `id=` and one `aria-labelledby=`.

---

### Task 8: Update the Platform section (foundations grid, remove FDR block, add PolicyOS)

**Files:**
- Modify: `src/pages/index.njk`

- [ ] **Update heading and intro copy.** Find:
```html
  <h2 id="building-heading">Five Foundations. Twenty-Five Pillars. Three Rights Frameworks.</h2>
  <p style="max-width:600px;margin-bottom:1.75rem;color:var(--ink)">The platform is organized into five structural foundations, each with concrete policy pillars. The outputs include three co-equal rights frameworks that finish what Roosevelt started in 1944, and go further than he could have imagined.</p>
```

Replace with:
```html
  <h2 id="building-heading">Five Foundations. <span data-dynamic="pillar-count">26</span> Policy Areas. Three Rights Frameworks.</h2>
  <p style="max-width:600px;margin-bottom:1.75rem;color:var(--ink)">The platform is organized into five structural foundations, each containing concrete policy positions. The rights frameworks establish the floor. The foundations build the public systems required to keep those rights real.</p>
```

- [ ] **Replace all 5 `f-num` divs with values callouts.** These exact strings are locked in the eng review (D5) -- they match policyos.html Layer 1. Replace each `<div class="f-num">Foundation N</div>` with the corresponding ready-to-paste block:

  **Foundation I (Accountable Power):**
  ```html
  <div style="font-family:'Libre Franklin',sans-serif;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--navy);opacity:.65;margin-bottom:.4rem">Grounded in: Accountable power, Democratic self-government</div>
  ```

  **Foundation II (Clean Democracy):**
  ```html
  <div style="font-family:'Libre Franklin',sans-serif;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--navy);opacity:.65;margin-bottom:.4rem">Grounded in: Democratic self-government, Equal standing</div>
  ```

  **Foundation III (Equal Justice):**
  ```html
  <div style="font-family:'Libre Franklin',sans-serif;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--navy);opacity:.65;margin-bottom:.4rem">Grounded in: Equal standing, Human dignity</div>
  ```

  **Foundation IV (Real Freedom):**
  ```html
  <div style="font-family:'Libre Franklin',sans-serif;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--navy);opacity:.65;margin-bottom:.4rem">Grounded in: Real liberty, Human dignity</div>
  ```

  **Foundation V (Freedom to Thrive):**
  ```html
  <div style="font-family:'Libre Franklin',sans-serif;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--navy);opacity:.65;margin-bottom:.4rem">Grounded in: Material security, Ecological habitability</div>
  ```

- [ ] **Remove the fdr-block from the Platform section.** It was moved to the History section in Task 7 -- it must not exist in two places. Delete the entire `<div class="fdr-block" ...>` block from inside the `building-heading` section only (the original location around line 158 of the original file).

- [ ] **Remove the old "See What We're Building" link paragraph** (`<p style="margin-top:1.75rem"><a href="policy-library.html" class="btn-primary">See What We're Building →</a></p>`). The hero now has this CTA.

- [ ] **Add PolicyOS blurb** after the closing `</div>` of `foundations-grid`, before the section closing `</div></section>`:

```html
  <p style="margin-top:2rem;max-width:640px;color:var(--ink);font-size:.95rem">This is not a list of demands without structure. Every policy position on this platform must identify the right it serves, the institution responsible, the enforcement mechanism, and the standard by which the public can judge success. Those rules are PolicyOS. <a href="policyos.html" style="color:var(--navy);font-weight:600">Read the framework.</a></p>
```

- [ ] Verify: `grep -n "f-num\|Pillars\.\|pillars\." src/pages/index.njk` -- all should return 0 results. Also confirm fdr-block is present in the history section and absent from the building section: `grep -n "fdr-block" src/pages/index.njk` -- should show exactly one result, inside the `history-heading` section.

---

### Task 9: Update Get Involved section -- external link rel attributes

**Files:**
- Modify: `src/pages/index.njk`

- [ ] Find the GitHub link (currently `rel="noopener"`):
```html
<a href="https://github.com/alistardust/freedom-and-dignity-project" class="entry-card-cta" target="_blank" rel="noopener">View on GitHub →</a>
```
Change `rel="noopener"` to `rel="noopener noreferrer"`.

- [ ] Find the Discord link (currently `rel="noopener"`):
```html
<a href="https://discord.gg/PGjFZnrhcr" class="entry-card-cta" target="_blank" rel="noopener">Join the Discord →</a>
```
Change `rel="noopener"` to `rel="noopener noreferrer"`.

- [ ] Verify: `grep -n 'rel="noopener"' src/pages/index.njk` -- should return 0 (all should now be `noopener noreferrer`).

---

### Task 10: Update Tour section Step 3

**Files:**
- Modify: `src/pages/index.njk`

- [ ] Find the Step 3 tour-step-desc span:
```html
<span class="tour-step-desc">Five foundations. <span data-dynamic="pillar-count">25</span> pillars. Three rights frameworks. The full system laid out clearly.</span>
```

Replace with (no count span, no "pillars"):
```html
<span class="tour-step-desc">Five foundations. Three rights frameworks. The full platform, laid out clearly.</span>
```

---

### Task 11: Replace site-closing with page-nav-cta

**Files:**
- Modify: `src/pages/index.njk`

- [ ] **Remove the `<div class="site-closing">` block entirely.** Find from `<!-- CLOSING -->` comment through the closing `</div>` of `site-closing`. Delete it all.

- [ ] **Add the page-nav-cta block** in its place, immediately before the `<div class="footnotes">` block:

```html
<!-- CLOSING CTA -->
<div class="page-nav-cta">
  <div class="wrap">
    <p style="max-width:640px;margin-bottom:1rem">The promise of this country is not kept by any one person, or any one party, or any one platform. It is kept by a generation that decides to keep it.</p>
    <p style="max-width:640px;margin-bottom:1.5rem">Come be part of this work.</p>
    <ul style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;list-style:none;padding:0">
      <li><a href="get-involved.html" class="btn-primary">Get Involved</a></li>
      <li><a href="policy-library.html" class="btn-outline">See the Platform</a></li>
    </ul>
  </div>
</div>
```

- [ ] Verify: `grep -n "site-closing" src/pages/index.njk` -- must return 0. `grep -n "page-nav-cta" src/pages/index.njk` -- must return at least 1.

---

### Task 12: Update footnotes

**Files:**
- Modify: `src/pages/index.njk`

The fdr-block moved to the History section in Task 7 with its footnote ref renumbered to `fn1`. The Problem section (removed in Task 5) held the original fn1 (EPI productivity) and fn2 (Federal Reserve wealth) refs. All three original footnotes are now orphaned from their original positions. Audit and renumber cleanly:

- [ ] The History section's `fdr-block` now uses `<sup><a href="#fn1">[1]</a></sup>`. Update the footnotes block to keep only the Roosevelt footnote, renumbered as fn1:

```html
<div class="footnotes">
  <div class="wrap">
    <p class="fn-head">Sources</p>
    <p id="fn1">[1] Roosevelt, State of the Union Address, January 11, 1944</p>
  </div>
</div>
```

- [ ] Remove the old fn1 (EPI productivity), fn2 (Federal Reserve wealth) definitions -- they are orphaned because the Problem section was removed.

- [ ] Remove the old fn3 definition (Roosevelt, original location) -- it is now fn1 in the updated footnotes block above.

- [ ] Verify no orphans: `grep -c 'href="#fn' src/pages/index.njk` and `grep -c 'id="fn' src/pages/index.njk` -- counts must match.

---

## Chunk 3: Build and verify

### Task 13: Build and run full test suite

**Files:**
- No source changes

- [ ] **Build the site:**
```bash
node scripts/build-site.js
```
Expected: no errors. The built `docs/index.html` reflects all changes.

- [ ] **Run unit tests:**
```bash
npm run test:unit
```
Expected: all tests pass. The unit tests do not cover E2E behavior, but `content.test.js` will catch em-dashes.

- [ ] **Run E2E tests (desktop Firefox only — mobile suite is separate):**
```bash
npm run test:e2e
```
Expected: all tests pass, including the 6 new homepage tests and the 6 updated nav tests.
Note: `test:e2e:firefox` is added by the mobile testing plan (a later task). Use `test:e2e` here.

- [ ] **Verify no "Pillars" in authored homepage content:**
```bash
grep -in "\bpillars\b" docs/index.html | grep -v "pillars/" | grep -v "pillar-count"
```
Expected: 0 results (or only results inside injected nav/footer, not authored sections).

- [ ] **Verify no em-dashes in built output:**
```bash
grep -n " -- \|—\|&#8212;" docs/index.html | grep -v '<title>'
```
Expected: 0 results (the `<title>` tag uses `—` as an approved exception; filtering it avoids a false positive).

- [ ] **Commit:**
```bash
git add src/pages/index.njk src/data/nav.json tests/e2e/site.spec.js docs/
git commit -m "feat(homepage): rewrite -- rights first, history bridge, new hero

- Remove Problem and Approach sections; problem.html stays in build
- New hero: 'The promise America never kept, and the plan to keep it.'
- Rights section first (bg-cream, updated copy and heading)
- New History bridge section (dark bg, FDR/MLK arc copy)
- Platform section: dynamic pillar count, values callouts replace f-num, PolicyOS blurb
- Tour Step 3: remove hardcoded pillar count
- CTA: page-nav-cta replaces site-closing
- nav.json: Rights replaces Problem in top nav
- 6 test updates + 6 new homepage tests

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Pre-implementation checklist (from eng review)

Before starting, verify:
- [ ] You are on the correct branch: `git branch --show-current`
- [ ] Working tree is clean: `git status`
- [ ] Test suite currently passes: `npm run test:unit` (all tests green)
- [ ] `problem.html` exists and stays in build -- do not delete it

## Pre-ship task (not a blocker for this plan)

The History section narrative (Roosevelt, King, Johnson claims) is accurate but uncited. Per the project citation standards, inline citations are required before this page ships publicly. A `[VERIFY]` comment is embedded in the History section HTML as a reminder. This must be resolved before launch -- add proper footnotes for the FDR 1944 speech, MLK demands, and LBJ Great Society legislation alongside the Roosevelt quote footnote already present.
