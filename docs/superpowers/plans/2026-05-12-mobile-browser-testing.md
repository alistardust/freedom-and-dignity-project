# Mobile Browser Testing Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add mobile browser test coverage (Android Chrome, iOS Safari, Firefox Mobile) with a shared constants module, a dedicated mobile spec, and a commit-time desktop+Chrome default with full CI coverage.

**Architecture:** Extract `SAMPLE_PILLARS` into `tests/e2e/shared.js` (no behaviour change), add three mobile Playwright projects scoped to both spec files, write `tests/e2e/mobile.spec.js` with four describe blocks (hamburger nav, overflow, tap targets, layout spot checks), then run the suite and fix mobile bugs surfaced.

**Tech Stack:** Playwright (Firefox, Chromium/WebKit device emulation), Node.js, GitHub Actions.

---

## Pre-implementation checklist

Before starting any task:

- [ ] Confirm you are on the correct branch: `git branch --show-current`
- [ ] Working tree is clean: `git status`
- [ ] Baseline passes: `npm run test:unit && npm run test:e2e`

---

## File map

| File | Action | Responsibility |
|------|--------|----------------|
| `tests/e2e/shared.js` | Create | Exports `SAMPLE_PILLARS` — single source of truth for both spec files |
| `tests/e2e/site.spec.js` | Modify | Replace inline `SAMPLE_PILLARS` declaration with `require('./shared')` |
| `playwright.config.js` | Modify | Add `mobile-chrome`, `mobile-safari`, `mobile-firefox` projects; add `testMatch` scoping to all projects |
| `package.json` | Modify | Add `test:e2e:all`, `test:e2e:firefox`, `test:e2e:mobile`, `test:e2e:chrome`, `test:e2e:safari`, `test:e2e:mobile-firefox`; update `test:e2e` to firefox+mobile-chrome |
| `.github/workflows/tests.yml` | Modify | Install chromium and webkit; switch e2e job to `npm run test:e2e:all` |
| `tests/e2e/mobile.spec.js` | Create | Mobile-specific tests: hamburger nav, horizontal overflow, tap targets, layout spot checks |
| `docs/assets/css/style.css` | Possibly modify | Fix mobile CSS bugs surfaced by the test run |
| `docs/assets/js/app.js` | Possibly modify | Fix mobile JS bugs surfaced by the test run |

---

## Chunk 1: Shared constants extraction

### Task 1: Create `tests/e2e/shared.js`

**Files:**
- Create: `tests/e2e/shared.js`

- [ ] Create the file with this exact content:

```js
/**
 * Shared constants for Playwright E2E specs.
 * Imported by site.spec.js and mobile.spec.js.
 */

// Each entry: { slug: string, title: string }
// slug matches the filename at docs/pillars/<slug>.html
const SAMPLE_PILLARS = [
  { slug: 'executive-power',               title: 'Executive Power' },
  { slug: 'elections-and-representation',  title: 'Elections' },
  { slug: 'anti-corruption',               title: 'Anti-Corruption' },
  { slug: 'equal-justice-and-policing',    title: 'Equal Justice' },
  { slug: 'rights-and-civil-liberties',    title: 'Rights' },
  { slug: 'courts-and-judicial-system',    title: 'Courts' },
  { slug: 'checks-and-balances',           title: 'Checks' },
  { slug: 'taxation-and-wealth',           title: 'Taxation' },
  { slug: 'healthcare',                    title: 'Healthcare' },
  { slug: 'antitrust-and-corporate-power', title: 'Antitrust' },
  { slug: 'information-and-media',         title: 'Information' },
  { slug: 'gun-policy',                    title: 'Gun Policy' },
  { slug: 'term-limits-and-fitness',       title: 'Term Limits' },
  { slug: 'administrative-state',          title: 'Administrative' },
  { slug: 'technology-and-ai',             title: 'Technology' },
  { slug: 'immigration',                   title: 'Immigration' },
  { slug: 'environment-and-agriculture',   title: 'Environment' },
  { slug: 'education',                     title: 'Education' },
  { slug: 'labor-and-workers-rights',      title: 'Labor' },
  { slug: 'housing',                       title: 'Housing' },
  { slug: 'consumer-rights',               title: 'Consumer' },
  { slug: 'data-rights-and-privacy',       title: 'Data Rights' },
  { slug: 'legislative-reform',            title: 'Legislative' },
  { slug: 'foreign-policy',                title: 'Foreign Policy' },
  { slug: 'science-technology-space',      title: 'Science Technology Space' },
];

module.exports = { SAMPLE_PILLARS };
```

