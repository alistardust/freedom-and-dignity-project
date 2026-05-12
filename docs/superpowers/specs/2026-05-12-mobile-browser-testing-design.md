# Mobile Browser Testing — Design Spec

**Date:** 2026-05-12
**Status:** Approved

---

## Problem

The existing Playwright E2E suite runs exclusively on Desktop Firefox. The site has responsive CSS (breakpoints at 480px, 540px, 600px, 640px, 700px, 860px, 900px) and a JavaScript-driven hamburger nav, but none of this behaviour is verified by automated tests. Mobile layout regressions and touch interaction failures are invisible until a user reports them.

---

## Goal

Add full mobile browser test coverage across Android Chrome, iOS Safari, and Firefox Mobile. Mobile tests run on every commit alongside the existing desktop suite. A one-time bug sweep follows the initial test run to fix any layout or interaction failures the new tests surface.

---

## Architecture

### Approach

Shared constants module + separate mobile spec file.

- Shared module (`SAMPLE_PILLARS`) extracted from `site.spec.js` into `tests/e2e/shared.js`
- `site.spec.js` imports from `shared.js` — no behaviour change
- New `tests/e2e/mobile.spec.js` imports from `shared.js` and contains mobile-specific tests
- Playwright `testMatch` per project controls which spec files each project runs

### Why not a single spec file with guards?

`test.skip(!isMobile)` guards scattered through `site.spec.js` make it hard to see what the mobile surface area is. A dedicated `mobile.spec.js` keeps the mobile-specific contract explicit and independently readable.

---

## File Changes

### `tests/e2e/shared.js` (new)

Exports `SAMPLE_PILLARS`, the per-pillar slug/title list used by both spec files. `PILLAR_COUNT` is intentionally excluded here. As part of the broader effort to retire "pillar" naming across the codebase, the existing `PILLAR_COUNT` constant in `site.spec.js` will also be removed in a dedicated cleanup task — do not add it to `shared.js` or `mobile.spec.js`.

```js
// Each entry: { slug: string, title: string }
// slug matches the filename at docs/pillars/<slug>.html
// Used to generate one describe block per pillar page in both site.spec.js and mobile.spec.js.
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

### `tests/e2e/site.spec.js` (updated)

Remove the inline `SAMPLE_PILLARS` constant declaration and replace with:

```js
const { SAMPLE_PILLARS } = require('./shared');
```

No other changes. All existing tests remain exactly as-is.

## `site.spec.js` on Mobile Profiles

All three mobile projects run `site.spec.js` in addition to `mobile.spec.js`. Most existing tests will pass unchanged on mobile profiles because they assert DOM presence, counts, text content, and attributes — not layout or visibility. Known safe categories:

- Page title and heading assertions
- Count assertions (nav links exist in the DOM at mobile even when `display:none`)
- Text content assertions
- Attribute assertions (`aria-current`, `href`, etc.)
- Accordion open/close behaviour (click-based, not touch-specific)

**Expected failure surface:** Any `site.spec.js` test that uses `toBeVisible()` on an element that is hidden via CSS at mobile viewports could fail. The nav links use `display:none` at ≤600px — `toBeVisible()` on `.nav-links a` would fail.

**How to handle failures found during the mobile bug sweep:**

1. If the failure is a genuine layout/visibility bug in the site, fix the site (`style.css` / `app.js`).
2. If the failure is a desktop-only assertion that is correct for desktop but wrong on mobile (e.g. checking nav link visibility), add a project-name guard to skip it on mobile profiles. Do not use the `isMobile` Playwright fixture — it is not set for the `mobile-firefox` project (which uses a custom viewport, not a device preset). Use `testInfo.project.name` inside the test body instead:
   ```js
   test('nav links are visible', async ({ page }, testInfo) => {
     test.skip(testInfo.project.name.startsWith('mobile'), 'desktop-only layout check');
     // ... rest of test
   });
   ```
   `testInfo` is the second parameter of the test callback — it is not available in the conditional annotation form `test.skip(fn)`. Call it inside the test body where `testInfo` is in scope. Do not delete the test — keep it running on the `firefox` desktop project.
3. If a test is meaningful on both platforms but behaves differently, split it into a desktop and a mobile variant using the same guard.

Both fixing the site and adding a skip guard are valid resolutions that satisfy success criterion #1 — the choice depends on whether the failure reflects a real bug.

### `playwright.config.js` (updated)

Add three mobile projects and scope `testMatch` on all projects:

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
    // Playwright has no Firefox mobile device preset — only Desktop Firefox and Desktop Firefox HiDPI
    // exist in the registry. Use a custom narrow viewport with Firefox instead.
    // Note: isMobile and hasTouch are not supported in Playwright's Firefox implementation;
    // click-based interactions (including the hamburger nav) work correctly.
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

`visual-firefox` is unchanged — its `testDir` override already isolates it.

### `tests/e2e/mobile.spec.js` (new)

Four describe blocks:

#### 1. Hamburger nav

Runs on homepage. Verifies:

- `.nav-links` links are hidden via `display: none` at ≤600px (confirmed in `style.css`); use `toBeHidden()` which correctly handles `display: none` without the `opacity:0` false-pass risk
- `.nav-hamburger` button is visible and has `aria-expanded="false"` on load
- Clicking the burger sets `aria-expanded="true"` and adds `.st-open` to `.site-tree`
- Clicking the burger a second time toggles it closed (`st-open` removed, `aria-expanded="false"`)
- Clicking the `.st-overlay` closes the panel (`st-open` removed, `aria-expanded="false"`)
- Pressing Escape closes an open panel

#### 2. No horizontal overflow

Runs on homepage, pillars index, `pillars/healthcare.html`, and `compare/republican-party.html` (compare pages are identified as high-risk — complex grid, breakpoints down to 480px). For each:

```js
const overflow = await page.evaluate(
  // Use documentElement (not body) — body overflow-x:hidden masks real overflow.
  // Allow 1px tolerance for sub-pixel rounding.
  () => document.documentElement.scrollWidth > window.innerWidth + 1
);
expect(overflow).toBe(false);
```

This is the most common mobile layout regression and the most invisible to desktop testing.

#### 3. Tap target sizes

Checks that key interactive controls meet the WCAG 2.5.5 minimum of 44 × 44 CSS pixels — both dimensions must meet the minimum. All assertions run on the homepage. Scoped to:

- `.nav-hamburger` button
- Primary CTA buttons on the homepage (`.entry-card a`, `.f-card a`)

Uses `locator.boundingBox()` and asserts `box.width >= 44 && box.height >= 44` (WCAG 2.5.5 requires both dimensions to meet the minimum). Call `scrollIntoViewIfNeeded()` before `boundingBox()` — off-screen elements return `null`.

#### 4. Mobile layout spot checks

- **Homepage:** `.foundations-grid` resolves to a single column at ≤640px. Assert via:
  ```js
  const cols = await page.evaluate(() =>
    getComputedStyle(document.querySelector('.foundations-grid')).gridTemplateColumns
  );
  // Single column resolves to one space-separated value (a pixel measurement)
  expect(cols.trim().split(/\s+/).length).toBe(1);
  ```
- **Sample pillar page (`pillars/healthcare.html`):** `.pil-snav` (sub-nav) does not overflow its container (`scrollWidth <= offsetWidth`); policy section (`#pil-policy`) is attached

