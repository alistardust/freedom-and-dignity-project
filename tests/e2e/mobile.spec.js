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
  { label: 'hamburger button', selector: '.nav-hamburger' },
  { label: 'entry card CTA',   selector: '.entry-card a' },
  { label: 'foundation card',  selector: '.f-card a' },
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
  // One pillar from each foundation.
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