---

### Task 2: Update `tests/e2e/site.spec.js`

**Files:**
- Modify: `tests/e2e/site.spec.js`

- [ ] Add the `shared.js` import after the existing `require` on line 6. The top of the file currently reads:

```js
const { test, expect } = require('@playwright/test');
```

Replace it with:

```js
const { test, expect } = require('@playwright/test');
const { SAMPLE_PILLARS } = require('./shared');
```

- [ ] Find and delete the inline `SAMPLE_PILLARS` declaration. It starts with the line:

```js
const SAMPLE_PILLARS = [
  { slug: 'executive-power',               title: 'Executive Power' },
```

and ends with the closing `];` (the one on its own line, after `science-technology-space`). Delete that entire block — the `for` loop that follows it stays exactly as-is. After the change, the section should read:

```js
// ── INDIVIDUAL PILLAR PAGES ───────────────────────────────────────────────────

for (const { slug, title } of SAMPLE_PILLARS) {
```

- [ ] Update the file-level comment at line 1–3 to reflect multi-browser:

```js
/**
 * Playwright E2E tests — Freedom and Dignity Project
 * Desktop: Firefox. Mobile profiles also run this file (see playwright.config.js).
 */
```

---

### Task 3: Verify and commit the refactor

**Files:** none new

- [ ] Run the unit tests: `npm run test:unit`
  Expected: all pass (unit tests do not depend on Playwright config).

- [ ] Run the E2E tests: `npm run test:e2e`
  Expected: same number of tests pass as before — this is a pure refactor. If any test fails, the `require` path or the SAMPLE_PILLARS content differs from the original; fix before proceeding.

- [ ] Commit:

```bash
git add tests/e2e/shared.js tests/e2e/site.spec.js
git commit -m "refactor(tests): extract SAMPLE_PILLARS into shared.js

No behaviour change. Both spec files will import from shared.js.
PILLAR_COUNT stays in site.spec.js pending the broader pillar
retirement cleanup task.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Chunk 2: Playwright config, npm scripts, CI

### Task 4: Update `playwright.config.js`

**Files:**
- Modify: `playwright.config.js`

- [ ] Replace the `projects` array. The current array is:

```js
projects: [
  { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  { name: 'visual-firefox', testDir: './tests/visual', use: { ...devices['Desktop Firefox'] } },
],
```

Replace it with:

```js
projects: [
  {
    name: 'firefox',
    use: { ...devices['Desktop Firefox'] },
    testMatch: ['**/site.spec.js'],
  },
  {
    name: 'mobile-chrome',
    use: { ...devices['Pixel 5'] },
    testMatch: ['**/site.spec.js', '**/mobile.spec.js'],
  },
  {
    name: 'mobile-safari',
    use: { ...devices['iPhone 14'] },
    testMatch: ['**/site.spec.js', '**/mobile.spec.js'],
  },
  {
    name: 'mobile-firefox',
    // Playwright has no Firefox mobile device preset — only Desktop Firefox and
    // Desktop Firefox HiDPI exist in the registry. Use a custom narrow viewport.
    // isMobile and hasTouch are not supported in Playwright's Firefox implementation.
    use: {
      browserName: 'firefox',
      viewport: { width: 390, height: 844 },
    },
    testMatch: ['**/site.spec.js', '**/mobile.spec.js'],
  },
  {
    name: 'visual-firefox',
    testDir: './tests/visual',
    use: { ...devices['Desktop Firefox'] },
  },
],
```

- [ ] Verify `mobile.spec.js` does not exist yet (`ls tests/e2e/mobile.spec.js` should return "No such file"). This is expected — `testMatch` references it but Playwright silently skips missing files until the next task creates it.

- [ ] Verify no syntax errors: `node -e "require('./playwright.config.js')" && echo "OK"`

---

### Task 5: Update `package.json` scripts

**Files:**
- Modify: `package.json`

- [ ] Replace the existing `"test:e2e"` line:

```json
"test:e2e": "playwright test --project=firefox",
```

with this block (preserving surrounding comma/structure):

```json
"test:e2e":              "playwright test --project=firefox --project=mobile-chrome",
"test:e2e:all":          "playwright test",
"test:e2e:firefox":      "playwright test --project=firefox",
"test:e2e:mobile":       "playwright test --project=mobile-chrome --project=mobile-safari --project=mobile-firefox",
"test:e2e:chrome":       "playwright test --project=mobile-chrome",
"test:e2e:safari":       "playwright test --project=mobile-safari",
"test:e2e:mobile-firefox": "playwright test --project=mobile-firefox",
```

- [ ] Verify JSON is valid: `node -e "require('./package.json')" && echo "OK"`

---

### Task 6: Update `.github/workflows/tests.yml`

**Files:**
- Modify: `.github/workflows/tests.yml`

- [ ] In the `e2e` job, update the job name:

```yaml
name: E2E tests (Firefox)
```
to:
```yaml
name: E2E tests (all browsers)
```

- [ ] In the `e2e` job, replace the Playwright install step:

```yaml
- run: npx playwright install firefox --with-deps
```
with:
```yaml
- run: npx playwright install firefox chromium webkit --with-deps
```

- [ ] In the `e2e` job, replace the test run step:

```yaml
- run: npm run test:e2e
```
with:
```yaml
- run: npm run test:e2e:all
```

- [ ] Verify the YAML is parseable: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/tests.yml'))" && echo "OK"` (or `node -e "require('js-yaml').load(require('fs').readFileSync('.github/workflows/tests.yml','utf8'))" && echo "OK"` if js-yaml is available).

---

### Task 7: Verify infrastructure and commit

- [ ] Run `npm run test:e2e:firefox` — must still pass with the same results as Task 3 (desktop-only; mobile.spec.js doesn't exist yet so mobile projects produce 0 tests from that file).

  Expected output includes lines like:
  ```
  Running N tests using N workers
  [firefox] ...
  ```
  No `mobile-chrome` / `mobile-safari` / `mobile-firefox` lines yet (or they show 0 tests) — that is correct at this stage.

- [ ] Commit:

```bash
git add playwright.config.js package.json .github/workflows/tests.yml
git commit -m "feat(tests): add mobile browser projects and npm scripts

- playwright.config.js: mobile-chrome (Pixel 5), mobile-safari (iPhone 14),
  mobile-firefox (custom 390x844 Firefox viewport); testMatch scoping per project
- package.json: test:e2e now runs firefox+mobile-chrome (commit-time default);
  test:e2e:all runs all four projects (CI); per-browser convenience aliases added
- tests.yml: install chromium+webkit alongside firefox; CI runs test:e2e:all

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Chunk 3: mobile.spec.js

### Task 8: Create `tests/e2e/mobile.spec.js`

**Files:**
- Create: `tests/e2e/mobile.spec.js`

- [ ] Create the file with this exact content:

```js
/**
 * Mobile browser E2E tests — Freedom and Dignity Project
 *
 * Runs on: mobile-chrome (Pixel 5), mobile-safari (iPhone 14),
 *          mobile-firefox (Firefox, 390x844 viewport).
 *
 * Covers: hamburger nav (homepage + pillar page), horizontal overflow,
 *         tap target sizes, and layout spot checks.
 */

const { test, expect } = require('@playwright/test');
const { SAMPLE_PILLARS } = require('./shared');

// ── HAMBURGER NAV ──────────────────────────────────────────────────────────────
// Tested on both a root page and a subdir page — app.js branches on
// /(pillars|compare)/ for asset path resolution, so the injected nav and
// overlay must work in both path contexts.

const BURGER_PAGES = [
  { label: 'homepage',    url: '/' },
  { label: 'pillar page', url: '/pillars/healthcare.html' },
];

for (const { label, url } of BURGER_PAGES) {
  test.describe(`Hamburger nav — ${label}`, () => {
    test.beforeEach(async ({ page }) => { await page.goto(url); });

    test('nav links are hidden at mobile viewport', async ({ page }) => {
      // .nav-links uses display:none at ≤600px — toBeHidden() correctly
      // handles display:none without the opacity:0 false-pass risk.
      await expect(page.locator('.nav-links a').first()).toBeHidden();
    });

    test('hamburger button is visible with aria-expanded=false on load', async ({ page }) => {
      const burger = page.locator('.nav-hamburger');
      await expect(burger).toBeVisible();
      await expect(burger).toHaveAttribute('aria-expanded', 'false');
    });

    test('clicking burger opens nav panel', async ({ page }) => {
      await page.locator('.nav-hamburger').click();
      await expect(page.locator('.nav-hamburger')).toHaveAttribute('aria-expanded', 'true');
      await expect(page.locator('.site-tree')).toHaveClass(/st-open/);
    });

    test('clicking burger again closes nav panel', async ({ page }) => {
      await page.locator('.nav-hamburger').click();
      await page.locator('.nav-hamburger').click();
      await expect(page.locator('.nav-hamburger')).toHaveAttribute('aria-expanded', 'false');
      await expect(page.locator('.site-tree')).not.toHaveClass(/st-open/);
    });

    test('clicking overlay closes nav panel', async ({ page }) => {
      await page.locator('.nav-hamburger').click();
      await page.locator('.st-overlay').click();
      await expect(page.locator('.nav-hamburger')).toHaveAttribute('aria-expanded', 'false');
      await expect(page.locator('.site-tree')).not.toHaveClass(/st-open/);
    });

    test('pressing Escape closes nav panel', async ({ page }) => {
      await page.locator('.nav-hamburger').click();
      await page.keyboard.press('Escape');
      await expect(page.locator('.nav-hamburger')).toHaveAttribute('aria-expanded', 'false');
      await expect(page.locator('.site-tree')).not.toHaveClass(/st-open/);
    });
  });
}

// ── NO HORIZONTAL OVERFLOW ────────────────────────────────────────────────────
// Compare pages are high-risk: complex grid layout, breakpoints down to 480px.
// Uses documentElement (not body) — body overflow-x:hidden masks real overflow.
// 1px tolerance for sub-pixel rounding differences across browsers.

const OVERFLOW_PAGES = [
  { label: 'homepage',      url: '/' },
  { label: 'pillars index', url: '/pillars/index.html' },
  { label: 'pillar page',   url: '/pillars/healthcare.html' },
  { label: 'compare page',  url: '/compare/republican-party.html' },
];

test.describe('No horizontal overflow', () => {
  for (const { label, url } of OVERFLOW_PAGES) {
    test(`${label} has no horizontal overflow`, async ({ page }) => {
      await page.goto(url);
      const overflows = await page.evaluate(
        () => document.documentElement.scrollWidth > window.innerWidth + 1
      );
      expect(overflows).toBe(false);
    });
  }
});

// ── TAP TARGET SIZES (WCAG 2.5.5) ────────────────────────────────────────────
// Both dimensions (width AND height) must be ≥ 44 CSS pixels.
// scrollIntoViewIfNeeded() is required — boundingBox() returns null for
// off-screen elements.

const TAP_TARGETS = [
  { label: 'hamburger button',  selector: '.nav-hamburger' },
  { label: 'entry card CTA',    selector: '.entry-card a' },
  { label: 'foundation card',   selector: '.f-card a' },
];

test.describe('Tap target sizes (WCAG 2.5.5)', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/'); });

  for (const { label, selector } of TAP_TARGETS) {
    test(`${label} meets 44×44 minimum`, async ({ page }) => {
      const locator = page.locator(selector).first();
      await locator.scrollIntoViewIfNeeded();
      const box = await locator.boundingBox();
      expect(box, `${selector} not found or not rendered`).not.toBeNull();
      expect(box.width).toBeGreaterThanOrEqual(44);
      expect(box.height).toBeGreaterThanOrEqual(44);
    });
  }
});

// ── MOBILE LAYOUT SPOT CHECKS ─────────────────────────────────────────────────

test.describe('Mobile layout spot checks', () => {
  test('foundations grid collapses to single column on homepage', async ({ page }) => {
    await page.goto('/');
    const cols = await page.evaluate(() =>
      getComputedStyle(document.querySelector('.foundations-grid')).gridTemplateColumns
    );
    // Single column: gridTemplateColumns resolves to one space-separated pixel value
    expect(cols.trim().split(/\s+/).length).toBe(1);
  });

  test('pillar sub-nav does not overflow its container', async ({ page }) => {
    await page.goto('/pillars/healthcare.html');
    const overflows = await page.evaluate(() => {
      const el = document.querySelector('.pil-snav');
      return el ? el.scrollWidth > el.offsetWidth : false;
    });
    expect(overflows).toBe(false);
  });

  test('policy section is present on pillar page', async ({ page }) => {
    await page.goto('/pillars/healthcare.html');
    await expect(page.locator('#pil-policy')).toBeAttached();
  });

  // Spot-check that SAMPLE_PILLARS entries resolve to real pages on mobile.
  // Tests one pillar from each foundation.
  const SPOT_PILLARS = [
    SAMPLE_PILLARS.find(p => p.slug === 'executive-power'),
    SAMPLE_PILLARS.find(p => p.slug === 'equal-justice-and-policing'),
    SAMPLE_PILLARS.find(p => p.slug === 'rights-and-civil-liberties'),
    SAMPLE_PILLARS.find(p => p.slug === 'healthcare'),
    SAMPLE_PILLARS.find(p => p.slug === 'housing'),
  ];

  for (const { slug, title } of SPOT_PILLARS) {
    test(`${title} pillar loads without overflow on mobile`, async ({ page }) => {
      await page.goto(`/pillars/${slug}.html`);
      await expect(page).toHaveTitle(new RegExp(title.split(' ')[0], 'i'));
      const overflows = await page.evaluate(
        () => document.documentElement.scrollWidth > window.innerWidth + 1
      );
      expect(overflows).toBe(false);
    });
  }
});
```

- [ ] Verify no syntax errors: `node -e "require('./tests/e2e/mobile.spec.js')" && echo "OK"`

---

## Chunk 4: First run, bug sweep, and final green

### Task 9: Run commit-time suite (firefox + mobile-chrome)

- [ ] Run: `npm run test:e2e`

  This runs desktop Firefox and mobile Chrome. Note every failure — do NOT fix yet. Record the failure list mentally or in a scratch file. Expected outputs fall into two categories:

  **a) `site.spec.js` failures on `mobile-chrome`** — tests that pass on Firefox but fail on mobile Chrome due to viewport-specific CSS visibility. These are not site bugs; they are desktop-only assertions that need a skip guard.

  **b) `mobile.spec.js` failures on `mobile-chrome`** — genuine site layout or interaction bugs. These need CSS/JS fixes.

---

### Task 10: Fix `site.spec.js` failures on mobile profiles

**Files:**
- Modify: `tests/e2e/site.spec.js`

For each `site.spec.js` test that fails on mobile but is correct on desktop (category a from Task 9):

- [ ] For each such test, add a skip guard **inside the test body** using the second `testInfo` parameter. Example — if `'nav links are visible'` fails on mobile because nav links are hidden:

  ```js
  test('nav links are visible', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name.startsWith('mobile'), 'desktop-only layout check');
    await expect(page.locator('.nav-links a').first()).toBeVisible();
  });
  ```

  **Critical:** use `testInfo.project.name`, not the `isMobile` fixture. `isMobile` is not set for the `mobile-firefox` project (custom viewport, not a device preset).

  **Do not delete any test.** The test must continue to run on the `firefox` desktop project.

- [ ] After adding all guards, run `npm run test:e2e:firefox` and confirm all desktop tests still pass.

- [ ] Run `npm run test:e2e` again and confirm the guarded tests are now skipped on mobile, not failing.

- [ ] If there are no `site.spec.js` failures on mobile, skip this task entirely.

- [ ] Commit if any guards were added:

```bash
git add tests/e2e/site.spec.js
git commit -m "fix(tests): skip desktop-only assertions on mobile profiles