---

## Mobile Bug Sweep

After the initial test run, triage all failures. Expected areas of risk based on the CSS:

- Pillar sub-nav (`.pil-snav`) — multiple breakpoints, likely to overflow on narrow screens
- Compare pages — complex grid layout, several breakpoints down to 480px
- Foundation cards — grid collapse to single column
- `.nav-hamburger` CSS state — the hamburger button icon is driven by CSS transitions that target `.site-tree.st-open`. Verify that the visual icon state (e.g., X vs. burger lines) visually updates on toggle and is not stuck in a closed or open appearance due to a missing or mis-scoped CSS rule. This is separate from the `aria-expanded` assertion and must be verified visually with `--headed` if the test passes but the visual is wrong.

Fixes go to `docs/assets/css/style.css` and/or `docs/assets/js/app.js`. Each distinct layout bug gets its own atomic commit (`fix(mobile): ...`).

---

## npm Scripts

`npm run test:e2e` is the default command run before every commit. It runs desktop Firefox plus Android Chrome as a quick mobile sanity check. The full four-project suite is reserved for CI, keeping local commit time fast while still catching the most common mobile regressions immediately.

```json
"test:e2e":              "playwright test --project=firefox --project=mobile-chrome",
"test:e2e:all":          "playwright test",
"test:e2e:firefox":      "playwright test --project=firefox",
"test:e2e:mobile":       "playwright test --project=mobile-chrome --project=mobile-safari --project=mobile-firefox",
"test:e2e:chrome":       "playwright test --project=mobile-chrome",
"test:e2e:safari":       "playwright test --project=mobile-safari",
"test:e2e:mobile-firefox": "playwright test --project=mobile-firefox"
```

CI (`.github/workflows/tests.yml`) must be updated to run `npm run test:e2e:all` so iOS Safari and Firefox Mobile are included on every push and pull request. The existing `e2e` job installs only Firefox — it will need Chromium and WebKit added: `npx playwright install firefox chromium webkit --with-deps`.

Use `npm run test:e2e:firefox` when running the desktop suite in isolation (e.g., during homepage or nav work that predates mobile test setup).

---

## Out of Scope

- Visual regression snapshots on mobile (separate concern, can be added later under `visual-firefox`-equivalent mobile projects)
- Real-device testing (Playwright emulation is sufficient for layout and interaction)
- Performance testing on mobile

---

## Success Criteria

1. `npm run test:e2e` passes desktop Firefox and mobile Chrome with zero failures; `npm run test:e2e:all` passes all four projects
2. The horizontal overflow check passes on all tested pages
3. The hamburger nav open/close/escape cycle passes on all three mobile profiles
4. No regressions introduced to the existing desktop Firefox suite