Uses testInfo.project.name.startsWith('mobile') guard inside each test
body. isMobile fixture not used -- not set for mobile-firefox project.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 11: Mobile bug sweep — fix site CSS/JS failures

**Files:**
- Possibly modify: `docs/assets/css/style.css`
- Possibly modify: `docs/assets/js/app.js`

For each `mobile.spec.js` failure from Task 9 (category b — genuine site bugs):

- [ ] Triage each failure. Expected risk areas per the spec:
  - **`.pil-snav` overflow** — sub-nav overflows its container on narrow screens
  - **Horizontal overflow on compare pages** — complex grid at 480px breakpoint
  - **Foundation grid not collapsing** — grid CSS missing or wrong breakpoint
  - **Hamburger toggle visual** — `aria-expanded` passes but icon is stuck (X vs burger lines); verify visually with `npm run test:e2e -- --headed` if you suspect a CSS state bug

- [ ] For each distinct bug, make one atomic CSS or JS fix. All style fixes go to `docs/assets/css/style.css`; all logic fixes go to `docs/assets/js/app.js`. Never touch built `docs/**/*.html` directly.

- [ ] After each fix, run `npm run test:e2e` to confirm the specific test now passes and no regressions appear.

- [ ] Commit each distinct bug fix separately:

```bash
git add docs/assets/css/style.css   # or app.js
git commit -m "fix(mobile): <description of specific bug fixed>

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

  Examples of good commit descriptions:
  - `fix(mobile): prevent pil-snav horizontal overflow at narrow viewports`
  - `fix(mobile): collapse foundations grid to single column below 640px`
  - `fix(mobile): constrain compare table grid at 480px breakpoint`

- [ ] If no `mobile.spec.js` failures occurred, skip this task — note it in the commit that follows.

---

### Task 12: Full suite green and final commit

- [ ] Run the full four-project suite: `npm run test:e2e:all`

  Expected: all projects pass with zero failures. If any remain, return to Task 10 or Task 11 as appropriate.

- [ ] Run unit tests to confirm no regressions: `npm run test:unit`

- [ ] Commit `mobile.spec.js` (and any unfixed skip guards from Task 10 if not yet committed):

```bash
git add tests/e2e/mobile.spec.js
git commit -m "feat(tests): add mobile.spec.js — hamburger, overflow, tap targets, layout

4 describe blocks covering 3 mobile profiles (Pixel 5, iPhone 14,
390x844 Firefox viewport). Hamburger nav tested on homepage and pillar
page to catch app.js subdir path-mode differences.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

- [ ] Final verification: `npm run test:unit && npm run test:e2e`
  Expected: all pass. This is the default commit-time command going forward.
